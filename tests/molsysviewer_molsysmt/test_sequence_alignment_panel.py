"""Receive sequence-derived components without positional-pair assumptions."""

import hashlib
import json

import h5py
import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import MolecularMechanics
from tests.molsysviewer_molsysmt.test_geometry_panel import act, coords, mount
from tests.molsysviewer_molsysmt.test_system_panel import transport

puw = msm.pyunitwizard


def _sequence_systems(reference_count=5):
    """Use distinct amino-acid labels and an explicit rigid-pose oracle."""
    peptide = msm.build.build_peptide("ACEALAGLYSERTHRNME")
    reference = msm.build.build_peptide("ACEALASERTHRNME")
    # This geometry fixture deliberately excludes the experimental mechanics
    # domain, which H5MSM 0.5 does not encode; chemical assignments remain.
    peptide.molecular_mechanics = MolecularMechanics()
    reference.molecular_mechanics = MolecularMechanics()
    data = msm.get(
        peptide,
        element="atom",
        group_name=True,
        atom_name=True,
        output_type="dictionary",
    )
    ref_data = msm.get(
        reference,
        element="atom",
        group_name=True,
        atom_name=True,
        output_type="dictionary",
    )
    n = msm.get(peptide, n_atoms=True)
    i = np.arange(n, dtype=float)
    base = np.column_stack([i * 0.04, (i % 5) * 0.1, (i % 9) * 0.07])
    lookup = {
        (group, atom): point
        for group, atom, point in zip(
            data["group_name"], data["atom_name"], base, strict=True
        )
    }
    ref_base = np.array(
        [
            lookup[group, atom]
            for group, atom in zip(
                ref_data["group_name"], ref_data["atom_name"], strict=True
            )
        ]
    )
    turn = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=float)
    query = np.stack(
        [
            base @ matrix.T + shift
            for matrix, shift in [
                (turn, [1.2, -0.3, 0.6]),
                (np.eye(3), [-0.5, 0.4, 0.2]),
                (turn.T, [0.3, 1.4, -0.8]),
            ]
        ]
    )
    msm.set(peptide, coordinates=puw.quantity(query, "nm"))
    builder = msm.MolSysBuilder()
    for name, kind in [("O", "O"), ("H1", "H"), ("H2", "H")]:
        builder.add_atom(atom_name=name, atom_type=kind)
    builder.add_group([0, 1, 2], group_name="HOH", group_type="water")
    builder.add_bond(0, 1)
    builder.add_bond(0, 2)
    water = np.array([[10.0, 2.0, 1.0], [10.1, 2.0, 1.0], [10.0, 2.1, 1.0]])
    builder.set_coordinates(puw.quantity(np.tile(water[None], (3, 1, 1)), "nm"))
    query = msm.merge([peptide, builder.build()])
    msm.set(query, box=puw.quantity(np.tile(np.eye(3) * 4, (3, 1, 1)), "nm"))
    ref_turn = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], dtype=float)
    ref_points = np.stack(
        [
            ref_base @ ref_turn.T + [3.1 + j * 0.1, -2.2, 0.7]
            for j in range(reference_count)
        ]
    )
    msm.set(reference, coordinates=puw.quantity(ref_points * 10, "angstrom"))
    reference = msm.permute_atoms(
        reference, atom_indices=list(range(len(ref_base) - 1, -1, -1))
    )
    expected = base @ ref_turn.T + [3.1 + (reference_count - 1) * 0.1, -2.2, 0.7]
    return query, reference, expected, n


@pytest.fixture
def sequence_case(tmp_path):
    source, reference, expected, moving = _sequence_systems()
    path = tmp_path / "sequence-reference.h5msm"
    msm.h5msm.write(reference, path)
    with msv.new_view(source) as view:
        analysis = msm.Interactions.from_records(
            [],
            n_atoms=msm.get(source, n_atoms=True),
            n_structures=3,
            evaluated_structure_indices=[0, 1, 2],
            method="existing-coverage",
        )
        view.molsys.interactions = {"science": analysis}
        sent = transport(view)
        mount(view)
        yield view, sent, reference, path, expected, moving, analysis


def _parameters(path=None, **kwargs):
    return {
        "task": "sequence",
        "fit_reference_kind": "file" if path else "system",
        "fit_reference_filename": str(path) if path else "",
        "fit_reference_structure": "4" if path else "1",
        "structures": "indices",
        "indices": "2,0,2",
        **kwargs,
    }


