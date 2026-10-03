"""Inspecting stored chemistry without completing or repairing molecular inputs."""

import numpy as np
import pandas as pd

from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt._private.variables import is_all


def _field(indices, values=None, *, supported=None, conflicts=None, origin=None):
    """Detach coverage and limited validation evidence on an explicit source axis."""
    indices = np.asarray(indices, dtype=np.int64).copy()
    values = (
        np.full(len(indices), None, dtype=object)
        if values is None
        else np.asarray(values, dtype=object).copy()
    )
    missing = pd.isna(values)
    values[missing] = None
    unsupported = np.zeros(len(indices), dtype=bool)
    if supported is not None:
        unsupported = ~missing & ~np.asarray(supported, dtype=bool)
    conflict = (
        np.zeros(len(indices), dtype=bool)
        if conflicts is None
        else np.asarray(conflicts, dtype=bool)
    )
    present = ~missing & ~unsupported & ~conflict
    status = (
        "empty"
        if not len(indices)
        else "conflict"
        if conflict.any()
        else "unsupported"
        if unsupported.any()
        else "missing"
        if missing.all()
        else "partial"
        if missing.any()
        else "present"
    )
    evidence = np.full(len(indices), "unassessed", dtype=object)
    if origin is not None:
        raw = np.asarray(origin, dtype=object)
        for label in ("explicit", "inferred"):
            evidence[np.asarray(pd.Series(raw).eq(label).fillna(False), dtype=bool)] = (
                label
            )
    return {
        "status": status,
        "indices": indices,
        "values": values,
        "present_indices": indices[present],
        "missing_indices": indices[missing],
        "unsupported_indices": indices[unsupported],
        "conflict_indices": indices[conflict],
        "origin": evidence,
    }


def _column(table, name, indices):
    return (
        None
        if table is None or name not in table
        else table[name].iloc[indices].to_numpy(dtype=object)
    )


def _frame(molecular_system, structure_indices, caller):
    from molsysmt._private.h5msm import modular_h5msm_dimensions
    from molsysmt.basic._index_validation import _get_count, validate_structure_indices

    dimensions = modular_h5msm_dimensions(molecular_system)
    count = (
        dimensions[1]
        if dimensions is not None
        else (_get_count(molecular_system, "structure") or 0)
    )
    if dimensions is None:
        validated = validate_structure_indices(
            molecular_system, structure_indices, caller
        )
    elif structure_indices is None or is_all(structure_indices):
        validated = structure_indices
    else:
        validated = np.asarray(structure_indices)
        if validated.ndim == 0:
            validated = validated.reshape(1)
        if (
            validated.ndim != 1
            or (validated.size and validated.dtype.kind not in "iu")
            or np.any(validated < 0)
            or np.any(validated >= count)
        ):
            raise ArgumentError(
                "structure_indices", value=structure_indices, caller=caller
            )
    if (validated is None or is_all(validated)) and count > 1:
        raise ArgumentError(
            "structure_indices",
            value=structure_indices,
            caller=caller,
            message="Chemical readiness assessment needs exactly one selected structure when structures are available.",
        )
    frames = (
        np.arange(count, dtype=np.int64)
        if validated is None or is_all(validated)
        else np.unique(np.asarray(validated, dtype=np.int64))
    )
    if len(frames) > 1 or (count and not len(frames)):
        raise ArgumentError(
            "structure_indices",
            value=structure_indices,
            caller=caller,
            message="Chemical readiness assessment needs exactly one selected structure when structures are available.",
        )
    return None if not len(frames) else int(frames[0])


