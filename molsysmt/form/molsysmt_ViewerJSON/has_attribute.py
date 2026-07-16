from molsysmt._private.arg_digestion import arg_digest
from . import attributes
from . import get_topological_attributes as get_topo


@arg_digest(form='molsysmt.ViewerJSON')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    """Attribute availability for `ViewerJSON` objects."""

    if not attributes[attribute]:
        return False

    if include_none:
        return True

    atoms = molecular_system.data.get('atoms', {}) or {}
    bonds = molecular_system.data.get('bonds', {}) or {}
    if isinstance(bonds, dict) and 'sets' in bonds:
        sets = bonds.get('sets', [])
        bonds = sets[0] if sets else {}
    structures = molecular_system.data.get(
        'structures',
        molecular_system.data.get('estructures', molecular_system.data.get('frames', [])),
    ) or []

    checkers = {
        'atom_index': lambda: range(get_topo.get_n_atoms_from_system(molecular_system, skip_digestion=True)),
        'atom_id': lambda: atoms.get('atom_id', None),
        'atom_name': lambda: atoms.get('atom_name', None),
        'group_id': lambda: atoms.get('group_id', atoms.get('group_ig', None)),
        'group_name': lambda: atoms.get('group_name', None),
        'chain_id': lambda: atoms.get('chain_id', None),
        'entity_id': lambda: atoms.get('entity_id', None),
        'formal_charge': lambda: get_topo.get_formal_charge_from_atom(molecular_system, skip_digestion=True),
        'partial_charge': lambda: get_topo.get_partial_charge_from_atom(molecular_system, skip_digestion=True),
        'n_atoms': lambda: get_topo.get_n_atoms_from_system(molecular_system, skip_digestion=True),
        'n_bonds': lambda: get_topo.get_n_bonds_from_system(molecular_system, skip_digestion=True),
        'bond_index': lambda: get_topo.get_bond_index_from_bond(molecular_system, skip_digestion=True),
        'bond_order': lambda: get_topo.get_bond_order_from_bond(molecular_system, skip_digestion=True),
        'bond_type': lambda: get_topo.get_bond_type_from_bond(molecular_system, skip_digestion=True),
        'bonded_atoms': lambda: bonds.get('atom_pairs', None),
        'coordinates': lambda: [frame.get('coordinates') for frame in structures if frame.get('coordinates') is not None],
        'time': lambda: [frame.get('time') for frame in structures if frame.get('time') is not None],
        'n_structures': lambda: structures,
    }

    try:
        value = checkers[attribute]()
    except Exception:
        return False

    if value is None:
        return False

    import numpy as np
    if isinstance(value, (list, tuple, np.ndarray)):
        return len(value) > 0

    return True
