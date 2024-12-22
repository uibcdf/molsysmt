from . import water
from . import ion
from . import small_molecule
from . import peptide
from . import protein
from . import dna
from . import rna
from . import lipid
from . import oligosaccharide

from .get_molecule_index import get_molecule_index
from .get_molecule_id import get_molecule_id
from .get_molecule_name import get_molecule_name
from .get_molecule_type import get_molecule_type
from .get_n_molecules import get_n_molecules

from .is_molecule_type import is_molecule_type

_molecule_types = [
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

_singular_molecule_type_to_plural = {
    'water': 'waters',
    'ion': 'ions',
    'small molecule': 'small molecules',
    'peptide': 'peptides',
    'protein': 'proteins',
    'dna': 'dnas',
    'rna': 'rnas',
    'lipid': 'lipids',
    'oligosaccharide': 'oligosaccharides',
}

_plural_molecule_types_to_singular = {
    'waters': 'water',
    'ions': 'ion',
    'small molecules': 'small molecule',
    'peptides': 'peptide',
    'proteins': 'protein',
    'dnas': 'dna',
    'rnas': 'rna',
    'lipids': 'lipid',
    'oligosaccharides': 'oligosaccharide',
}


