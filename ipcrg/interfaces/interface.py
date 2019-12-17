"""Abstract interface definition."""
import json
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from ..io import parse_edge_list


def filter_relation(relation, relation_type, relation_subtype, entity_ids):
    """
    Function to filter a relation for given: type, subtype and entitiy ids.

    Args:
        relation (dict): dictionary representing a relation.
        relation_type (str): relation type.
        relation_subtype (str): relation subtype.
        entity_ids (set): entitiy ids.

    Returns:
        bool: True is a relation match the filter, False otherwise.
    """
    return (
        relation['relation_type'] == relation_type
        and relation['relation_subtype'] == relation_subtype and
        (relation['source'] in entity_ids or relation['target'] in entity_ids)
    )


def filter_relation_ignore_subtype(
    relation, relation_type, relation_subtype, entity_ids
):
    """
    Function to filter a relation for given: type and entitiy ids.

    Args:
        relation (dict): dictionary representing a relation.
        relation_type (str): relation type.
        relation_subtype (str): relation subtype. Argument ignored.
        entity_ids (set): entitiy ids.

    Returns:
        bool: True is a relation match the filter, False otherwise.
    """
    return (
        relation['relation_type'] == relation_type and
        (relation['source'] in entity_ids or relation['target'] in entity_ids)
    )


