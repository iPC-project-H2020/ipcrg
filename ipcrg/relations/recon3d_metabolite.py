"""Recon3DMetabolite relation."""
from .relation import Relation


class Recon3DMetabolite(Relation):
    """
    Recon3DMetabolite relation.

    Attributes:
        source (ipcrg.entities.entity.Entity): source entity.
        target (ipcrg.entities.entity.Entity): target entity.
        relation_type (str): type of the relation. Set to mondo.
        relation_subtype (str): relation subtype.
        weight (float): weight of the relation.
    """

    def __init__(self, source, target, relation_subtype='', weight=1.0):
        """
        Initialize the Recon3DMetabolite relation.

        Args:
            source (ipcrg.entities.entity.Entity): source entity.
            target (ipcrg.entities.entity.Entity): target entity.
            relation_subtype (str, optional): relation subtype. Defaults to ''.
            weight (float, optional): weight of the relation. Defaults to 1.0.
        """
        self.source = source
        self.target = target
        self.relation_type = 'recon3d-metabolite'
        self.relation_subtype = relation_subtype
        self.weight = weight
        parameters = {
            'source': self.source,
            'target': self.target,
            'relation_type': self.relation_type,
            'relation_subtype': self.relation_subtype,
            'weight': self.weight
        }
        super().__init__(**parameters)
