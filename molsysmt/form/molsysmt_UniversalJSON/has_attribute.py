from molsysmt._private.arg_digestion import arg_digest
from . import attributes
from .get import (
    get_atom_id_from_atom,
    get_atom_name_from_atom,
    get_group_id_from_atom,
    get_group_name_from_atom,
    get_chain_id_from_atom,
    get_entity_id_from_atom,
    get_formal_charge_from_atom,
    get_n_atoms_from_system,
    get_n_bonds_from_system,
    get_bond_index_from_bond,
    get_bonded_atoms_from_atom,
    get_coordinates_from_system,
    get_time_from_system,
    get_n_structures_from_system,
)


@arg_digest(form='molsysmt.UniversalJSON')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    """Attribute availability for `UniversalJSON` objects."""

    if not attributes[attribute]:
        return False

    checkers = {
        'atom_id': lambda: get_atom_id_from_atom(molecular_system, skip_digestion=True),
        'atom_name': lambda: get_atom_name_from_atom(molecular_system, skip_digestion=True),
        'group_id': lambda: get_group_id_from_atom(molecular_system, skip_digestion=True),
        'group_name': lambda: get_group_name_from_atom(molecular_system, skip_digestion=True),
        'chain_id': lambda: get_chain_id_from_atom(molecular_system, skip_digestion=True),
        'entity_id': lambda: get_entity_id_from_atom(molecular_system, skip_digestion=True),
        'formal_charge': lambda: get_formal_charge_from_atom(molecular_system, skip_digestion=True),
        'n_atoms': lambda: get_n_atoms_from_system(molecular_system, skip_digestion=True),
        'n_bonds': lambda: get_n_bonds_from_system(molecular_system, skip_digestion=True),
        'bond_index': lambda: get_bond_index_from_bond(molecular_system, skip_digestion=True),
        'bonded_atoms': lambda: get_bonded_atoms_from_atom(molecular_system, skip_digestion=True),
        'coordinates': lambda: get_coordinates_from_system(molecular_system, skip_digestion=True),
        'time': lambda: get_time_from_system(molecular_system, skip_digestion=True),
        'n_structures': lambda: get_n_structures_from_system(molecular_system, skip_digestion=True),
    }

    value = checkers[attribute]()
    if include_none:
        return True

    if value is None:
        return False

    if isinstance(value, (list, tuple)):
        return len(value) > 0

    return True
