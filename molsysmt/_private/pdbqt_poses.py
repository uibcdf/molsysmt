"""Validating declared pose axes without perceiving chemistry from docking output."""

from copy import deepcopy
from pathlib import Path

import numpy as np

from molsysmt._private.pdbqt import PREFIX, fail, parse
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.variables import is_all

CALLER = "molsysmt.form.file_pdbqt.read_poses"
_TREE_ARRAYS = (
    "atom_ids",
    "fragment_atom_indices",
    "fragment_offsets",
    "branch_atom_pairs",
    "branch_fragment_pairs",
)


def models(payload):
    """Yield balanced model bodies, preserving labels separately from positions."""
    from molsysmt._private.pdbqt_document import model_spans

    for label, start, stop, prefix in model_spans(payload):
        yield label, parse(prefix + payload[start:stop])


def integer_axis(value, name, size):
    array = np.asarray(value)
    if (
        array.shape != (size,)
        or array.dtype.kind not in "iu"
        or (array.size and np.any(array > np.iinfo(np.int64).max))
    ):
        fail(f"atom_map requires a typed integer {name} axis of length {size}.")
    return array.astype(np.int64, copy=False)


def validate_map(source, state_index, mapping):
    """Check both map directions and their chemical/label bindings before use."""
    from molsysmt.chemical_states._chemical_graph import chemical_graph_digest

    if not isinstance(mapping, dict) or (
        mapping.get("schema") != "molsysmt.atom_export@1"
        or mapping.get("target_form") != "file:pdbqt"
        or mapping.get("typing_scheme") != "autodock4"
    ):
        fail("atom_map must be a completed AutoDock4 PDBQT atom-export report.")
    n_source = source.topology.n_atoms
    n_written = mapping.get("n_output_atoms")
    if (
        type(mapping.get("n_source_atoms")) is not int
        or mapping["n_source_atoms"] != n_source
        or type(n_written) is not int
        or not 0 < n_written <= n_source
    ):
        fail("atom_map atom counts disagree with the known source.")
    inverse = integer_axis(
        mapping.get("output_to_source_atom_indices"),
        "output_to_source_atom_indices",
        n_written,
    )
    forward = integer_axis(
        mapping.get("source_to_output_atom_indices"),
        "source_to_output_atom_indices",
        n_source,
    )
    if (
        np.any(inverse < 0)
        or np.any(inverse >= n_source)
        or len(np.unique(inverse)) != n_written
    ):
        fail("atom_map output-to-source indices must be unique and in bounds.")
    expected = np.full(n_source, -1, dtype=np.int64)
    expected[inverse] = np.arange(n_written)
    if not np.array_equal(forward, expected):
        fail("atom_map directions are not inverse retained-atom correspondences.")
    if (
        mapping.get("chemical_state_index") != state_index
        or mapping.get("chemical_state_id")
        != source.chemical_states._states[state_index].state_id
        or mapping.get("source_chemical_digest")
        != chemical_graph_digest(source, state_index)
    ):
        fail("atom_map chemical-state binding disagrees with the known source.")
    for field, column in (
        ("source_atom_ids", "atom_id"),
        ("source_atom_names", "atom_name"),
        ("source_atom_types", "atom_type"),
    ):
        stored = np.asarray(mapping.get(field), dtype=object)
        values = source.topology.atoms[column]
        current = values.astype(object).where(values.notna(), None).to_numpy()
        if stored.shape != (n_source,) or not np.array_equal(stored, current):
            fail(f"atom_map {field} does not match the known source axis.")
    # The completed writer map declares a presentation axis separately from
    # the chemically bound source axis. Poses must match that written axis.
    from molsysmt._private.pdbqt_presentation import prepare

    for field in ("output_atom_ids", "output_atom_names"):
        values = np.asarray(mapping.get(field), dtype=object)
        if values.shape != (n_written,) or any(not isinstance(v, str) for v in values):
            fail(f"atom_map {field} requires a string written axis.")
    prepare(
        {
            "atom_serials": mapping["output_atom_ids"],
            "atom_names": mapping["output_atom_names"],
        },
        n_written,
        np.arange(n_written),
    )
    charges = np.asarray(mapping.get("written_partial_charge"))
    if (
        mapping.get("charge_unit") != "elementary_charge"
        or charges.shape != (n_written,)
        or charges.dtype.kind not in "fiu"
        or not np.isfinite(charges).all()
    ):
        fail("atom_map requires finite written_partial_charge in elementary_charge.")
    if mapping.get("torsion_tree") is None:
        fail("Pose reading requires an exported ligand ROOT/BRANCH tree.")
    return inverse, forward, charges


