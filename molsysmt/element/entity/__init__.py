from .get_entity_index import get_entity_index
from .get_entity_id import get_entity_id
from .get_entity_name import get_entity_name
from .get_entity_type import get_entity_type
from .get_n_entities import get_n_entities

_entity_types = [
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

_singular_entity_type_to_plural = {
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

_plural_entity_types_to_singular = {
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

