from . import water
from . import ion
from . import small_molecule
from . import peptide
from . import protein
from . import dna
from . import rna
from . import lipid
from . import oligosaccharide

from .get_component_index import get_component_index
from .get_component_id import get_component_id
from .get_component_name import get_component_name
from .get_component_type import get_component_type
from .get_n_components import get_n_components
from .is_component_type import is_component_type

_component_types = [
        'water',
        'ion',
        'small molecule',
        'peptide',
        'protein',
        'dna',
        'rna',
        'lipid',
        'oligosaccharide'
        ]

_singular_component_type_to_plural = {
    'water': 'waters',
    'ion': 'ions',
    'small molecule': 'small molecules',
    'peptide': 'peptides',
    'protein': 'proteins',
    'lipid': 'lipids',
    'oligosaccharide': 'oligosaccharides',
}

_plural_component_types_to_singular = {
    'waters': 'water',
    'ions': 'ion',
    'small molecules': 'small molecule',
    'peptides': 'peptide',
    'proteins': 'protein',
    'lipids': 'lipid',
    'oligosaccharides': 'oligosaccharide',
}

