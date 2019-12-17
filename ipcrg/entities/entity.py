"""Representation of an entity."""
import copy
from jsonschema import validate
from ..knowledge_unit import KnowledgeUnit

ENTITY_SCHEMA = {
    'type': 'object',
    'properties':
        {
            'name': {
                'type': 'string'
            },
            'entity_type': {
                'type': 'string'
            },
        },
    'required': ['name', 'entity_type']
}


class Entity(KnowledgeUnit):
    """
    Basic entity.

    Attributes:
        name (str): entity name.
        entity_type (str): entity type.
    """

    def __init__(self, name, entity_type, **kwargs):
        """
        Initialize the basic entity.

        Args:
            name (str): entity name.
            entity_type (str): entity type.
            kwargs (dict): key-value arguments passed to KnowledgeUnit
                contructor.
        """
        self.name = name
        self.entity_type = entity_type
        parameters = copy.deepcopy(kwargs)
        parameters['name'] = self.name
        parameters['entity_type'] = self.entity_type
        validate(parameters, schema=ENTITY_SCHEMA)
        super().__init__(**parameters)

    @staticmethod
    def from_dict(self, dict_representation):
        """
        Create an entity from a dictionary.

        Args:
            dict: dictionary representing the entityt.

        Returns:
            Entity: an Entity.
        """
        _ = dict_representation.pop('_id', None)
        return Entity(**dict_representation)

    @staticmethod
    def create_entities(*args, **kwargs):
        """
        Generate entities.

        Args:
            args (list): list of arguments.
            kwargs (dict): key-value arguments.

        Returns:
            typing.Iterable[Entity]: an iterable of entities.
        """
        raise NotImplementedError