def _domains(molecular_system, caller):
    """Get native chemical storage; keep coordinate access on the original source."""
    from molsysmt._private.h5msm import modular_h5msm_dimensions
    from molsysmt.basic import convert, get_form
    from molsysmt.native import ChemicalStates, MolSys, Structures, Topology

    source = molecular_system
    form = get_form(source)
    dimensions = modular_h5msm_dimensions(source)
    links = None
    if dimensions is not None:
        from molsysmt.h5msm import read_layers

        payload = read_layers(
            source, layers=["topology", "chemical_states", "associations"]
        )
        topology, states, links = (
            payload["topology"],
            payload["chemical_states"],
            payload["associations"] or [],
        )
        required = []
        if topology is not None and states is not None:
            required.append(("chemical_states", "topology"))
        target = (
            "topology"
            if topology is not None
            else "chemical_states"
            if states is not None
            else None
        )
        if dimensions[1] and target is not None:
            required.append(("structures", target))
        for left, right in required:
            if not any(
                link["axis"] == "atom"
                and link["source"] == left
                and link["target"] == right
                and isinstance(link["indices"], str)
                and link["indices"] == "identity"
                for link in links
            ):
                raise StructuralInconsistencyError(
                    reason="Chemical readiness requires declared identity atom-axis links; remap independent H5MSM layers before combining their fields.",
                    caller=caller,
                )
        return source, topology, states, dimensions[0], links
    if isinstance(form, (list, tuple)):
        source = convert(source, to_form="molsysmt.MolSys")
    elif form == "molsysmt.ChemicalStatesDict":
        source = convert(source, to_form="molsysmt.ChemicalStates")
    elif form == "molsysmt.StructuresDict":
        source = convert(source, to_form="molsysmt.Structures")
    if isinstance(source, MolSys):
        return (
            source,
            source.topology,
            source.chemical_states,
            source.get_n_atoms(),
            links,
        )
    if isinstance(source, ChemicalStates):
        return source, None, source, source.n_atoms, links
    if isinstance(source, Structures):
        return source, None, None, source.n_atoms, links
    topology = (
        source
        if isinstance(source, Topology)
        else convert(source, to_form="molsysmt.Topology")
    )
    return topology, topology, topology._chemical_states_domain, topology.n_atoms, links


def _state(source, states, requested, frame, links, caller):
    if states is None or not states.n_chemical_states:
        if isinstance(requested, int):
            raise ArgumentError("chemical_state", value=requested, caller=caller)
        return None, None, "unavailable"
    if requested == "structure":
        if frame is None:
            return None, None, "unassociated"
        if links is not None:
            association = next(
                (
                    link
                    for link in links
                    if link["axis"] == "structure_state"
                    and link["source"] == "structures"
                    and link["target"] == "chemical_states"
                ),
                None,
            )
            value = (
                (0 if states.n_chemical_states == 1 else -1)
                if association is None
                else frame
                if isinstance(association["indices"], str)
                else association["indices"][frame]
            )
        else:
            from molsysmt.native import MolSys

            if not isinstance(source, MolSys):
                if states.n_chemical_states != 1:
                    return None, None, "unassociated"
                value = 0
            else:
                value = source._get_structure_chemical_state_indices(
                    structure_indices=[frame], resolved=True
                )[0]
        if pd.isna(value) or value < 0:
            return None, None, "unassociated"
        index = states._resolve_index(int(value))
    elif requested == "reference":
        if states.reference_chemical_state_index is None:
            return None, None, "ambiguous"
        index = states._resolve_index()
    else:
        index = states._resolve_index(requested)
    return states._states[index], index, "resolved"