class Interface:
    """
    Abstract definition of a db interface.

    Attributes:
        uri (str): uri connection string.
        database_name (str): name of the database.
        parameters (dict): parameters for the interface.
    """

    def __init__(self, uri, database_name, **parameters):
        """
        Initialize the interface.

        Args:
            uri (str): uri connection string.
            database_name (str): name of the database.
            parameters (dict): parameters for the interface.
        """
        self.uri = uri
        self.database_name = database_name
        self.parameters = parameters

    def create_entity(self, entity):
        """
        Create an entity.

        Args:
            entity (dict): entity representation.
        """
        raise NotImplementedError

    def create_entities(self, entities):
        """
        Create entities.

        Args:
            entities (typing.List[dict]): list of entity representations.
        """
        raise NotImplementedError

    def get_entities(self, query):
        """
        Get entities.

        Args:
            query (dict): query representation.

        Returns:
            typing.Iterable[dict]: an iterable of entities.
        """
        raise NotImplementedError

    def get_all_entities(self):
        """
        Get all entities.

        Returns:
            typing.Iterable[dict]: an iterable of entities.
        """
        raise NotImplementedError

    def get_entities_by_ids(self, ids):
        """
        Get entities by ids.

        Returns:
            typing.Iterable[dict]: an iterable of entities.
        """
        raise NotImplementedError

    def get_entity_types(self):
        """
        Get entity types.

        Returns:
            list: a list of entity types.
        """
        raise NotImplementedError

    def delete_all_entities(self):
        """Delete all entities."""
        raise NotImplementedError

    def create_relation(self, relation):
        """
        Create a relation.

        Args:
            relation (dict): relation representation.
        """
        raise NotImplementedError

    def create_relations(self, relations):
        """
        Create relations.

        Args:
            relations (typing.List[dict]): list of relation representations.
        """
        raise NotImplementedError

    def get_relations(self, query):
        """
        Get relations.

        Args:
            query (dict): query representation.

        Returns:
            typing.Iterable[dict]: an iterable of relations.
        """
        raise NotImplementedError

    def get_all_relations(self):
        """
        Get all relations.

        Returns:
            typing.Iterable[dict]: an iterable of relations.
        """
        raise NotImplementedError

    def get_relation_types(self):
        """
        Get relation types.

        Returns:
            list: a list of relation types.
        """
        raise NotImplementedError

    def get_relation_subtypes(self, relation_types=None):
        """
        Get relation subtypes.

        Args:
            relation_types (list): relation types to consider. Defaults to
                None, a.k.a. all relation types.

        Returns:
            dict: a dictionary of relation types mapped to the respective
                subtypes.
        """
        raise NotImplementedError

    def delete_all_relations(self):
        """Delete all relations."""
        raise NotImplementedError

    def create_indexes(self):
        """Create search indexes."""
        raise NotImplementedError

    def get_entity_out_neighbors(
        self,
        entity_query,
        relation_query={},
        relation_weight_fn=lambda relation: relation['weight']
    ):
        """
        Get outgoing neighbors from an entity.

        Args:
            entity_query (dict): query for a single entity. In case of multiple
                hits, considers the first one.
            relation_query (dict): query for the relations. Defaults to {},
                a.k.a. all the relations.
            relation_weight_fn (typing.Callable[[dict], float], optional):
                function to extract the weight from a relation. Defaults to
                extract the 'weight' field.

        Returns:
            typing.List[typing.Tuple[str, float]]: list of ids and weights.
        """
        raise NotImplementedError

    def get_entity_in_neighbors(
        self,
        entity_query,
        relation_query={},
        relation_weight_fn=lambda relation: relation['weight']
    ):
        """
        Get incoming neighbors from an entity.

        Args:
            entity_query (dict): query for a single entity. In case of multiple
                hits, considers the first one.
            relation_query (dict): query for the relations. Defaults to {},
                a.k.a. all the relations.
            relation_weight_fn (typing.Callable[[dict], float], optional):
                function to extract the weight from a relation. Defaults to
                extract the 'weight' field.

        Returns:
            typing.List[typing.Tuple[str, float]]: list of ids and weights.
        """
        raise NotImplementedError

    def _get_adjacency_and_index_mapping_df(
        self, relations, relation_filter_fn, relation_weight_fn
    ):
        """
        Get adjacency and the index mapping dataframe.

        Args:
            relations (list): a list of dictionaries representing the
                relations.
            relation_filter_fn (typing.Callable[[dict], bool]):
                function to filter a relation.
            relation_weight_fn (typing.Callable[[dict], float]):
                function to extract the weight from a relation.

        Returns:
            typing.Tuple[scipy.sparse.coo_matrix, pd.DataFrame]: a tuple
                containing the adjacency and the index mapping dataframe.
        """
        # select relations by type and id
        sources, targets, weights = zip(
            *[
                (
                    relation['source'], relation['target'],
                    relation_weight_fn(relation)
                ) for relation in relations if relation_filter_fn(relation)
            ]
        )
        connected_entities_ids = list(set(sources) | set(targets))
        entities = list(self.get_entities_by_ids(connected_entities_ids))
        n = len(entities)
        index_mapping_df = pd.read_json(json.dumps(entities))
        id_to_index = {
            an_id: index
            for index, an_id in enumerate(index_mapping_df['_id'].tolist())
        }
        return (
            coo_matrix(
                (
                    np.array(weights), (
                        np.array([id_to_index[source] for source in sources]),
                        np.array([id_to_index[target] for target in targets])
                    )
                ),
                shape=(n, n)
            ), index_mapping_df
        )

    def get_adjacency(
        self,
        entity_query={},
        relation_query={},
        relation_weight_fn=lambda relation: relation['weight'],
        ignore_relation_subtype=False
    ):
        """
        Get a dictionary of adjacency matrices given queries for entities
        and relations. Optionally a function to extract a custom name
        can be provided. Similarly the weight can be accessed with a custom
        function.

        Args:
            entity_query (dict): query for the entities. Defaults to {},
                a.k.a. all the entities.
            relation_query (dict): query for the relations. Defaults to {},
                a.k.a. all the relations.
            relation_weight_fn (typing.Callable[[dict], float], optional):
                function to extract the weight from a relation. Defaults to
                extract the 'weight' field.
            ignore_relation_subtype (bool, optional): ignore relation subtype
                information. Defaults to False, a.k.a. consider subtype.

        Returns:
            dict: dictionary keyed by relation types and containing as value
                a dictionary keyed by relation subtypes and containing as
                value a tuple of a scipy.sparse.coo_matrix representing the
                relation subtype-specific adjacency and a dataframe
                containing the index mappings.
                If ignore_relation_subtype is True the subtype dictionary
                contains only one key called 'adjacency' and the overlapping
                interactions between subtyped need to be handled by the user.
        """
        # get entity ids
        entity_ids = set(
            [entity['_id'] for entity in self.get_entities(entity_query)]
        )
        # get and persist relations
        relations = list(self.get_relations(relation_query))
        # relation types
        relation_types = set(
            [relation['relation_type'] for relation in relations]
        )
        # define relation type and subtype dictionary
        if ignore_relation_subtype:
            relation_type_dict = {
                relation_type: ['adjacency']
                for relation_type in relation_types
            }
        else:
            relation_type_dict = relation_type_dict = {
                relation_type: list(
                    set(
                        [
                            relation['relation_subtype']
                            for relation in relations
                        ]
                    )
                )
                for relation_type in relation_types
            }
        return {
            relation_type: {
                relation_subtype: self._get_adjacency_and_index_mapping_df(
                    relations,
                    relation_filter_fn=(
                        (
                            lambda relation: filter_relation_ignore_subtype(
                                relation, relation_type, relation_subtype,
                                entity_ids
                            )
                        ) if ignore_relation_subtype else (
                            lambda relation: filter_relation(
                                relation, relation_type, relation_subtype,
                                entity_ids
                            )
                        )
                    ),
                    relation_weight_fn=relation_weight_fn
                )
                for relation_subtype in relation_subtypes
            }
            for relation_type, relation_subtypes in relation_type_dict.items()
        }

    def from_edge_list_filepath(
        self,
        filepath,
        relation_class,
        source_entity_class,
        source_entity_parameters={},
        target_entity_class=None,
        target_entity_parameters=None,
        **kwargs
    ):
        """
        Insert entities and relations from filepath.

        Args:
            filepath (str): path to a file.
            relation_class (type(ipcrg.relations.relation.Relation)):
                class type for relation.
            source_entity_class (type(ipcrg.entities.entity.Entity)):
                class type for source entity.
            source_entity_parameters (dict): parameters for the
                source_entity_class.create_entities method. Defaults to {}.
            target_entity_class (type(ipcrg.entities.entity.Entity)):
                class type for target entity. Defaults to None, a.k.a same
                as source_entity_class.
            target_entity_parameters (dict): parameters for the
                target_entity_class.create_entities method. Defaults to None,
                a.k.a. same as source_entity_parameters.
            kwargs (dict): key-value arguments for pd.read_csv.
        """
        if target_entity_class is None:
            target_entity_class = source_entity_class
        if target_entity_parameters is None:
            target_entity_parameters = source_entity_parameters
        # parse the edge list
        df, source_entity_labels, target_entity_labels = parse_edge_list(
            filepath, **kwargs
        )
        # prepare source entity parameters
        _ = source_entity_parameters.pop('name', None)
        # source entities
        label_to_source_entity = {
            label: entity
            for label in source_entity_labels
            for entity in source_entity_class.
            create_entities(name=str(label), **source_entity_parameters)
        }
        # prepare target entity parameters
        _ = target_entity_parameters.pop('name', None)
        # target entities
        label_to_target_entity = {
            label: entity
            for label in target_entity_labels
            for entity in target_entity_class.
            create_entities(name=str(label), **target_entity_parameters)
        }
        # create them in the relational graph
        self.create_entities(
            set(label_to_source_entity.values())
            | set(label_to_target_entity.values())
        )
        # construct relations
        relations = set(
            [
                relation_class(
                    source=label_to_source_entity[row['source']],
                    target=label_to_target_entity[row['target']],
                    relation_subtype=row.get('subtype', ''),
                    weight=row.get('weight', 1.0)
                ) for _, row in df.iterrows()
            ]
        )
        # create them in the relational graph
        self.create_relations(relations)
