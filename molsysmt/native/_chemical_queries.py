"""Read declared chemical axes and counts without stable-inventory reconstruction."""

import numpy as np

from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt._private.variables import is_all
from molsysmt.basic._index_validation import validate_element_indices

from ._membership import lookup, pack


def count(item, element):
    """Read the relevant axis in the active chemical scope, without a fallback."""
    if element == "atom":
        return item.n_atoms
    state = item._resolve_chemical_state()
    return len(state.bonds if element == "bond" else state.components)


def indices(item, element, selected, *, state=None):
    """Validate against the selected state's axis before any positional access."""
    size = (
        count(item, element)
        if state is None
        else item.n_atoms
        if element == "atom"
        else len(state.bonds if element == "bond" else state.components)
    )
    if is_all(selected):
        return list(range(size))
    return validate_element_indices(
        item,
        selected,
        element,
        "indices",
        "chemical-state query",
        count_getter=lambda _: size,
    )


def _membership(item, state, positions=None):
    membership = state.component_indices
    selected = membership if positions is None else membership.iloc[positions]
    values = selected.to_numpy(dtype=np.int64, na_value=-1)
    if (
        len(membership) != item.n_atoms
        or selected.lt(0).any()
        or np.any(values >= len(state.components))
    ):
        raise StructuralInconsistencyError(
            reason="Stored component membership does not match the chemical atom/component axes.",
            caller="molsysmt.native.ChemicalStates.get",
        )
    return values


def system(item, attribute):
    """Separate collection inventory from selected-state declarations/counts."""
    if attribute == "n_atoms":
        return item.n_atoms
    if attribute == "n_chemical_states":
        return item.n_chemical_states
    if attribute == "chemical_state_index":
        return list(range(item.n_chemical_states))
    if attribute == "chemical_state_id":
        return [state.state_id for state in item._states]
    if attribute == "reference_chemical_state_index":
        return item.reference_chemical_state_index
    if attribute == "n_bonds":
        return count(item, "bond")
    if attribute == "n_components":
        return count(item, "component")
    return getattr(item._resolve_chemical_state(), attribute)


def project(item, element, attribute, selected="all"):
    """Project stored axes with ordered repetitions and defined empty results."""
    if is_all(selected):
        if attribute == "n_" + element + "s":
            return count(item, element)
        if element == "atom" and attribute == "n_components":
            return count(item, "component")
    positions = indices(item, element, selected)
    if positions is None:
        return None
    if attribute == element + "_index":
        return positions
    if attribute == "n_" + element + "s":
        return len(positions)
    state = item._resolve_chemical_state()
    return project_arrays(
        element,
        attribute,
        positions,
        n_atoms=item.n_atoms,
        n_components=len(state.components),
        membership=lambda selected=None: _membership(item, state, selected),
        pairs=lambda: state.bonds[["atom1_index", "atom2_index"]].to_numpy(
            dtype=np.int64
        ),
    )


def project_arrays(
    element, attribute, positions, *, n_atoms, n_components, membership, pairs
):
    """Project stored incidence/membership arrays independently of their container."""
    if element == "atom":
        if attribute in {"component_index", "n_components"}:
            members = membership(positions)
            if attribute == "component_index":
                return [int(value) if value >= 0 else None for value in members]
            return int(len(np.unique(members[members >= 0])))
        bond_pairs = pairs()
        if attribute == "n_bonds":
            degrees = np.bincount(bond_pairs.ravel(), minlength=n_atoms)
            return degrees[positions].tolist()
        grouped = pack(bond_pairs.ravel(), n_atoms)
        return [(lookup(index, grouped) // 2).tolist() for index in positions]
    members = membership()
    if attribute == "n_atoms":
        counts = np.bincount(members[members >= 0], minlength=n_components)
        return counts[positions].tolist()
    if attribute == "atom_index":
        grouped = pack(members, n_components)
        return [lookup(index, grouped).tolist() for index in positions]
    # Count each stored edge once per incident component. Cross-component edges
    # count for both declared endpoints; unknown endpoints acquire no membership.
    bond_pairs = pairs()
    endpoints = members[bond_pairs]
    first, second = endpoints[:, 0], endpoints[:, 1]
    parents = np.r_[first[first >= 0], second[(second >= 0) & (second != first)]]
    counts = np.bincount(parents, minlength=n_components)
    return counts[positions].tolist()
