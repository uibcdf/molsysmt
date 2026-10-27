"""Applying a typed terminal-H projection with explicit charge-transfer evidence."""

from copy import deepcopy

import numpy as np
import pandas as pd
from depdigest import dep_digest

from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError

CALLER = "molsysmt.build.merge_nonpolar_hydrogens"
REFERENCE = {
    "id": "meeko-terminal-charge-aggregation-reference",
    "type": "software",
    "title": "Meeko terminal-atom charge aggregation",
    "version": "0.8.0",
    "revision": "1eac18bd6d1111f35f9f1abaa8af502c2668d054",
    "url": "https://github.com/forlilab/Meeko/blob/1eac18bd6d1111f35f9f1abaa8af502c2668d054/meeko/molsetup.py",
    "roles": ["reference_implementation"],
}


def fail(reason):
    raise StructuralInconsistencyError(reason=reason, caller=CALLER)


@dep_digest("rdkit")
def _detached_rdkit(source):
    from rdkit import Chem

    return Chem.Mol(source)


def _labels(column):
    """Detach optional labels without inventing string IDs for missing values."""
    return np.asarray(
        [None if pd.isna(value) else str(value) for value in column], dtype=object
    )


def project(
    molecular_system, scheme, selection, structures, chemical_state, report, syntax
):
    from molsysmt import __version__, _ackredit
    from molsysmt._private import autodock_assignment as typing
    from molsysmt._private import partial_charges as charges
    from molsysmt._private.autodock_types import decode_atom_ff_type
    from molsysmt._private.variables import is_all
    from molsysmt.basic import convert, extract, get_form
    from molsysmt.basic._index_validation import validate_structure_indices
    from molsysmt.native import MolSys
    from molsysmt.topology._chemical_graph import (
        chemical_graph_context,
        chemical_graph_digest,
        select_chemical_atoms,
    )

    if scheme != "autodock4":
        raise ArgumentError("typing_scheme", value=scheme, caller=CALLER)
    if get_form(molecular_system) == "rdkit.Mol":
        molecular_system = _detached_rdkit(molecular_system)
    source = (
        molecular_system
        if isinstance(molecular_system, MolSys)
        else convert(molecular_system, to_form="molsysmt.MolSys")
    )
    _, states, state, index, _, _, frames = chemical_graph_context(
        source, chemical_state, structures, False, CALLER
    )
    if states.n_chemical_states != 1 or source.topology is None or not states.n_atoms:
        fail(
            "Hydrogen projection requires one nonempty state and an element inventory."
        )
    typing.validate_assignment(source, scheme)
    charges.validate_assignment(source)
    mechanics = source.molecular_mechanics
    if (
        mechanics is None
        or mechanics.atom_ff_type is None
        or mechanics.partial_charge is None
    ):
        fail(
            "Explicit AutoDock labels and partial charges are required; no defaults are inferred."
        )
    if any(
        value is not None
        for name, value in vars(mechanics).items()
        if name not in {"atoms_ff", "partial_charge_assignment", "atom_type_assignment"}
    ) or set(mechanics.atoms_ff.columns) - {"atom_ff_type", "partial_charge"}:
        fail(
            "Projection supports atom types and partial charges, not other force-field parameters."
        )
    n_atoms = states.n_atoms
    symbols = source.topology.atoms.atom_type.to_numpy()
    labels = np.asarray(mechanics.atom_ff_type)
    try:
        values = np.asarray(mechanics.partial_charge, dtype=float)
        decoded = [decode_atom_ff_type(value, scheme) for value in labels]
    except (ValueError, TypeError) as error:
        fail(f"Invalid explicit types or charges: {error}")
    if (
        values.shape != (n_atoms,)
        or labels.shape != (n_atoms,)
        or not np.isfinite(values).all()
    ):
        fail(
            "Types and finite partial charges must cover the complete source atom axis."
        )
    if not np.array_equal(decoded, symbols):
        fail("AutoDock labels and chemical element symbols disagree.")
    selected = select_chemical_atoms(
        source,
        states,
        index,
        selection,
        frames,
        syntax,
        reference_request=chemical_state in (None, "reference"),
    )
    if not len(selected):
        raise ArgumentError(
            "selection",
            value=selection,
            caller=CALLER,
            message="Select at least one atom.",
        )
    selected_mask = np.zeros(n_atoms, dtype=bool)
    selected_mask[selected] = True
    merged = selected[labels[selected] == "H"]
    neighbors = {int(atom): [] for atom in merged}
    for row in state.bonds.itertuples():
        a, b = int(row.atom1_index), int(row.atom2_index)
        if a in neighbors:
            neighbors[a].append((b, row.bond_type, row.bond_order))
        if b in neighbors:
            neighbors[b].append((a, row.bond_type, row.bond_order))
    pairs = []
    for atom in merged:
        if len(neighbors[atom]) != 1:
            fail(f"Merged H {atom} must have exactly one bonded neighbor.")
        parent, kind, order = neighbors[atom][0]
        if (
            kind != "covalent"
            or pd.isna(order)
            or int(order) != 1
            or symbols[parent] == "H"
            or not selected_mask[parent]
        ):
            fail(
                f"Merged H {atom} needs a retained heavy parent through a declared single bond."
            )
        isotope = source.topology.atoms.loc[atom, "isotope"]
        if pd.notna(isotope) or any(
            pd.isna(state.atom_attributes.loc[atom].get(field, pd.NA))
            or state.atom_attributes.loc[atom, field] != 0
            for field in ("formal_charge", "n_unpaired_electrons")
        ):
            fail(
                "Merging isotope-labelled, charged, radical or unassessed H is unsupported."
            )
        if any(
            pd.notna(value := state.atom_attributes.loc[atom].get(field, pd.NA))
            and value != 0
            for field in ("n_explicit_hydrogens", "n_implicit_hydrogens")
        ):
            fail("Merged H cannot carry additional virtual hydrogen assignments.")
        for field in ("n_explicit_hydrogens", "n_implicit_hydrogens"):
            value = state.atom_attributes.loc[parent].get(field, pd.NA)
            if pd.isna(value) or (field == "n_implicit_hydrogens" and value != 0):
                fail(
                    "Merged parents require known virtual explicit H and zero implicit H; prepare or declare the inventory first."
                )
        pairs.append((int(atom), int(parent)))
    pairs = np.asarray(pairs, dtype=np.int64).reshape(-1, 2)
    retained = selected[labels[selected] != "H"]
    output = extract(source, selection=retained, structure_indices=structures)
    structure_map = validate_structure_indices(source, structures, CALLER)
    if structure_map is None or is_all(structure_map):
        structure_map = np.arange(
            0 if source.structures is None else source.structures.n_structures,
            dtype=np.int64,
        )
    forward = np.full(n_atoms, -1, dtype=np.int64)
    forward[retained] = np.arange(len(retained), dtype=np.int64)
    projected = values[retained].copy()
    transferred = values[merged].copy()
    if len(pairs):
        np.add.at(projected, forward[pairs[:, 1]], transferred)
        attributes = output.chemical_states._states[0].atom_attributes
        explicit = attributes["n_explicit_hydrogens"].copy()
        increments = np.bincount(forward[pairs[:, 1]], minlength=len(retained))
        for atom in np.flatnonzero(increments):
            explicit.loc[atom] = int(explicit.loc[atom]) + int(increments[atom])
        output.topology._set_chemical_state_atom_attribute(
            "n_explicit_hydrogens", explicit
        )
        permission = attributes.get(
            "allows_implicit_hydrogens",
            pd.Series(pd.NA, index=attributes.index, dtype="boolean"),
        ).copy()
        permission.loc[np.flatnonzero(increments)] = False
        output.topology._set_chemical_state_atom_attribute(
            "allows_implicit_hydrogens", permission
        )
        output.interactions = {}
    tolerance = max(
        1e-12, float(8 * np.finfo(float).eps * np.abs(values[selected]).sum())
    )
    if abs(projected.sum() - values[selected].sum()) > tolerance:
        fail("Charge aggregation did not conserve the selected full-precision total.")
    source_charge = deepcopy(mechanics.partial_charge_assignment)
    output.molecular_mechanics.partial_charge = projected
    derived = dict(
        schema="molsysmt.partial_charge_assignment@1",
        method="nonpolar_hydrogen_charge_aggregation",
        engine="MolSysMT",
        chemical_state_index=0,
        chemical_state_id=state.state_id,
        n_atoms=len(retained),
        atom_indices=np.arange(len(retained), dtype=np.int64),
        evaluated_atom_indices=selected.copy(),
        coverage="complete",
        charge_unit="elementary_charge",
        total_charge=float(projected.sum()),
        software={"molsysmt": __version__},
        references=[deepcopy(REFERENCE)],
        attribution=dict(
            schema="molsysmt.scientific_attribution@1",
            target=CALLER,
            items=[deepcopy(REFERENCE)],
        ),
        source_assignment=source_charge,
        parameters={
            "typing_scheme": scheme,
            "merged_label": "H",
            "retained_hydrogen_label": "HD",
            "source_calculation": None
            if source_charge is None
            else {
                key: deepcopy(source_charge[key])
                for key in ("method", "engine", "software", "parameters")
            },
        },
    )
    bound = charges.bind_assignment(output, derived)
    bound.update(status="derived", atom_source_indices=retained.copy())
    output.molecular_mechanics.partial_charge_assignment = bound
    type_report = output.molecular_mechanics.atom_type_assignment
    if type_report is not None:
        original_indices = type_report["atom_source_indices"].copy()
        type_report = typing.bind_assignment(output, type_report)
        type_report.update(
            status="derived",
            atom_source_indices=original_indices,
            hydrogen_policy="nonpolar_H_merged_after_original_typing",
            source_assignment=deepcopy(mechanics.atom_type_assignment),
        )
        output.molecular_mechanics.atom_type_assignment = type_report
    status = np.full(n_atoms, "omitted", dtype="U8")
    status[retained], status[merged] = "retained", "merged"
    result = dict(
        schema="molsysmt.atom_projection@1",
        operation="merge_nonpolar_hydrogens",
        typing_scheme=scheme,
        software={"molsysmt": __version__},
        n_source_atoms=n_atoms,
        n_output_atoms=len(retained),
        source_to_output_atom_indices=forward,
        output_to_source_atom_indices=retained.copy(),
        source_atom_status=status,
        selected_source_atom_indices=selected.copy(),
        omitted_source_atom_indices=np.flatnonzero(~selected_mask),
        merged_source_atom_pairs=pairs,
        charge_transfers=transferred,
        charge_unit="elementary_charge",
        source_total_charge=float(values.sum()),
        selected_total_charge=float(values[selected].sum()),
        output_total_charge=float(projected.sum()),
        charge_conservation_tolerance=tolerance,
        invalidated_interaction_names=list(source.interactions) if len(pairs) else [],
        source_atom_ids=_labels(source.topology.atoms.atom_id),
        source_atom_names=_labels(source.topology.atoms.atom_name),
        output_atom_ids=_labels(output.topology.atoms.atom_id),
        output_atom_names=_labels(output.topology.atoms.atom_name),
        chemical_state_index=index,
        chemical_state_id=state.state_id,
        source_chemical_digest=chemical_graph_digest(source, index),
        source_structure_indices=np.asarray(structure_map, dtype=np.int64).copy(),
        references=[deepcopy(REFERENCE)],
        attribution=dict(
            schema="molsysmt.scientific_attribution@1",
            target=CALLER,
            items=[deepcopy(REFERENCE)],
        ),
        reasons={
            "retained": "selected atom with retained AutoDock label",
            "merged": "terminal neutral H with AutoDock H label; charge transferred to parent",
            "omitted": "outside selection",
        },
    )
    with _ackredit.scope(CALLER) as provider:
        _ackredit.credit(provider, [REFERENCE], CALLER, contextual=True)
    return dict(molecular_system=output, report=result) if report else output
