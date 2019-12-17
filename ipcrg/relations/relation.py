"""Representation of a relation."""
from jsonschema import validate
from ..knowledge_unit import KnowledgeUnit

RELATION_SCHEMA = {
    'type':
        'object',
    'properties':
        {
            'source': {
                'type': 'string'
            },
            'target': {
                'type': 'string'
            },
            'relation_type': {
                'type': 'string'
            },
            'relation_subtype': {
                'type': 'string'
            },
            'weight': {
                'type': 'number'
            },
        },
    'required':
        ['source', 'target', 'relation_type', 'relation_subtype', 'weight']
}


class Relation(KnowledgeUnit):
    """
    Basic relation.

    Attributes:
        source (ipcrg.entities.entity.Entity): source entity.
        target (ipcrg.entities.entity.Entity): target entity.
        relation_type (str): type of the relation.
        relation_subtype (str): relation subtype.
        weight (float): weight of the relation.
    """

    def __init__(
        self, source, target, relation_type, relation_subtype, weight=1.0
    ):
        """
        Initialize the basic relation.

        Args:
            source (ipcrg.entities.entity.Entity): source entity.
            target (ipcrg.entities.entity.Entity): target entity.
            relation_type (str): relation type.
            relation_subtype (str, optional): relation subtype. Defaults to ''.
            weight (float, optional): weight of the relation. Defaults to 1.0.
        """
        self.source = source
        self.target = target
        self.relation_type = relation_type
        self.relation_subtype = relation_subtype
        self.weight = weight
        parameters = {
            'source': self.source.to_dict()['_id'],
            'target': self.target.to_dict()['_id'],
            'relation_type': self.relation_type,
            'relation_subtype': self.relation_subtype,
            'weight': self.weight
        }
        validate(parameters, schema=RELATION_SCHEMA)
        super().__init__(**parameters)
