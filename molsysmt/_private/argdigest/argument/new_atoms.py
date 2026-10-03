"""Validating detached terminal-atom declarations."""

from copy import deepcopy

import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_new_atoms(new_atoms, caller=None):
    allowed = {
        "parent_atom_index",
        "atom_type",
        "atom_name",
        "atom_id",
        "isotope",
        "bond_order",
        "chemical_attributes",
    }
    if not isinstance(new_atoms, (list, tuple)):
        raise ArgumentError("new_atoms", value=new_atoms, caller=caller)
    result = deepcopy(list(new_atoms))
    for record in result:
        if not isinstance(record, dict) or set(record) - allowed:
            raise ArgumentError("new_atoms", value=new_atoms, caller=caller)
        parent = record.get("parent_atom_index")
        if (
            isinstance(parent, (bool, np.bool_))
            or not isinstance(parent, (int, np.integer))
            or parent < 0
            or not isinstance(record.get("atom_type"), str)
            or not isinstance(record.get("chemical_attributes", {}), dict)
        ):
            raise ArgumentError("new_atoms", value=new_atoms, caller=caller)
        order = record.get("bond_order", 1)
        if (
            isinstance(order, (bool, np.bool_))
            or not isinstance(order, (int, np.integer))
            or order not in (1, 2, 3)
        ):
            raise ArgumentError("new_atoms", value=new_atoms, caller=caller)
        isotope = record.get("isotope")
        if isotope is not None and (
            isinstance(isotope, (bool, np.bool_))
            or not isinstance(isotope, (int, np.integer))
            or not 0 <= isotope <= 65535
        ):
            raise ArgumentError("new_atoms", value=new_atoms, caller=caller)
        record["parent_atom_index"] = int(parent)
    return result
