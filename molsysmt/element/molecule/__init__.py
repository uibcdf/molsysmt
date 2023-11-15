from . import water
from . import ion
from . import small_molecule
from . import peptide
from . import protein
from . import dna
from . import rna
from . import lipid
from . import oligosaccharide

from .get_molecule_index_from_atom import get_molecule_index_from_atom
from .get_molecule_id_from_molecule import get_molecule_id_from_molecule
from .get_molecule_type_from_molecule import get_molecule_type_from_molecule
from .get_molecule_name_from_molecule import get_molecule_name_from_molecule
from .get_molecule_type_from_group_names import get_molecule_type_from_group_names
from .get_molecule_type_from_sequence import get_molecule_type_from_sequence
from .get_n_molecules_from_system import get_n_molecules_from_system

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
    'protein': 'protein',
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


