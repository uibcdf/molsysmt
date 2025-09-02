from . import water
from . import ion
from . import small_molecule
from . import peptide
from . import protein
from . import dna
from . import rna
from . import lipid
from . import monosaccharide
from . import disaccharide
from . import oligosaccharide
from . import polysaccharide

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
        'monosaccharide', # 1 sugar unit
        'disaccharide', # 2 sugar units
        'oligosaccharide', # 3-10 sugar units
        'polysaccharide' # >10 sugar units
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
    'monosaccharide': 'monosaccharides',
    'disaccharide': 'disaccharides',
    'oligosaccharide': 'oligosaccharides',
    'polysaccharide': 'polysaccharides'
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
    'monosaccharides': 'monosaccharide',
    'disaccharides': 'disaccharide',
    'oligosaccharides': 'oligosaccharide',
    'polysaccharides': 'polysaccharide'
}

