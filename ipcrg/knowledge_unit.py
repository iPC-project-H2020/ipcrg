"""Representation of a knowledge unit."""
import copy
import json
import hashlib


class KnowledgeUnit:
    """Definition of a knowledge unit.

    Attributes:
        parameters (dict): parameters for the knowledge unit.
    """

    def __init__(self, **parameters):
        """
        Initialize the knowledge unit.

        Args:
            parameters (dict): parameters for the knowledge unit.
        """
        self.parameters = parameters

    def to_dict(self):
        """
        Knowledge unit to dictionary.

        Returns:
            dict: dictionary representing the knowledge unit.
        """
        dict_representation = copy.deepcopy(self.parameters)
        dict_representation['_id'] = self.get_id()
        return dict_representation

    @staticmethod
    def from_dict(self, dict_representation):
        """
        Create a knowledge unit from a dictionary.

        Args:
            dict: dictionary representing the knowledge unit.

        Returns:
            KnowledgeUnit: a knowledge unit.
        """
        _ = dict_representation.pop('_id', None)
        return KnowledgeUnit(**dict_representation)

    def get_id(self, length=32):
        """
        Get id by hashing the knowledge unit using the MD5
        checksum of the parameters dumped in JSON.

        Args:
            length (int, optional): length of the id.
                Defaults to 32, since it's a MD5 checksum.

        Returns:
            dict: dictionary representing the knowledge unit.
        """
        json_string = str(self)
        return hashlib.md5(json_string.encode()).hexdigest()[:length]

    def __str__(self):
        """
        Knowledge unit to string.

        Returns:
            str: string representing the knowledge unit.
        """
        return json.dumps(self.parameters)

    def __hash__(self):
        """Hash function for a KnowledgeUnit."""
        return hash(self.get_id())

    def __eq__(self, other):
        """
        Test equality between KnowledgeUnits.

        Args:
            other (KnowledgeUnit): other knowledge unit.

        Returns:
            bool: true in case of equality, false otherwise.
        """
        if not isinstance(other, type(self)):
            raise NotImplementedError
        return self.get_id() == other.get_id()
