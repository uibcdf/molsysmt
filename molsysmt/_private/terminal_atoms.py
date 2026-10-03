"""Attaching declared terminal atoms while retaining native domain ownership."""

from copy import deepcopy

import numpy as np
import pandas as pd

from molsysmt._private.smonitor import (
    StructuralAttributeDropWarning,
    StructuralInconsistencyError,
    warn,
)


def attach(source, records, coordinates, attribute_policy, caller):
    from molsysmt import pyunitwizard as puw
    from molsysmt.element.atom import is_atom_type
    from molsysmt.native import MolecularMechanics, MolSys
    from molsysmt.native.molsys import _extend_interaction_atoms
    from molsysmt.native.structures import (
        _ATOM_ALIGNED_ATTRIBUTES,
        _SYSTEM_LEVEL_OBSERVABLES,
    )

    def fail(reason):
        raise StructuralInconsistencyError(reason=reason, caller=caller)

    if (
        source.topology is None
        or source.chemical_states is None
        or source.structures is None
    ):
        fail("Terminal attachment requires topology, chemical states and structures.")
    if source.chemical_states.n_chemical_states != 1:
        fail(
            "Terminal attachment requires exactly one chemical state; extract it explicitly first."
        )
    original = source.structures.coordinates
    if original is None:
        fail("Terminal attachment requires coordinates for every existing atom.")
    n_atoms, n_new = source.get_n_atoms(), len(records)
    if coordinates is None:
        fail("Terminal attachment requires a length quantity for the new coordinates.")
    positions = np.asarray(puw.get_value(coordinates, to_unit="nm"), dtype=np.float64)
    original_values = puw.get_value(original, to_unit="nm")
    if (
        positions.shape != (source.structures.n_structures, n_new, 3)
        or not np.isfinite(positions).all()
    ):
        fail(
            "New coordinates must be finite and aligned to all source frames and declared atoms."
        )
    if not np.isfinite(original_values).all():
        fail("Existing coordinates must be finite.")
    if any(record["parent_atom_index"] >= n_atoms for record in records):
        fail("A terminal parent index is outside the existing atom domain.")
    if not np.all(is_atom_type([record["atom_type"] for record in records])):
        fail("Terminal atom_type must be a supported chemical element symbol.")
    if not n_new:
        return {
            "molecular_system": source.copy(),
            "report": dict(
                schema="molsysmt.terminal_attachment@1",
                status="unchanged",
                atom_correspondence=np.column_stack(
                    (np.arange(n_atoms), np.arange(n_atoms))
                ).astype(np.int64),
                parent_atom_pairs=np.empty((0, 2), dtype=np.int64),
                generated_atom_ids=[],
                coordinate_unit="nm",
                dropped_attributes=[],
                invalidated_interactions=[],
            ),
        }
    dropped = [
        name
        for name in _ATOM_ALIGNED_ATTRIBUTES + _SYSTEM_LEVEL_OBSERVABLES
        if name != "coordinates" and getattr(source.structures, name) is not None
    ]
    mechanics = source.molecular_mechanics
    if mechanics is not None and mechanics.atoms_ff is not None:
        dropped.append("atoms_ff")
    if dropped and attribute_policy == "strict":
        fail(
            "Atom-domain expansion cannot retain these attributes without supplied values: "
            + ", ".join(dropped)
        )
    topology = source.topology.copy()
    state = topology._chemical_states_domain._states[0]
    used_ids = set(topology.atoms["atom_id"].dropna().astype(str))
    next_id = n_atoms
    component_indices = list(state.component_indices)
    added_components = []
    new_rows, attrs, parent_pairs, ids = [], [], [], []
    for k, record in enumerate(records):
        parent = record["parent_atom_index"]
        row = {field: pd.NA for field in topology.atoms.columns}
        for field in ("group_index", "chain_index"):
            row[field] = topology.atoms.at[parent, field]
        identifier = record.get("atom_id")
        if identifier is None:
            while str(next_id) in used_ids:
                next_id += 1
            identifier = str(next_id)
            next_id += 1
        identifier = str(identifier)
        if identifier in used_ids:
            fail("A declared new atom_id collides with an existing or added atom_id.")
        used_ids.add(identifier)
        ids.append(identifier)
        row.update(
            atom_id=identifier,
            atom_type=record["atom_type"],
            atom_name=str(
                record.get("atom_name", f"{record['atom_type']}{n_atoms + k}")
            ),
        )
        if "isotope" in record:
            row["isotope"] = record["isotope"]
        new_rows.append(row)
        attrs.append(record.get("chemical_attributes", {}))
        added_components.append(component_indices[parent])
        parent_pairs.append((parent, n_atoms + k))
    new_table = pd.DataFrame(new_rows)
    if "isotope" in new_table and "isotope" not in topology.atoms:
        topology.atoms["isotope"] = pd.array([pd.NA] * n_atoms, dtype="UInt16")
    for name, dtype in topology.atoms.dtypes.items():
        new_table[name] = new_table[name].astype(dtype)
    topology.atoms = pd.concat([topology.atoms, new_table], ignore_index=True)
    topology._coerce_id_columns_to_string()
    for field in ("group_index", "chain_index"):
        topology.atoms[field] = topology.atoms[field].astype("Int64")
    fields = set(state.atom_attributes).union(*(set(record) for record in attrs))
    state.atom_attributes = pd.DataFrame(
        {
            name: (
                list(state.atom_attributes[name])
                if name in state.atom_attributes
                else [pd.NA] * n_atoms
            )
            + [record.get(name, pd.NA) for record in attrs]
            for name in fields
        },
        index=range(n_atoms + n_new),
    )
    state.component_indices = pd.Series(
        pd.array(component_indices + added_components, dtype="Int64")
    )
    state._ensure_compatibility(n_atoms + n_new)
    topology._chemical_states_domain._resize_atom_domain(n_atoms + n_new)
    topology._append_chemical_state_bonds(
        parent_pairs,
        bond_order=[record.get("bond_order", 1) for record in records],
        bond_type=["covalent"] * n_new,
        is_aromatic=[False] * n_new,
        joins_components=[True] * n_new,
        evidence=["explicit"] * n_new,
    )
    structures = source.structures.copy()
    structures.coordinates = puw.quantity(
        np.concatenate((original_values, positions), axis=1), "nm"
    )
    for name in dropped:
        if name != "atoms_ff":
            setattr(structures, name, None)
    analyses = {}
    for name, result in source.interactions.items():
        invalidated = result.invalidate_structures(
            np.arange(result.n_structures, dtype=np.int64)
        )
        analyses[name] = _extend_interaction_atoms(invalidated, n_atoms + n_new)
    output = MolSys._from_partial_domains(
        topology=topology,
        chemical_states=topology._chemical_states_domain,
        structures=structures,
        interactions=analyses,
    )
    links = source._structure_chemical_state_indices
    output._structure_chemical_state_indices = None if links is None else links.copy()
    output.molecular_mechanics = (
        MolecularMechanics()
        if "atoms_ff" in dropped
        else None
        if mechanics is None
        else mechanics.copy()
    )
    report = dict(
        schema="molsysmt.terminal_attachment@1",
        status="attached",
        atom_correspondence=np.column_stack(
            (np.arange(n_atoms), np.arange(n_atoms))
        ).astype(np.int64),
        parent_atom_pairs=np.asarray(parent_pairs, dtype=np.int64).reshape(-1, 2),
        generated_atom_ids=ids,
        coordinate_unit="nm",
        dropped_attributes=dropped,
        invalidated_interactions=list(analyses),
    )
    if dropped:
        warn(StructuralAttributeDropWarning(attributes=dropped, caller=caller))
    return {"molecular_system": output, "report": deepcopy(report)}
