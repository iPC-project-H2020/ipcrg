"""Gene entity."""
from .entity import Entity
from ..io import get_gene_id_mapping_df


class Gene(Entity):
    """Gene entity."""

    def __init__(self, name, **parameters):
        """
        Initialize the gene entity.

        Args:
            name (str): entity name.
            parameters (dict): parameters for the Entity constructor.
        """
        super().__init__(name=name, entity_type='gene', **parameters)

    @staticmethod
    def create_entities(name, id_type='GeneID'):
        """
        Generate gene entities via the id mapping.

        Args:
            name (str): entity name.
            id_type (str): type of the identifier. Defaults to 'GeneID'.
                Supported values: 'GeneID' and 'Symbol'.

        Returns:
            typing.Iterable[Gene]: an iterable of genes.
        """
        matching_mapping = get_gene_id_mapping_df().query(
            '{} == "{}"'.format(id_type, name)
        )
        if matching_mapping.empty:
            yield Gene(name=name, **{id_type: name})
        else:
            for _, row in matching_mapping.iterrows():
                yield Gene.id_mapping_row_to_entity(row)

    @staticmethod
    def id_mapping_row_to_entity(row):
        """
        Generate a gene from an id mapping dataframe row.

        Args:
            row (pd.Series): row of the id mapping dataframe.

        Returns:
            Gene: a gene entity.
        """
        return Gene(
            name=row['Symbol'],
            synonyms=sorted(map(str, row.values)),
            **row.to_dict()
        )