@pytest.mark.parametrize("reference_kind", ["system", "file"])
@pytest.mark.parametrize("effect", ["update", "result"])
@pytest.mark.parametrize("policy", ["nm", "pm"])
@pytest.mark.parametrize("population", ["default", "indices", "names"])
def test_sequence_alignment_has_gap_name_and_complete_component_semantics(
    sequence_case, monkeypatch, reference_kind, effect, policy, population
):
    view, sent, reference, path, external_expected, moving, old_analysis = sequence_case
    target = view.molsys
    before, reference_before = (
        coords(view),
        puw.get_value(msm.get(reference, coordinates=True), to_unit="nm").copy(),
    )
    box = puw.get_value(target.structures.box, to_unit="nm").copy()
    revision = view.addons.molsysmt.get_sync_status()["target_revision"]
    raw = path.read_bytes()
    parameters = _parameters(path if reference_kind == "file" else None, effect=effect)
    expression = (
        'atom_name in ["N", "CA", "C"]' if population == "names" else 'atom_name=="CA"'
    )
    query_atoms = msm.select(target, selection=expression)
    reference_atoms = msm.select(
        reference if reference_kind == "file" else target, selection=expression
    )
    if population != "names":
        assert len(query_atoms) == 4
        assert len(reference_atoms) == (3 if reference_kind == "file" else 4)
    else:
        parameters["fit_expression"] = expression
        parameters["fit_reference_expression"] = expression
    if population == "indices":
        parameters["fit_expression"] = json.dumps(query_atoms[::-1] + query_atoms[:1])
        parameters["fit_reference_expression"] = json.dumps(
            reference_atoms[::-1] + reference_atoms[:1]
        )
    expected = before.copy()
    expected[[2, 0], :moving] = (
        external_expected if reference_kind == "file" else before[1, :moving]
    )
    calls = []
    original = msm.structure.least_rmsd_align

    def align(*args, **kwargs):
        calls.append(kwargs)
        return original(*args, **kwargs)

    monkeypatch.setattr(msm.structure, "least_rmsd_align", align)
    with puw.context(standard_units=[policy, "fs", "radians", "dalton"]):
        active_policy = dict(puw.configure.get_standard_units())
        reviewed = act(view, sent, "review", parameters=parameters)
        assert dict(puw.configure.get_standard_units()) == active_policy
    assert reviewed["stage"] == "review", reviewed["message"]
    assert calls == []
    assert reviewed["review"]["n_atoms"] == moving
    assert reviewed["review"]["n_fit_atoms"] == len(query_atoms)
    assert reviewed["review"]["n_reference_atoms"] == len(reference_atoms)
    assert reviewed["review"]["structure_indices"] == [2, 0]
    np.testing.assert_array_equal(coords(view), before)
    packet = act(view, sent, "apply", token=reviewed["review"]["token"])
    assert packet["stage"] == ("done" if effect == "update" else "result"), packet[
        "message"
    ]
    assert len(calls) == 1
    assert calls[0]["selection"] == query_atoms
    assert calls[0]["use_gpu"] is False
    assert calls[0]["engine_sequence_alignment"] == "Biopython"
    output = (
        view
        if effect == "update"
        else view.addons.manager.presentations.get(packet["result"]["id"])
    )
    np.testing.assert_allclose(coords(output), expected, rtol=0, atol=1e-11)
    np.testing.assert_array_equal(coords(output)[1], before[1])
    np.testing.assert_array_equal(coords(output)[:, moving:], before[:, moving:])
    np.testing.assert_array_equal(
        puw.get_value(output.molsys.structures.box, to_unit="nm"), box
    )
    np.testing.assert_array_equal(
        output.molsys.interactions["science"].evaluated_structure_indices, [1]
    )
    np.testing.assert_array_equal(old_analysis.evaluated_structure_indices, [0, 1, 2])
    np.testing.assert_array_equal(
        puw.get_value(msm.get(reference, coordinates=True), to_unit="nm"),
        reference_before,
    )
    assert path.read_bytes() == raw
    assert view.molsys is target
    if effect == "result":
        np.testing.assert_array_equal(coords(view), before)
        assert output.molsys is not target
        assert not np.shares_memory(
            puw.get_value(output.molsys.structures.coordinates),
            puw.get_value(target.structures.coordinates),
        )
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision + (
        effect == "update"
    )