def validate_model(record, mapping, inverse, charges, source, baseline):
    atoms = record["atoms"]
    if len(atoms) != len(inverse):
        fail("PDBQT pose atom count disagrees with atom_map.")
    for field, key, expected in (
        ("serial IDs", "serial", mapping["output_atom_ids"]),
        ("atom names", "atom_name", mapping["output_atom_names"]),
        ("elements", "element", source.topology.atoms.atom_type.to_numpy()[inverse]),
    ):
        actual = [str(atom[key]) for atom in atoms]
        if not np.array_equal(actual, expected):
            fail(f"PDBQT pose {field} disagree with the declared written axis.")
    if not np.allclose(
        [a["partial_charge"] for a in atoms], charges, rtol=0, atol=1e-12
    ):
        fail("PDBQT pose charges disagree with the exported written charges.")
    labels = np.asarray([a["atom_ff_type"] for a in atoms])
    expected_labels = mapping.get("output_atom_ff_types")
    if expected_labels is None and source.molecular_mechanics.atom_ff_type is not None:
        expected_labels = np.asarray(source.molecular_mechanics.atom_ff_type)[inverse]
    if expected_labels is not None and not np.array_equal(labels, expected_labels):
        fail("PDBQT pose AutoDock types disagree with the declared export/source.")
    # Metadata may not silently change identity between poses, even when absent
    # from the export map. Geometry and opaque REMARKs are the variable fields.
    identity = [
        tuple(
            atom[key]
            for key in (
                "serial",
                "atom_name",
                "element",
                "group_name",
                "chain_id",
                "group_id",
                "record",
                "atom_ff_type",
            )
        )
        for atom in atoms
    ]
    if baseline is not None and identity != baseline:
        fail("PDBQT pose atom identity/type fields change between structures.")
    tree = record["torsion_tree"]
    expected_tree = mapping["torsion_tree"]
    if not isinstance(expected_tree, dict) or tree is None:
        fail("PDBQT pose is missing the declared ligand torsion tree.")
    for field in (*_TREE_ARRAYS, "schema_version", "root_fragment_index", "torsdof"):
        expected_value = np.asarray(expected_tree.get(field))
        if field in {
            "branch_atom_pairs",
            "branch_fragment_pairs",
        } and expected_value.shape == (0,):
            expected_value = expected_value.reshape(0, 2)
        if field not in expected_tree or not np.array_equal(
            tree[field], expected_value
        ):
            fail(f"PDBQT pose torsion tree disagrees with atom_map field {field}.")
    return identity, labels


