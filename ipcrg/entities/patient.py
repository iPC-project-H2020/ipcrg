"""Patient entity."""
from .entity import Entity


class Patient(Entity):
    """Patient entity."""

    def __init__(self, name, **parameters):
        """
        Initialize the patient entity.

        Args:
            name (str): entity name.
            parameters (dict): additional parameters for the patient entity.
        """
        # NOTE: make sure name and entity_type are not overwritten.
        _ = parameters.pop('name', None)
        _ = parameters.pop('entity_type', None)
        super().__init__(name=name, entity_type='patient', **parameters)

    @staticmethod
    def create_entities(*args, **kwargs):
        """
        Generate patient entities.

        Args:
            args (list): list of arguments.
            kwargs (dict): key-value arguments.

        Returns:
            typing.Iterable[Patient]: an iterable of patient entities.
        """
        yield Patient(*args, **kwargs)