"""MongoDB interface."""
import logging
import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, BulkWriteError
from .interface import Interface
from ..entities.entity import ENTITY_SCHEMA
from ..relations.relation import RELATION_SCHEMA

logger = logging.getLogger(__name__)


class MongoDBInterface(Interface):
    """
    Mongo DB interface.

    Attributes:
        client (MongoClient): a client for Mongo DB.
        entities_collection (str): name of the entity collection.
        relations_collection (str): name of the relation collection.
    """

    def __init__(self, uri, database_name, **parameters):
        """
        Initialize the interface.

        Args:
            uri (str): uri for Mongo DB.
            database_name (str): name of the database.
            parameters (dict): parameters for the interface.
        """
        self.client = MongoClient(uri)
        self.entities_collection = 'entities'
        self.relations_collection = 'relations'
        super().__init__(uri=uri, database_name=database_name, **parameters)

    def _create_one(self, knowledge_unit, collection_name):
        """
        Create one object in a database.

        Args:
            knowledge_unit (ipcrg.knowledge_unit.KnowledgeUnit): a knowledge
                unit.
            collection_name (str): name of the collection where the document
                is created.
        """
        try:
            self.client[self.database_name][collection_name].insert_one(
                knowledge_unit.to_dict()
            )
        except DuplicateKeyError:
            logger.debug('document already present skipping insertion')

    def _create_many(self, knowledge_units, collection_name):
        """
        Create many objects in a database.

        Args:
            knowledge_units
                (typing.Iterable[ipcrg.knowledge_unit.KnowledgeUnit]):
                    a list of knowledge units.
            collection_name (str): name of the collection where the documents
                are created.
        """
        try:
            self.client[self.database_name][collection_name].insert_many(
                [
                    knowledge_unit.to_dict()
                    for knowledge_unit in knowledge_units
                ],
                ordered=False
            )
        except BulkWriteError as exception:
            logger.debug(exception.details)

    def _get_entity_neighbors(
        self,
        entity_id,
        id_fn,
        relation_query,
        relation_weight_fn=lambda relation: relation['weight']
    ):
        """
        Get neighbors from an entity id.

        Args:
            entity_id (str): id for the entity.
            id_fn (typing.Callable[dict, str]): function to extract the
                id of the neighbors.
            relation_query (dict): query for the relations.
            relation_weight_fn (typing.Callable[[dict], float], optional):
                function to extract the weight from a relation. Defaults to
                extract the 'weight' field.

        Returns:
            typing.List[typing.Tuple[str, float]]: list of ids and weights.
        """
        return [
            (id_fn(relation), relation_weight_fn(relation))
            for relation in self.get_relations(relation_query)
        ]

    def create_entity(self, entity):
        """
        Create an entity.

        Args:
            entity (dict): entity representation.
        """
        self._create_one(entity, self.entities_collection)

    def create_entities(self, entities):
        """
        Create entities.

        Args:
            entities (typing.List[dict]): list of entity representations.
        """
        self._create_many(entities, self.entities_collection)

    def get_entities(self, query):
        """
        Get entities.

        Args:
            query (dict): query representation.

        Returns:
            typing.Iterable[dict]: an iterable of entities.
        """
        return self.client[self.database_name][self.entities_collection
                                               ].find(query)

    def get_all_entities(self):
        """
        Get all entities.

        Returns:
            typing.Iterable[dict]: an iterable of entities.
        """
        return self.client[self.database_name][self.entities_collection].find(
            {}
        )

    def get_entities_by_ids(self, ids):
        """
        Get entities by ids.

        Returns:
            typing.Iterable[dict]: an iterable of entities.
        """
        return self.get_entities({'_id': {'$in': ids}})

    def get_entity_types(self):
        """
        Get entity types.

        Returns:
            list: a list of entity types.
        """
        return self.client[self.database_name][self.entities_collection
                                               ].distinct('entity_type')

    def delete_all_entities(self):
        """Delete all entities."""
        self.client[self.database_name][self.entities_collection].delete_many(
            {}
        )

    def create_relation(self, relation):
        """
        Create a relation.

        Args:
            relation (dict): relation representation.
        """
        self._create_one(relation, self.relations_collection)

    def create_relations(self, relations):
        """
        Create relations.

        Args:
            relations (typing.List[dict]): list of relation representations.
        """
        self._create_many(relations, self.relations_collection)

    def get_relations(self, query):
        """
        Get relations.

        Args:
            query (dict): query representation.

        Returns:
            typing.Iterable[dict]: an iterable of relations.
        """
        return self.client[self.database_name][self.relations_collection
                                               ].find(query)

    def get_all_relations(self):
        """
        Get relations.

        Args:
            query (dict): query representation.

        Returns:
            typing.Iterable[dict]: an iterable of relations.
        """
        return self.client[self.database_name][self.relations_collection].find(
            {}
        )

    def get_relation_types(self):
        """
        Get relation types.

        Returns:
            list: a list of relation types.
        """
        return self.client[self.database_name][self.relations_collection
                                               ].distinct('relation_type')

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
        if relation_types is None:
            relation_types = self.get_relation_types()
        return {
            relation_type: self.client[self.database_name][
                self.relations_collection].distinct(
                    'relation_subtype',
                    filter={'relation_type': relation_type}
                )
            for relation_type in relation_types
        }

    def delete_all_relations(self):
        """Delete all relations."""
        self.client[self.database_name][self.relations_collection].delete_many(
            {}
        )

    def create_indexes(self):
        """Create search indexes."""
        # entities index
        self.client[self.database_name][self.entities_collection].create_index(
            [
                (parameter, pymongo.ASCENDING)
                for parameter in ENTITY_SCHEMA['required']
            ]
        )
        # relations index
        self.client[self.database_name][
            self.relations_collection].create_index(
                [
                    (parameter, pymongo.ASCENDING)
                    for parameter in RELATION_SCHEMA['required']
                ]
            )

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
        entity_id = next(self.get_entities(entity_query))['_id']
        relation_query['source'] = entity_id
        return self._get_entity_neighbors(
            entity_id,
            id_fn=lambda document: document['target'],
            relation_query=relation_query,
            relation_weight_fn=relation_weight_fn
        )

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
        entity_id = next(self.get_entities(entity_query))['_id']
        relation_query['target'] = entity_id
        return self._get_entity_neighbors(
            entity_id,
            id_fn=lambda document: document['source'],
            relation_query=relation_query,
            relation_weight_fn=relation_weight_fn
        )
