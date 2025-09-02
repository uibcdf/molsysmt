from .is_component_type import is_component_type
from .get_component_index import get_component_index
from .get_component_id import get_component_id
from .get_component_name import get_component_name
from .get_component_type import get_component_type
from .get_n_components import get_n_components

_component_types = [
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
        'polysaccharide', # >10 sugar units
        ]

_singular_component_type_to_plural = {
    'water': 'waters',
    'ion': 'ions',
    'small molecule': 'small molecules',
    'peptide': 'peptides',
    'protein': 'proteins',
    'lipid': 'lipids',
    'monosaccharide': 'monosaccharides',
    'disaccharide': 'disaccharides',
    'oligosaccharide': 'oligosaccharides',
    'polysaccharide': 'polysaccharides',
}

_plural_component_types_to_singular = {
    'waters': 'water',
    'ions': 'ion',
    'small molecules': 'small molecule',
    'peptides': 'peptide',
    'proteins': 'protein',
    'lipids': 'lipid',
    'monosaccharides': 'monosaccharide',
    'disaccharides': 'disaccharide',
    'oligosaccharides': 'oligosaccharide',
    'polysaccharides': 'polysaccharide',
}

