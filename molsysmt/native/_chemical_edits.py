"""Stage selected-state graph edits independently of Topology chemistry."""

import numpy as np
import pandas as pd

from molsysmt._private.smonitor import StructuralInconsistencyError

from ._chemical_components import (
    group_components,
    indices_from_bonds,
    infer_names,
    infer_types,
    unchanged_rows,
)
from ._chemical_state import Components_DataFrame


def context(topology, n_atoms):
    """Validate an explicitly supplied stable context without reading chemistry."""
    if topology is not None and topology.n_atoms != n_atoms:
        raise StructuralInconsistencyError(
            reason="Component reconstruction requires topology on the same atom domain.",
            caller="molsysmt.native.ChemicalStates.rebuild_components",
        )
    return topology


def rebuild(
    state,
    n_atoms,
    bonds,
    *,
    redefine_indices=True,
    redefine_ids=True,
    redefine_types=True,
    redefine_names=True,
    force=False,
    topology=None,
    require_valid_membership=False,
):
    """Prepare a component replacement using the admitted stored-graph rules."""
    reconstruct = (
        redefine_indices
        or force
        or ((redefine_types or redefine_names) and state.component_indices.isna().any())
    )
    state._validate_atom_domain(
        n_atoms, check_component_indices=require_valid_membership or not reconstruct
    )
    if reconstruct:
        indices = indices_from_bonds(n_atoms, bonds)
        count = int(indices.max()) + 1 if len(indices) else 0
        components = Components_DataFrame(n_components=count)
        preserved = [
            name
            for name, replace in (
                ("component_id", redefine_ids),
                ("component_type", redefine_types),
                ("component_name", redefine_names),
            )
            if not replace
        ]
        if preserved:
            old = state.component_indices.to_numpy(dtype=np.int64, na_value=-1)
            new_rows, old_rows = unchanged_rows(
                old, indices, len(state.components), count
            )
            for name in preserved:
                components[name] = pd.array(
                    [pd.NA] * count, dtype=state.components[name].dtype
                )
                components.loc[new_rows, name] = (
                    state.components[name].iloc[old_rows].to_numpy()
                )
        membership = pd.Series(indices, dtype="Int64")
    else:
        components = Components_DataFrame(n_components=len(state.components))
        for name in state.components:
            components[name] = state.components[name].copy(deep=True)
        membership = state.component_indices
        count = len(components)

    if redefine_ids:
        components["component_id"] = pd.array(
            np.arange(count).astype(str), dtype="string"
        )
    if redefine_types or redefine_names:
        if topology is None or not topology.n_groups:
            for name, replace in (
                ("component_type", redefine_types),
                ("component_name", redefine_names),
            ):
                if replace:
                    components[name] = pd.array([pd.NA] * count, dtype="string")
        else:
            # Group recognition is stable-inventory inference. It returns values
            # without rebuilding or mutating the supplied Topology.
            group_types = topology.groups["group_type"].to_numpy(dtype=object)
            if topology.groups["group_type"].isna().any():
                from ._topology_infer import infer_group_types_from_topology

                group_types = infer_group_types_from_topology(topology)
            groups = group_components(topology, membership)
            group_names = topology.groups["group_name"].to_numpy(dtype=object)
            if redefine_types:
                values = infer_types(group_names, group_types, groups, count)
                values[np.asarray(values == "unknown")] = pd.NA
                components["component_type"] = values
            if redefine_names:
                types = (
                    components["component_type"]
                    .fillna("unknown")
                    .to_numpy(dtype=object)
                )
                values = infer_names(group_names, groups, types)
                represented = np.zeros(count, dtype=bool)
                represented[groups[groups >= 0]] = True
                supported = np.isin(
                    types,
                    ["peptide", "protein", "small molecule", "ion", "lipid", "water"],
                )
                values[~represented | ~supported] = pd.NA
                components["component_name"] = values

    components["component_id"] = components["component_id"].astype("string")
    changes = {"components": components}
    if reconstruct:
        complete = state.connectivity_completeness == "complete" and (
            not len(bonds)
            or "joins_components" in bonds
            and not bonds.joins_components.isna().any()
        )
        changes.update(
            component_indices=membership,
            _component_completeness="complete" if complete else "partial",
            _component_evidence="inferred",
        )
    return changes


def scientific_change(state, changes):
    """Ignore presentation IDs/names when deciding occurrence invalidation."""
    if "bonds" in changes:
        left, right = state.bonds, changes["bonds"]
        columns = tuple(name for name in right if name != "bond_id")
        if columns != tuple(name for name in left if name != "bond_id") or any(
            not left[name].equals(right[name]) for name in columns
        ):
            return True
    if "component_indices" in changes and not state.component_indices.equals(
        changes["component_indices"]
    ):
        return True
    return any(
        name in changes and changes[name] != getattr(state, name)
        for name in ("_connectivity_completeness", "_component_completeness")
    )
