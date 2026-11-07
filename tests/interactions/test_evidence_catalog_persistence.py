"""Preserve complete typed evidence catalogs independently of active rows."""

import numpy as np
import pytest

import molsysmt as msm
from tests.interactions.test_copy import _equal


def _analysis(state):
    labels = ("unused/α", "polar_geometry", "unused_middle", "declared/external")
    codes = [3, 1]
    if state == "used-control":
        labels, codes = ("geometry",), [0, 0]
    result = msm.Interactions(
        n_atoms=3,
        n_structures=3,
        evaluated_structure_indices=[0, 1, 2],
        relation_types=["hbond"],
        relation_participant_offsets=[0, 3],
        participant_roles=["donor", "hydrogen", "acceptor"],
        participant_atom_offsets=[0, 1, 2, 3],
        participant_atoms=[0, 1, 2],
        occurrence_structures=[0, 2],
        occurrence_relations=[0, 0],
        occurrence_evidence=codes,
        evidence_labels=labels,
        measurements={"distance": [0.2, 0.25], "angle": [2.5, 2.8]},
        measure_units={"distance": "nm", "angle": "radians"},
        method="catalog-fixture",
        parameters={"threshold": {"value": 0.3, "unit": "nm"}},
        source_id="historical-source",
        software={"molsysmt": "0.7.1+producer"},
        execution={"execution": "fixture", "execution_chunks": 1},
        atom_source_indices=[4, 1, 3],
        source_n_atoms=5,
        structure_source_indices=[7, 2, 5],
        source_n_structures=8,
        evaluation_mode="incident",
        evaluation_atom_indices=[0],
        evaluation_universe_indices=[0, 1, 2],
        occurrence_image_offsets=[0, 3, 6],
        image_vectors=[
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [-1, 2, 0],
        ],
    )
    if state == "partial":
        return result.invalidate_structures([0])
    if state == "evaluated-empty":
        return result.invalidate_structures([0, 2])
    if state == "unevaluated":
        return result.invalidate_structures([0, 1, 2])
    if state == "empty-control":
        return msm.Interactions.from_records(
            [],
            n_atoms=3,
            n_structures=3,
            evaluated_structure_indices=[1],
            method="empty-control",
        )
    return result


def _payload(result):
    return msm.convert(result, to_form="molsysmt.InteractionsDict").to_dict()


def _carrier(analysis):
    builder = msm.MolSysBuilder()
    atoms = [
        builder.add_atom(atom_name=name, atom_type=kind)
        for name, kind in [("N", "N"), ("H", "H"), ("O", "O")]
    ]
    builder.add_group(atoms, group_name="LIG")
    builder.add_bond(atoms[0], atoms[1])
    builder.set_coordinates(
        msm.pyunitwizard.quantity(
            np.tile([[0.0, 0.0, 0.0], [0.1, 0.0, 0.0], [0.3, 0.0, 0.0]], (3, 1, 1)),
            "nm",
        )
    )
    builder.set_box(msm.pyunitwizard.quantity(np.tile(np.eye(3) * 3, (3, 1, 1)), "nm"))
    system = builder.build()
    system.interactions = {"hbonds": analysis}
    return system


@pytest.mark.parametrize("route", ["standalone", "layers", "molsys", "convert"])
@pytest.mark.parametrize(
    "state",
    [
        "packed",
        "partial",
        "evaluated-empty",
        "unevaluated",
        "empty-control",
        "used-control",
    ],
)
@pytest.mark.parametrize(
    "policy",
    [["nm", "ps", "radians", "dalton"], ["pm", "fs", "radians", "dalton"]],
    ids=["nm-ps", "pm-fs"],
)
def test_complete_evidence_catalog_payload_survives_all_public_storage_routes(
    tmp_path, route, state, policy
):
    original = _analysis(state)
    expected = _payload(original)
    with msm.pyunitwizard.context(standard_units=policy):
        if route == "standalone":
            filename = tmp_path / "catalog.h5i"
            original.save(filename)
            restored = msm.Interactions.load(filename)
        elif route == "layers":
            filename = tmp_path / "layers.h5msm"
            msm.h5msm.write_layers(filename, interactions={"hbonds": original})
            restored = msm.h5msm.read_layers(filename, layers="interactions")[
                "interactions"
            ]["hbonds"]
        else:
            source = _carrier(original)
            before = _payload(source.interactions["hbonds"])
            candidate = msm.copy(source)
            filename = tmp_path / "system.h5msm"
            if route == "molsys":
                msm.h5msm.write(candidate, filename)
                result = msm.h5msm.read(filename)
            else:
                msm.convert(candidate, to_form="file:h5msm", output_filename=filename)
                result = msm.convert(filename, to_form="molsysmt.MolSys")
            restored = result.interactions["hbonds"]
            _equal(_payload(source.interactions["hbonds"]), before)
            np.testing.assert_array_equal(
                msm.pyunitwizard.get_value(result.structures.coordinates, to_unit="nm"),
                msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm"),
            )
    _equal(_payload(restored), expected)
    _equal(_payload(original), expected)
    assert restored.evidence_labels == original.evidence_labels
    np.testing.assert_array_equal(
        restored.occurrence_evidence, original.occurrence_evidence, strict=True
    )
    if state in {"evaluated-empty", "unevaluated"}:
        assert restored.n_interactions == 0
        np.testing.assert_array_equal(
            restored.evaluated_structure_indices,
            [1] if state == "evaluated-empty" else [],
        )


@pytest.mark.parametrize(
    "codes, message",
    [
        (np.array([-1, 1], dtype=np.int32), "evidence code.*outside"),
        (np.array([4, 1], dtype=np.int32), "evidence code.*outside"),
        (np.array([2**32, 1], dtype=np.uint64), "outside.*range"),
        (np.array([3.0, 1.0]), "integers"),
        (np.array([True, False]), "integers"),
    ],
    ids=["negative", "out-of-table", "int32-overflow", "floating", "boolean"],
)
def test_stored_evidence_codes_are_validated_before_label_lookup(
    tmp_path, codes, message
):
    import h5py

    path = tmp_path / "invalid-code.h5i"
    _analysis("packed").save(path)
    with h5py.File(path, "r+") as file:
        del file["occurrence_evidence"]
        file.create_dataset("occurrence_evidence", data=codes)
    with pytest.raises(ValueError, match=message):
        msm.Interactions.load(path)


@pytest.mark.parametrize("state", ["packed", "partial", "unevaluated"])
def test_legacy_schema_retains_the_explicit_evidence_catalog(tmp_path, state):
    import json

    import h5py

    original = _analysis(state)
    expected = _payload(original)
    path = tmp_path / "schema-one.h5i"
    original.save(path)
    with h5py.File(path, "r+") as file:
        metadata = json.loads(file.attrs["metadata"])
        metadata["parameters"].update(execution="fixture", execution_chunks=1)
        file.attrs["metadata"] = json.dumps(metadata)
        file.attrs["schema_version"] = 1
        del file["execution"]
    _equal(_payload(msm.Interactions.load(path)), expected)
    _equal(_payload(original), expected)
