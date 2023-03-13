_elements = [
        'atom',
        'group',
        'component',
        'molecule',
        'chain',
        'entity'
        ]

_element_indices = {
        'atom': 'atom_indices',
        'group': 'group_indices',
        'component': 'component_indices',
        'molecule': 'molecule_indices',
        'chain': 'chain_indices',
        'entity': 'entity_indices',
        }

_element_index = {
        'atom': 'atom_index',
        'group': 'group_index',
        'component': 'component_index',
        'molecule': 'molecule_index',
        'chain': 'chain_index',
        'entity': 'entity_index',
        }

from . import atom as atom
from . import group as group
from . import component as component
from . import molecule as molecule
from . import chain as chain
from . import entity as entity

from .elements_to_string import elements_to_string
from .is_element import is_element
