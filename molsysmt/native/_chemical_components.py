"""Own state-local graph partitions and exact component metadata matching."""

import numpy as np
import pandas as pd


def indices_from_bonds(n_atoms, bonds):
    """Infer a partition using the existing stored participation convention."""
    from molsysmt._private.rust_backend import (
        get_component_index_from_bonded_atom_pairs,
    )

    if "joins_components" in bonds.columns:
        participates = ~bonds["joins_components"].eq(False).fillna(False)
        bonds = bonds.loc[participates]
    pairs = np.asarray(bonds[["atom1_index", "atom2_index"]].to_numpy(), dtype=np.int64)
    pairs = pairs.reshape((-1, 2))
    return get_component_index_from_bonded_atom_pairs(pairs, np.int64(n_atoms)).astype(
        np.int64
    )


def unchanged_rows(old_indices, new_indices, n_old, n_new, *, atom_indices=None):
    """Match exact full source atom sets in linear memory and time.

    A restricted subset cannot justify metadata transfer merely by retaining
    every atom of a new component. Its cardinality must also equal the full
    original component. Unknown old membership cannot establish equality.
    """
    if not n_old or not n_new:
        return np.empty(0, dtype=np.int64), np.empty(0, dtype=np.int64)
    valid = (old_indices >= 0) & (old_indices < n_old)
    known = np.where(valid, old_indices, -1)
    if atom_indices is not None:
        known = known[atom_indices]
    minimum = np.full(n_new, n_old, dtype=np.int64)
    maximum = np.full(n_new, -1, dtype=np.int64)
    represented = new_indices >= 0
    np.minimum.at(minimum, new_indices[represented], known[represented])
    np.maximum.at(maximum, new_indices[represented], known[represented])
    new_rows = np.flatnonzero((minimum >= 0) & (minimum == maximum))
    old_rows = minimum[new_rows]
    old_counts = np.bincount(old_indices[valid], minlength=n_old)
    new_counts = np.bincount(new_indices[represented], minlength=n_new)
    unchanged = new_counts[new_rows] == old_counts[old_rows]
    return new_rows[unchanged], old_rows[unchanged]


def restrict(state, atom_indices, bonds):
    """Stage components for a restriction without changing the source state.

    Complete graphs yield induced partitions with exact-atom-set metadata
    matching. Otherwise rows retain their meaning as restricted declarations,
    with downgraded completeness when their original memberships were cut.
    """
    import pandas as pd

    from ._chemical_state import Components_DataFrame

    old_indices = state.component_indices.to_numpy(dtype=np.int64, na_value=-1)
    if state.connectivity_completeness == "complete":
        indices = indices_from_bonds(len(atom_indices), bonds)
        n_components = int(indices.max()) + 1 if len(indices) else 0
        components = Components_DataFrame(n_components=n_components)
        components["component_id"] = pd.array(
            np.arange(n_components).astype(str), dtype="string"
        )
        components["component_name"] = pd.NA
        components["component_type"] = pd.NA
        new_rows, old_rows = unchanged_rows(
            old_indices,
            indices,
            len(state.components),
            n_components,
            atom_indices=atom_indices,
        )
        for column in components.columns:
            components.loc[new_rows, column] = (
                state.components[column].iloc[old_rows].to_numpy()
            )
        participation_complete = not len(bonds) or (
            "joins_components" in bonds.columns
            and not bonds["joins_components"].isna().any()
        )
        completeness = "complete" if participation_complete else "partial"
        evidence = (
            state.component_evidence
            if len(new_rows) == n_components
            and state.component_completeness == "complete"
            else "inferred"
        )
        return components, pd.Series(indices, dtype="Int64"), completeness, evidence

    membership = state.component_indices.iloc[atom_indices].copy()
    old_rows = membership.dropna().unique().tolist()
    components = Components_DataFrame(n_components=len(old_rows))
    for column in state.components.columns:
        components[column] = (
            state.components[column].iloc[old_rows].reset_index(drop=True)
        )
    mapping = {old: new for new, old in enumerate(old_rows)}
    restricted = membership.map(mapping).astype("Int64").reset_index(drop=True)
    completeness = state.component_completeness
    if completeness == "complete":
        source_counts = np.bincount(
            old_indices[old_indices >= 0], minlength=len(state.components)
        )
        kept_indices = old_indices[atom_indices]
        kept_counts = np.bincount(
            kept_indices[kept_indices >= 0], minlength=len(state.components)
        )
        if np.any(source_counts[old_rows] != kept_counts[old_rows]):
            completeness = "partial"
    return components, restricted, completeness, state.component_evidence


def group_components(topology, component_indices):
    """Derive per-group component membership from atom-aligned state data."""
    n_groups = topology.n_groups
    _adf = pd.DataFrame(
        {
            "group_index": topology.atoms["group_index"],
            "component_index": component_indices,
        }
    ).dropna()
    _gc = _adf.groupby("group_index", sort=False)["component_index"].first()
    result = np.full(n_groups, -1, dtype=np.int64)
    result[_gc.index.to_numpy(dtype=np.int64)] = _gc.to_numpy(dtype=np.int64)
    return result


def infer_types(group_names, group_types, component_index_of_groups, n_components):
    from molsysmt.element.component.get_component_type import (
        _get_component_type_from_group_names_and_types,
    )

    output = np.empty(n_components, dtype=object)

    for component_index in range(n_components):
        mask = component_index_of_groups == component_index
        if np.any(mask):
            output[component_index] = _get_component_type_from_group_names_and_types(
                group_names[mask], group_types[mask]
            )
        else:
            output[component_index] = "unknown"

    return output


def infer_names(group_names, component_index_of_groups, component_types):

    output = []
    counters = {"peptide": 0, "protein": 0, "small molecule": 0, "unknown": 0}
    peptides = {}

    for component_index, component_type in enumerate(component_types):
        mask = component_index_of_groups == component_index
        names_in_component = group_names[mask].tolist()

        if component_type == "peptide":
            peptide_key = ",".join(names_in_component)
            if peptide_key in peptides:
                name = peptides[peptide_key]
            else:
                name = f"{component_type} {counters[component_type]}"
                peptides[peptide_key] = name
                counters[component_type] += 1
        elif component_type in ["protein", "small molecule"]:
            name = f"{component_type} {counters[component_type]}"
            counters[component_type] += 1
        elif component_type in ["ion", "lipid"]:
            name = (
                names_in_component[0]
                if names_in_component
                else f"unknown {counters['unknown']}"
            )
        elif component_type == "water":
            name = "water"
        else:
            name = f"unknown {counters['unknown']}"
            counters["unknown"] += 1

        output.append(name)

    return np.array(output, dtype=object)
