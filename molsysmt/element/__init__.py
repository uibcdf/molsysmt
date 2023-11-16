from . import atom as atom
from . import group as group
from . import component as component
from . import molecule as molecule
from . import chain as chain
from . import entity as entity

from .is_element import is_element
from .is_composed_of import is_composed_of

_elements = [
        'atom',
        'group',
        'component',
        'molecule',
        'chain',
        'entity',
        'bond',
        'system'
        ]

_element_indices = {
        'atom': 'atom_indices',
        'group': 'group_indices',
        'component': 'component_indices',
        'molecule': 'molecule_indices',
        'chain': 'chain_indices',
        'entity': 'entity_indices',
        'bond': 'bond_indices'
        }

_element_index = {
        'atom': 'atom_index',
        'group': 'group_index',
        'component': 'component_index',
        'molecule': 'molecule_index',
        'chain': 'chain_index',
        'entity': 'entity_index',
        'bond': 'bond_index'
        }

_plural_elements_to_singular = {
    'atoms': 'atom',
    'groups': 'group',
    'residue': 'group',
    'residues': 'group',
    'components': 'component',
    'chains': 'chain',
    'molecules': 'molecule',
    'entities': 'entity',
    'bonds': 'bond',
}

_singular_element_to_plural = {
    'atom': 'atoms',
    'group': 'groups',
    'component': 'components',
    'chain': 'chains',
    'molecule': 'molecules',
    'entity': 'entities',
    'bond': 'bonds',
}

