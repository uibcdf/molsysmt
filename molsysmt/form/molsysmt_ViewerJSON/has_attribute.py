from molsysmt._private.arg_digestion import arg_digest
from . import attributes
from . import get_topological_attributes as get_topo
from . import get_structural_attributes as get_struc


@arg_digest(form='molsysmt.ViewerJSON')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    """Attribute availability for `ViewerJSON` objects."""

    if not attributes[attribute]:
        return False

    checkers = {
        'atom_id': lambda: get_topo.get_atom_id_from_atom(molecular_system, skip_digestion=True),
        'atom_name': lambda: get_topo.get_atom_name_from_atom(molecular_system, skip_digestion=True),
        'group_id': lambda: get_topo.get_group_id_from_atom(molecular_system, skip_digestion=True),
        'group_name': lambda: get_topo.get_group_name_from_atom(molecular_system, skip_digestion=True),
        'chain_id': lambda: get_topo.get_chain_id_from_atom(molecular_system, skip_digestion=True),
        'entity_id': lambda: get_topo.get_entity_id_from_atom(molecular_system, skip_digestion=True),
        'formal_charge': lambda: get_topo.get_formal_charge_from_atom(molecular_system, skip_digestion=True),
        'n_atoms': lambda: get_topo.get_n_atoms_from_system(molecular_system, skip_digestion=True),
        'n_bonds': lambda: get_topo.get_n_bonds_from_system(molecular_system, skip_digestion=True),
        'bond_index': lambda: get_topo.get_bond_index_from_bond(molecular_system, skip_digestion=True),
        'bonded_atoms': lambda: get_topo.get_bonded_atoms_from_atom(molecular_system, skip_digestion=True),
        'coordinates': lambda: get_struc.get_coordinates_from_atom(molecular_system, skip_digestion=True),
        'time': lambda: get_struc.get_time_from_system(molecular_system, skip_digestion=True),
        'n_structures': lambda: get_struc.get_n_structures_from_system(molecular_system, skip_digestion=True),
    }

    try:
        value = checkers[attribute]()
    except:
        return False

    if include_none:
        return True

    if value is None:
        return False

    import numpy as np
    if isinstance(value, (list, tuple, np.ndarray)):
        return len(value) > 0

    return True