def test_sequence_review_reads_one_slab_and_only_stored_topology(
    sequence_case, tmp_path, monkeypatch
):
    view, sent, _, _, _, _, _ = sequence_case
    _, reference, _, _ = _sequence_systems(reference_count=5000)
    path = tmp_path / "many-structures.h5msm"
    msm.h5msm.write(reference, path)
    raw = hashlib.sha256(path.read_bytes()).hexdigest()
    original = h5py.Dataset.__getitem__
    windows = []

    def getitem(dataset, key):
        if dataset.name.startswith(("/chemical_states/", "/interactions/")):
            pytest.fail("Review read unrelated reference chemistry or interactions")
        if dataset.name == "/structures/coordinates":
            windows.append(key)
            assert isinstance(key, tuple) and int(key[0]) == 4999
            assert len(key[1]) == 3
        return original(dataset, key)

    def forbidden(*args, **kwargs):
        pytest.fail("Review fitted coordinates or copied the complete trajectory")

    with monkeypatch.context() as patch:
        patch.setattr(h5py.Dataset, "__getitem__", getitem)
        patch.setattr(msm.basic, "copy", forbidden)
        patch.setattr(msm.structure, "least_rmsd_align", forbidden)
        patch.setattr(msm.structure, "least_rmsd_fit", forbidden)
        packet = act(
            view,
            sent,
            "review",
            parameters=_parameters(path, fit_reference_structure="4999"),
        )
    assert packet["stage"] == "review", packet["message"]
    assert windows
    review = view._active_panel_widgets[None][2]._review
    assert puw.get_value(review.reference_coordinates).shape == (1, 3, 3)
    assert msm.get(review.reference_system, n_atoms=True, n_structures=True) == [
        msm.get(reference, n_atoms=True),
        1,
    ]
    positions = puw.get_value(msm.get(review.reference_system, coordinates=True))
    assert positions.shape == (1, msm.get(reference, n_atoms=True), 3)
    assert np.count_nonzero(np.isfinite(positions)) == 3 * 3
    assert review.reference_system.chemical_states is None
    assert hashlib.sha256(path.read_bytes()).hexdigest() == raw


@pytest.mark.parametrize("change", ["write", "delete"])
def test_changed_sequence_reference_rejects_before_fitting(
    sequence_case, monkeypatch, change
):
    view, sent, _, path, _, _, _ = sequence_case
    before = coords(view)
    packet = act(view, sent, "review", parameters=_parameters(path))
    assert packet["stage"] == "review", packet["message"]
    if change == "delete":
        path.unlink()
    else:
        with path.open("ab") as stream:
            stream.write(b"changed")

    def forbidden(*args, **kwargs):
        pytest.fail("An expired file reference must not be fitted")

    monkeypatch.setattr(msm.structure, "least_rmsd_align", forbidden)
    packet = act(view, sent, "apply", token=packet["review"]["token"])
    assert packet["stage"] == "error"
    np.testing.assert_array_equal(coords(view), before)
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize("bad", ["[true]", "[0.5]", "[9999]", "atom_index==9999"])
def test_bad_sequence_populations_reject_during_review(sequence_case, bad):
    view, sent, _, path, _, _, _ = sequence_case
    before = coords(view)
    packet = act(view, sent, "review", parameters=_parameters(path, fit_expression=bad))
    assert packet["stage"] == "error"
    assert not packet.get("review")
    np.testing.assert_array_equal(coords(view), before)


def test_last_degenerate_structure_rejects_before_every_write(sequence_case):
    view, sent, _, path, _, _, _ = sequence_case
    before = coords(view)
    anchors = msm.select(view.molsys, selection='atom_name=="CA"')
    before[0, anchors] = np.column_stack(
        [np.arange(len(anchors)), np.zeros((len(anchors), 2))]
    )
    view.addons.molsysmt.basic.set(coordinates=puw.quantity(before, "nm"))
    status = view.addons.molsysmt.get_sync_status()
    packet = act(view, sent, "review", parameters=_parameters(path))
    assert packet["stage"] == "review", packet["message"]
    packet = act(view, sent, "apply", token=packet["review"]["token"])
    assert packet["stage"] == "error"
    np.testing.assert_array_equal(coords(view), before)
    after = view.addons.molsysmt.get_sync_status()
    assert {k: v for k, v in after.items() if k != "operation_id"} == {
        k: v for k, v in status.items() if k != "operation_id"
    }
    assert after["operation_id"].startswith("molsysmt.structure.least_rmsd_align:")
