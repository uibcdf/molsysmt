from . import water
from . import ion
from . import small_molecule
from . import amino_acid
from . import terminal_capping
from . import nucleotide
from . import lipid
from . import saccharide
from . import oligosaccharide

from .is_group_type import is_group_type
from .get_group_type import get_group_type, get_group_type_from_group_name
from .get_bonded_atom_pairs import get_bonded_atom_pairs

_group_types = [
        'water',
        'ion',
        'small molecule',
        'amino acid',
        'terminal capping',
        'nucleotide',
        'lipid',
        'saccharide',
        'oligosaccharide'
        ]

_singular_group_type_to_plural = {
    'water': 'waters',
    'ion': 'ions',
    'small molecule': 'small molecules',
    'amino acid': 'amino acids',
    'terminal capping': 'terminal cappings',
    'nucleotide': 'nucleotides',
    'lipid': 'lipids',
    'saccharide': 'saccharides',
    'oligosaccharide': 'oligosaccharides',
}

_plural_group_types_to_singular = {
    'waters': 'water',
    'ions': 'ion',
    'small molecules': 'small molecule',
    'amino acids': 'amino acid',
    'terminal cappings': 'terminal capping',
    'nucleotides': 'nucleotide',
    'lipids': 'lipid',
    'saccharides': 'saccharide',
    'oligosaccharides': 'oligosaccharide',
}