def assess(
    molecular_system, selection, structure_indices, chemical_state, syntax, caller
):
    from molsysmt import __version__
    from molsysmt import pyunitwizard as puw
    from molsysmt.basic import get, get_form, has_attribute, select
    from molsysmt.element.atom import is_atom_type

    frame = _frame(molecular_system, structure_indices, caller)
    source, topology, states, n_atoms, links = _domains(molecular_system, caller)
    if n_atoms is None or n_atoms < 0:
        raise StructuralInconsistencyError(
            reason="Chemical readiness requires a declared atom-index domain.",
            caller=caller,
        )
    state, state_index, state_status = _state(
        source, states, chemical_state, frame, links, caller
    )
    if selection is None or is_all(selection):
        atoms = np.arange(n_atoms, dtype=np.int64)
    elif not isinstance(selection, str):
        raw = np.asarray(selection)
        if (
            raw.ndim != 1
            or (raw.size and raw.dtype.kind not in "iu")
            or np.any(raw < 0)
            or np.any(raw >= n_atoms)
        ):
            raise ArgumentError("selection", value=selection, caller=caller)
        atoms = np.unique(raw).astype(np.int64)
    else:
        # Rich syntax uses the established public resolver, including spatial
        # and state-dependent selection semantics; numeric scopes need no view.
        selection_state = (
            "reference"
            if state_index is None
            or (
                source is not molecular_system
                and links is None
                and state_index == states.reference_chemical_state_index
            )
            else state_index
        )
        atoms = np.unique(
            select(
                molecular_system,
                selection=selection,
                structure_indices="all" if frame is None else [frame],
                chemical_state=selection_state,
                syntax=syntax,
            )
        ).astype(np.int64)
    atom_table = None if topology is None else topology.atoms
    atom_types = _column(atom_table, "atom_type", atoms)
    if atom_types is not None:
        atom_types = (
            pd.Series(atom_types)
            .replace(["nan", "None", "<NA>", ""], None)
            .to_numpy(dtype=object)
        )
    fields = {
        "atom_type": _field(
            atoms,
            atom_types,
            supported=None
            if atom_types is None
            else is_atom_type(
                [value if isinstance(value, str) else "" for value in atom_types]
            ),
        )
    }
    for name in ("atom_id", "isotope"):
        values = _column(atom_table, name, atoms)
        conflicts = None
        if name == "atom_id" and values is not None:
            conflicts = atom_table[name].duplicated(keep=False).iloc[
                atoms
            ].to_numpy() & ~pd.isna(values)
        fields[name] = _field(atoms, values, conflicts=conflicts)
    atom_chemistry = None if state is None else state.atom_attributes
    for name in (
        "formal_charge",
        "is_aromatic",
        "n_unpaired_electrons",
        "n_implicit_hydrogens",
        "n_explicit_hydrogens",
        "allows_implicit_hydrogens",
        "stereochemistry",
    ):
        key = (
            "atom_is_aromatic"
            if name == "is_aromatic"
            else "atom_stereochemistry"
            if name == "stereochemistry"
            else name
        )
        values = _column(atom_chemistry, name, atoms)
        supported = (
            None
            if name != "stereochemistry" or values is None
            else pd.Series(values).isin(["R", "S", "r", "s", "unspecified"]).to_numpy()
        )
        fields[key] = _field(atoms, values, supported=supported)
    bonds = None if state is None else state.bonds
    all_bonds = np.arange(0 if bonds is None else len(bonds), dtype=np.int64)
    pairs = (
        np.empty((0, 2), dtype=np.int64)
        if not len(all_bonds)
        else bonds[["atom1_index", "atom2_index"]].to_numpy(dtype=np.int64, na_value=-1)
    )
    valid = (
        (pairs >= 0).all(axis=1)
        & (pairs < n_atoms).all(axis=1)
        & (pairs[:, 0] != pairs[:, 1])
    )
    duplicate = np.asarray(pd.DataFrame(np.sort(pairs, axis=1)).duplicated(keep=False))
    incident = np.isin(pairs, atoms).any(axis=1)
    bond_indices = all_bonds[incident]
    origin = _column(bonds, "evidence", bond_indices)
    for name in (
        "bond_id",
        "bond_type",
        "bond_order",
        "is_aromatic",
        "stereochemistry",
    ):
        key = (
            "bond_is_aromatic"
            if name == "is_aromatic"
            else "bond_stereochemistry"
            if name == "stereochemistry"
            else name
        )
        values = _column(bonds, name, bond_indices)
        supported = None
        if values is not None and name in ("bond_type", "stereochemistry"):
            choices = (
                ["covalent", "dative"]
                if name == "bond_type"
                else ["E", "Z", "cis", "trans", "unspecified"]
            )
            supported = pd.Series(values).isin(choices).to_numpy()
        fields[key] = _field(
            bond_indices,
            values,
            supported=supported,
            origin=origin if name == "bond_type" else None,
        )
    relationships = _column(bonds, "bond_type", bond_indices)
    if relationships is not None:
        covalent = (
            pd.Series(relationships).eq("covalent").fillna(False).to_numpy(dtype=bool)
        )
    else:
        covalent = np.zeros(len(bond_indices), dtype=bool)
    covalent_indices = bond_indices[covalent]
    order = _column(bonds, "bond_order", covalent_indices)
    aromatic = _column(bonds, "is_aromatic", covalent_indices)
    effective = (
        np.full(len(covalent_indices), None, dtype=object)
        if order is None
        else order.copy()
    )
    if aromatic is not None:
        effective[
            np.asarray(pd.Series(aromatic).eq(True).fillna(False), dtype=bool)
        ] = "aromatic"
    fields["covalent_multiplicity"] = _field(
        covalent_indices,
        effective,
        supported=pd.Series(effective).isin([1, 2, 3, "aromatic"]).to_numpy(),
    )
    coordinate_values = None
    coordinates = None
    if frame is not None:
        if links is not None:
            from molsysmt.form.file_h5msm.iterators import StructuresIterator

            # Reuse the form's bounded series reader, also used by ChunkedExecutor.
            with StructuresIterator(
                molecular_system,
                atom_indices=atoms,
                structure_indices=[frame],
                coordinates=True,
            ) as iterator:
                coordinates = next(iterator)
        elif has_attribute(molecular_system, "coordinates"):
            coordinates = get(
                molecular_system,
                element="atom",
                selection=atoms.tolist(),
                structure_indices=[frame],
                coordinates=True,
            )
    if coordinates is not None:
        values = puw.get_value(coordinates, to_unit="nm")
        if values.shape != (1, len(atoms), 3):
            raise StructuralInconsistencyError(
                reason="Coordinate shape differs from the assessed atom/frame domain.",
                caller=caller,
            )
        coordinate_values = np.isfinite(values[0]).all(axis=1)
    fields["coordinates"] = _field(
        atoms,
        coordinate_values,
        conflicts=None if coordinate_values is None else ~coordinate_values,
    )
    fields["coordinates"]["unit"] = "nm"
    fields["formal_charge"]["unit"] = "elementary_charge"
    return {
        "schema": "molsysmt.chemical_readiness@1",
        "method": "stored_field_audit",
        "rule_version": 1,
        "source_forms": get_form(molecular_system),
        "n_atoms": int(n_atoms),
        "atom_indices": atoms,
        "bond_indices": bond_indices,
        "bonded_atom_pairs": pairs[incident].copy(),
        "structure_index": frame,
        "chemical_state_index": state_index,
        "chemical_state_status": state_status,
        "state_provenance_index": None if state is None else state.provenance_index,
        "fields": fields,
        "connectivity": {
            "declared_completeness": "unavailable"
            if state is None
            else state.connectivity_completeness,
            "examined_bond_indices": all_bonds,
            "invalid_bond_indices": all_bonds[~valid | duplicate],
            "crossing_bond_indices": bond_indices[
                ~np.isin(pairs[incident], atoms).all(axis=1)
            ],
            "evidence": np.full(len(bond_indices), None, dtype=object)
            if origin is None
            else _field(bond_indices, origin)["values"],
        },
        "explicit_hydrogen_atom_indices": np.empty(0, dtype=np.int64)
        if atom_types is None
        else atoms[np.asarray(pd.Series(atom_types).eq("H").fillna(False), dtype=bool)],
        "unassessed_checks": [
            "valence",
            "protonation",
            "missing_hydrogen_inventory",
            "aromaticity_perception",
            "stereogenicity",
            "periodic_geometry",
            "conformer_quality",
            "charge_model",
            "docking_readiness",
            "property_origin",
        ],
        "software": {"molsysmt": __version__},
    }
