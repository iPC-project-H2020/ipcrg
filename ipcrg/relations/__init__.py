"""Initialize relation module."""
from .relation import Relation  # noqa
from .curie import Curie
from .drug import Drug
from .mondo import MONDO
from .ppi import PPI
from .biogrid import BioGRID
from .reactome import Reactome
from .recon3d_metabolite import Recon3DMetabolite

# relation factory
RELATION_FACTORY = {
    'curie': Curie,
    'drug': Drug,
    'mondo': MONDO,
    'ppi': PPI,
    'biogrid': BioGRID,
    'reactome': Reactome,
    'recon3d-metabolite': Recon3DMetabolite
}