def read_poses(item, molecular_system, atom_map, structures, missing_atoms, report):
    import hashlib

    from molsysmt import __version__
    from molsysmt import pyunitwizard as puw
    from molsysmt._private.argdigest.argument._correspondence_axes import flat_axis
    from molsysmt.basic import get_form
    from molsysmt.chemical_states._chemical_graph import (
        chemical_graph_context,
        detached_chemical_graph_view,
    )
    from molsysmt.native import Structures

    if missing_atoms not in ("error", "omit"):
        raise ArgumentError("missing_atoms", value=missing_atoms, caller=CALLER)
    form = get_form(item)
    if form not in {"file:pdbqt", "string:pdbqt_text", "molsysmt.PDBQTFileHandler"}:
        raise ArgumentError("item", value=item, caller=CALLER)
    if form == "molsysmt.PDBQTFileHandler":
        item._require_open()
    payload = (
        item._document.payload
        if form == "molsysmt.PDBQTFileHandler"
        else item[len(PREFIX) :]
        if form == "string:pdbqt_text"
        else Path(item).read_bytes().decode("utf-8")
    )
    source, states, _, state_index, _, _, _ = chemical_graph_context(
        molecular_system, "reference", "all", False, CALLER
    )
    if states.n_chemical_states != 1:
        fail("Pose reading requires one known source chemical state.")
    # The general chemistry view copies inventory/state only, never a source
    # trajectory, periodic boxes or analyses calculated on old coordinates.
    view = detached_chemical_graph_view(source, states, state_index, CALLER)
    inverse, forward, charges = validate_map(view, state_index, atom_map)
    omitted = np.flatnonzero(forward < 0)
    if len(omitted) and missing_atoms == "error":
        fail(
            "Export omitted source atoms; use missing_atoms='omit' for the retained subsystem. No missing H coordinates are recovered."
        )
    # Read optional source labels without copying or attaching its mechanics.
    if getattr(source, "molecular_mechanics", None) is not None:
        view.molecular_mechanics = source.molecular_mechanics
    retained = np.sort(inverse)
    written_to_output = np.searchsorted(retained, inverse)
    selection = flat_axis(structures, "structure_indices", CALLER)
    requested = (
        None if selection is None or is_all(selection) else set(selection.tolist())
    )
    coordinates, labels, remarks, chosen_indices = [], [], [], []
    baseline = None
    n_models = 0
    written_types = None
    for index, (label, record) in enumerate(models(payload)):
        baseline, written_types = validate_model(
            record, atom_map, inverse, charges, view, baseline
        )
        n_models = index + 1
        if requested is None or index in requested:
            xyz = np.empty((len(inverse), 3), dtype=np.float64)
            xyz[written_to_output] = [atom["coordinates"] for atom in record["atoms"]]
            coordinates.append(xyz)
            labels.append(label)
            remarks.append(record["remarks"])
            chosen_indices.append(index)
    if requested is not None and any(index >= n_models for index in requested):
        raise ArgumentError("structure_indices", value=structures, caller=CALLER)
    # Selection order/repetitions affect the new structure axis, not MODEL IDs.
    selected = np.arange(n_models, dtype=np.int64) if requested is None else selection
    lookup = {value: index for index, value in enumerate(chosen_indices)}
    order = [lookup[int(index)] for index in selected]
    xyz = np.asarray([coordinates[index] for index in order], dtype=np.float64).reshape(
        -1, len(inverse), 3
    )
    selected_labels = [labels[index] for index in order]
    # Detach only chemical domains via their normal extraction path. No rounded
    # PDBQT charge is relabelled as a source force-field calculation.
    from molsysmt.native import MolecularMechanics

    view.molecular_mechanics = MolecularMechanics()
    output = view.extract(atom_indices=retained)
    output.structures = Structures(
        coordinates=puw.quantity(xyz, "angstrom"),
        structure_id=None
        if all(label is None for label in selected_labels)
        else np.asarray(selected_labels, dtype=object),
    )
    output._set_structure_chemical_state_indices(np.full(len(selected), state_index))
    if not report:
        return output
    source_to_output = np.full(len(forward), -1, dtype=np.int64)
    source_to_output[retained] = np.arange(len(retained))
    result = dict(
        schema="molsysmt.pdbqt_pose_read@1",
        software={"molsysmt": __version__},
        input_form=form,
        input_payload_sha256=hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        export_map=deepcopy(atom_map),
        n_source_atoms=len(forward),
        n_output_atoms=len(retained),
        n_input_structures=n_models,
        source_to_output_atom_indices=source_to_output,
        output_to_source_atom_indices=retained.copy(),
        pdbqt_to_output_atom_indices=written_to_output.copy(),
        input_structure_indices=selected.copy(),
        model_ids=np.asarray(selected_labels, dtype=object),
        omitted_source_atom_indices=omitted,
        missing_atoms=missing_atoms,
        coordinate_evidence="declared_pdbqt_pose_coordinates",
        source_coordinates_reused=False,
        partial_charge=charges[np.argsort(inverse)].copy(),
        charge_unit="elementary_charge",
        atom_ff_type=written_types[np.argsort(inverse)].copy(),
        typing_scheme="autodock4",
        remarks=[deepcopy(remarks[index]) for index in order],
        source_interactions_copied=False,
    )
    return {"molecular_system": output, "report": result}
