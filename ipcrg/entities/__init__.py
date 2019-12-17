"""Initialize entities module."""
from .entity import Entity  # noqa
from .gene import Gene
from .protein import Protein
from .patient import Patient

# entity factory
ENTITY_FACTORY = {
    'gene': Gene,
    'protein': Protein,
    'patient': Patient
}
