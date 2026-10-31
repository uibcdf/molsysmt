"""Prepare the admitted one-state chemical union before molecular publication."""

from copy import deepcopy

import numpy as np
import pandas as pd

from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt._private.variables import is_all

from ._table_columns import concatenate as _concat_columns


def union(left, right, atom_indices, topology, keep_ids):
    """Merge one declared state per source; never guess a multistate alignment."""
    from ._chemical_state import _concatenate_bond_tables, _remap_bond_atom_indices
    from .chemical_states import ChemicalStates

    if (
        left is None
        or right is None
        or left.n_chemical_states != 1
        or right.n_chemical_states != 1
    ):
        raise StructuralInconsistencyError(
            reason="Adding molecular systems requires one chemical state per source; absent, zero-state or multistate inputs need an explicit alignment policy.",
            caller="molsysmt.MolSys.add",
        )
    other = right if is_all(atom_indices) else right._extract_atoms(atom_indices)
    first, second = left._states[0], other._states[0]
    state = deepcopy(first)
    from molsysmt._private.preparation_history import remap_bond_history_references

    bonds = remap_bond_history_references(
        second.bonds, second._preparation_history, len(first._preparation_history)
    )
    state.bonds = _concatenate_bond_tables(
        first.bonds,
        _remap_bond_atom_indices(
            bonds, {index: index + left.n_atoms for index in range(other.n_atoms)}
        ),
    )
    state.atom_attributes = _concat_columns(
        first.atom_attributes, second.atom_attributes
    )
    state._normalize_atom_attribute_columns()
    membership = second.component_indices.copy()
    membership += len(first.components)
    state.component_indices = pd.concat(
        [first.component_indices, membership], ignore_index=True
    ).astype("Int64")
    state.components = _concat_columns(first.components, second.components)
    state._preparation_history.extend(deepcopy(second._preparation_history))
    state.state_id = first.state_id if first.state_id == second.state_id else None
    state.provenance_index = None
    declarations = {first.connectivity_completeness, second.connectivity_completeness}
    state.connectivity_completeness = (
        "complete"
        if declarations == {"complete"}
        else "unavailable"
        if declarations == {"unavailable"}
        else "partial"
    )
    result = ChemicalStates(n_atoms=left.n_atoms + other.n_atoms, skip_digestion=True)
    result._append_state(state, set_as_reference=True)
    result.rebuild_components(
        redefine_ids=not keep_ids, topology=topology, skip_digestion=True
    )
    return result


def stable_inventory_equals(left, right):
    """Compare ordered stable declarations without any chemical owner lookup."""
    if left is None or right is None:
        return left is right
    from ._atom_molecules import stored
    from ._chain_groups import by_chain

    if any(
        not getattr(left, name).equals(getattr(right, name))
        for name in ("atoms", "groups", "molecules", "entities", "chains")
    ):
        return False
    a, b = stored(left), stored(right)
    if (a is None) != (b is None) or a is not None and not np.array_equal(a, b):
        return False
    return all(np.array_equal(a, b) for a, b in zip(by_chain(left), by_chain(right)))
