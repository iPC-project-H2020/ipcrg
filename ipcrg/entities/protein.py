"""Protein entity."""
from .entity import Entity
from ..io import get_protein_id_mapping_df


class Protein(Entity):
    """Protein entity."""

    def __init__(self, name, **parameters):
        """
        Initialize the protein entity.

        Args:
            name (str): entity name.
            parameters (dict): parameters for the Entity constructor.
        """
        super().__init__(name=name, entity_type='protein', **parameters)

    @staticmethod
    def create_entities(name, id_type='Gene_Name'):
        """
        Generate protein entities via the id mapping.

        Args:
            name (str): entity name.
            id_type (str): type of the identifier. Defaults to 'Gene_Name'.
                Supported values: 'UniProtKB-AC', 'GeneID', 'Gene_Name'.

        Returns:
            typing.Iterable[Protein]: an iterable of proteins.
        """
        matching_mapping = get_protein_id_mapping_df().query(
            '{} == "{}"'.format(id_type, name)
        )
        if matching_mapping.empty:
            yield Protein(name=name, **{id_type: name})
        else:
            for _, row in matching_mapping.iterrows():
                yield Protein.id_mapping_row_to_entity(row)

    @staticmethod
    def id_mapping_row_to_entity(row):
        """
        Generate a protein from an id mapping dataframe row.

        Args:
            row (pd.Series): row of the id mapping dataframe.

        Returns:
            Protein: a protein entity.
        """
        dict_representation = row.dropna().to_dict()
        if 'Gene_Synonym' in dict_representation:
            gene_synonyms = sorted(
                dict_representation['Gene_Synonym'].split(';')
            )
        else:
            gene_synonyms = []
        dict_representation['Gene_Synonym'] = gene_synonyms
        synonyms = [
            dict_representation[identifier]
            for identifier in ['UniProtKB-AC', 'GeneID', 'Gene_Name']
            if identifier in dict_representation
        ]
        return Protein(
            name=dict_representation.get(
                'Gene_Name', dict_representation['UniProtKB-AC']
            ),
            synonyms=sorted(map(str, synonyms)),
            **dict_representation
        )
