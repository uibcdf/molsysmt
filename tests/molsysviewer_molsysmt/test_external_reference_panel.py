"""Receive a distinct fitting reference without adopting or mutating it."""

import hashlib

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import Structures
from tests.molsysviewer_molsysmt.test_geometry_panel import act, coords
from tests.molsysviewer_molsysmt.test_geometry_panel import case as case

puw = msm.pyunitwizard


def _prepare(case, tmp_path, *, count=5, full=False):
    view, sent = case
    base = coords(view)[0]
    turn = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=float)
    reference_turn = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], dtype=float)
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
    view.addons.molsysmt.basic.set(coordinates=puw.quantity(query, "nm"))
    analysis = msm.Interactions.from_records(
        [],
        n_atoms=len(base),
        n_structures=3,
        evaluated_structure_indices=[0, 1, 2],
        method="existing-coverage",
    )
    view.molsys.interactions = {"science": analysis}
    order = [7, 19, 0, 11, 3]
    reference = np.stack(
        [
            base[order] @ reference_turn.T + np.array([3.1, -2.2, 0.7]) + i * 0.1
            for i in range(count)
        ]
    )
    path = tmp_path / "distinct-reference.h5msm"
    if full:
        builder = msm.MolSysBuilder()
        atoms = [builder.add_atom(atom_name=f"C{i}", atom_type="C") for i in range(5)]
        builder.add_group(atoms, group_name="LIG")
        builder.set_coordinates(puw.quantity(reference * 10, "angstrom"))
        msm.h5msm.write(builder.build(), path)
    else:
        msm.h5msm.write_layers(
            path,
            structures=Structures(coordinates=puw.quantity(reference * 10, "angstrom")),
        )
    return view, sent, base, query, reference, reference_turn, path, analysis


def _parameters(path, *, count=5, effect="update"):
    return {
        "task": "fit",
        "fit_reference_kind": "file",
        "fit_reference_filename": str(path),
        "fit_reference_structure": str(count - 1),
        "fit_expression": "[19, 3, 11, 0, 7]",
        "fit_reference_expression": "[1, 4, 3, 2, 0]",
        "structures": "indices",
        "indices": "2,0,2",
        "effect": effect,
    }


@pytest.mark.parametrize("effect", ["update", "result"])
@pytest.mark.parametrize("count", [1, 5])
@pytest.mark.parametrize("full", [False, True], ids=["structures-only", "full-system"])
@pytest.mark.parametrize("policy", ["nm", "pm"])
def test_external_reference_matches_analytic_pose_and_preserves_both_systems(
    case, tmp_path, effect, count, full, policy
):
    view, sent, base, before, reference, rotation, path, analysis = _prepare(
        case, tmp_path, count=count, full=full
    )
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    box = puw.get_value(view.molsys.structures.box, to_unit="nm").copy()
    revision = view.addons.molsysmt.get_sync_status()["target_revision"]
    with puw.context(standard_units=[policy, "fs", "radians", "dalton"]):
        reviewed = act(
            view,
            sent,
            "review",
            draft={"source": "indices", "indices": "0,1,2,3,4,5,6,7,8,9"},
            parameters=_parameters(path, count=count, effect=effect),
        )
    assert reviewed["stage"] == "review", reviewed["message"]
    assert reviewed["review"]["structure_indices"] == [2, 0]
    assert reviewed["review"]["reference_kind"] == "file"
    assert reviewed["review"]["reference_n_structures"] == count
    assert reviewed["review"]["reference_structure"] == count - 1
    panel = view._active_panel_widgets[None][2]
    assert panel._review.references.fit == (19, 3, 11, 0, 7)
    assert panel._review.references.reference == (1, 4, 3, 2, 0)
    snapshot = panel._review.reference_coordinates
    assert puw.get_value(snapshot).shape == (1, 5, 3)
    np.testing.assert_allclose(
        puw.get_value(snapshot, to_unit="nm"),
        reference[[-1]][:, [1, 4, 3, 2, 0]],
        atol=1e-13,
    )
    np.testing.assert_array_equal(coords(view), before)
    # Apply outside the review's physical-unit policy: the snapshot carries its unit.
    applied = act(view, sent, "apply", token=reviewed["review"]["token"])
    assert applied["stage"] == ("done" if effect == "update" else "result"), applied[
        "message"
    ]
    output = (
        view
        if effect == "update"
        else view.addons.manager.presentations.get(applied["result"]["id"])
    )
    expected = before.copy()
    expected[np.ix_([2, 0], range(10))] = (
        base[:10] @ rotation.T + np.array([3.1, -2.2, 0.7]) + (count - 1) * 0.1
    )
    np.testing.assert_allclose(coords(output), expected, atol=1e-10)
    np.testing.assert_array_equal(coords(output)[1], before[1])
    np.testing.assert_array_equal(coords(output)[:, 10:], before[:, 10:])
    np.testing.assert_array_equal(
        puw.get_value(output.molsys.structures.box, to_unit="nm"), box
    )
    np.testing.assert_array_equal(
        output.molsys.interactions["science"].evaluated_structure_indices, [1]
    )
    np.testing.assert_array_equal(analysis.evaluated_structure_indices, [0, 1, 2])
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision + int(
        effect == "update"
    )
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
    if effect == "result":
        np.testing.assert_array_equal(coords(view), before)
        assert output.molsys is not view.molsys
        assert output.molsys.structures.n_structures == 3
        act(view, sent, "result.discard")
        assert output.closed


def test_reference_review_reads_only_one_coordinate_slab_without_fitting_or_copying(
    case, tmp_path, monkeypatch
):
    import h5py

    view, sent, _, before, reference, _, _, _ = _prepare(case, tmp_path, count=5000)
    path = tmp_path / "wide-reference.h5msm"
    wide = np.zeros((5000, 10, 3))
    wide[:, :5] = reference
    msm.h5msm.write_layers(
        path, structures=Structures(coordinates=puw.quantity(wide, "nm"))
    )
    original_get = msm.basic.get
    original_read = h5py.Dataset.__getitem__
    reads = []
    disk_reads = []

    def read(dataset, key):
        if dataset.name == "/structures/coordinates":
            disk_reads.append(key)
        return original_read(dataset, key)

    def get(system, *args, **kwargs):
        if (
            isinstance(system, str)
            and system == str(path)
            and kwargs.get("coordinates")
        ):
            reads.append((kwargs["structure_indices"], kwargs["selection"]))
        return original_get(system, *args, **kwargs)

    def forbidden(*args, **kwargs):
        pytest.fail("Review must not fit or copy a molecular trajectory.")

    with monkeypatch.context() as patch:
        patch.setattr(msm.basic, "get", get)
        patch.setattr(msm.structure, "least_rmsd_fit", forbidden)
        patch.setattr(msm.basic, "copy", forbidden)
        patch.setattr(h5py.Dataset, "__getitem__", read)
        reviewed = act(
            view,
            sent,
            "review",
            draft={"source": "all"},
            parameters=_parameters(path, count=5000),
        )
    assert reviewed["stage"] == "review", reviewed["message"]
    assert reads == [([4999], [1, 4, 3, 2, 0])]
    assert disk_reads
    for key in disk_reads:
        assert isinstance(key, tuple)
        assert np.asarray(key[0]).shape == () and int(key[0]) == 4999
        np.testing.assert_array_equal(key[1], [0, 1, 2, 3, 4])
    snapshot = view._active_panel_widgets[None][2]._review.reference_coordinates
    assert puw.get_value(snapshot).nbytes == 5 * 3 * np.dtype("float64").itemsize
    np.testing.assert_array_equal(coords(view), before)


@pytest.mark.parametrize("change", ["write", "replace", "delete"])
def test_changed_reference_rejects_without_editing_or_rerunning_the_fit(
    case, tmp_path, monkeypatch, change
):
    view, sent, _, before, _, _, path, _ = _prepare(case, tmp_path)
    reviewed = act(
        view, sent, "review", draft={"source": "all"}, parameters=_parameters(path)
    )
    assert reviewed["stage"] == "review", reviewed["message"]
    if change == "write":
        with path.open("ab") as stream:
            stream.write(b"changed-after-review")
    elif change == "replace":
        other = path.with_name("replacement.h5msm")
        other.write_bytes(path.read_bytes())
        other.replace(path)
    else:
        path.unlink()
    status = view.addons.molsysmt.get_sync_status()

    def forbidden(*args, **kwargs):
        pytest.fail("A stale reference must reject before the native fit.")

    with monkeypatch.context() as patch:
        patch.setattr(msm.structure, "least_rmsd_fit", forbidden)
        result = act(view, sent, "apply", token=reviewed["review"]["token"])
    assert result["stage"] == "error"
    np.testing.assert_array_equal(coords(view), before)
    current = view.addons.molsysmt.get_sync_status()
    assert current["state"] == "synchronized"
    assert current["target_revision"] == status["target_revision"]
    assert not current["pending_operations"]


@pytest.mark.parametrize(
    "selection",
    [
        "[true, false, true]",
        "[1.0, 2, 3]",
        "[[0,1,2]]",
        "[1,",
        "[]",
        "[-1,0,2]",
        "[0,1,999]",
    ],
)
def test_ordered_fit_input_rejects_malformed_or_out_of_range_indices(
    case, tmp_path, selection
):
    view, sent, _, before, _, _, path, _ = _prepare(case, tmp_path)
    parameters = _parameters(path)
    parameters["fit_reference_expression"] = selection
    packet = act(view, sent, "review", draft={"source": "all"}, parameters=parameters)
    assert packet["stage"] == "error"
    np.testing.assert_array_equal(coords(view), before)
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize(
    "changes",
    [
        {"fit_reference_filename": ""},
        {"fit_reference_filename": "/missing/molsysmt-reference.h5msm"},
        {"fit_reference_filename": None},
        {"fit_reference_structure": "5"},
        {"fit_reference_structure": "-1"},
        {"fit_reference_structure": "1.5"},
        {"fit_reference_kind": "unknown"},
        {"fit_reference_expression": "[0,1,2]"},
    ],
)
def test_invalid_external_reference_never_publishes_coordinates(
    case, tmp_path, changes
):
    view, sent, _, before, _, _, path, _ = _prepare(case, tmp_path)
    parameters = {**_parameters(path), **changes}
    revision = view.addons.molsysmt.get_sync_status()["target_revision"]
    packet = act(view, sent, "review", draft={"source": "all"}, parameters=parameters)
    assert packet["stage"] == "error"
    np.testing.assert_array_equal(coords(view), before)
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision
    assert not view.addons.manager.presentations.records()


@pytest.mark.parametrize("side", ["source", "reference"])
@pytest.mark.parametrize("effect", ["update", "result"])
def test_late_degenerate_geometry_rejects_before_every_coordinate_write(
    case, tmp_path, side, effect
):
    import h5py

    view, sent, _, _, _, _, path, _ = _prepare(case, tmp_path)
    if side == "reference":
        with h5py.File(path, "r+") as file:
            unit = file["structures/coordinates"].attrs["unit"]
            file["structures/coordinates"][4] = np.column_stack(
                [np.arange(5), np.zeros((5, 2))]
            )
            assert file["structures/coordinates"].attrs["unit"] == unit
    else:
        value = coords(view)
        # The first requested structure is valid, the second must reject the whole fit.
        value[0, [19, 3, 11, 0, 7]] = np.column_stack([np.arange(5), np.zeros((5, 2))])
        view.addons.molsysmt.basic.set(coordinates=puw.quantity(value, "nm"))
    before = coords(view)
    reviewed = act(
        view,
        sent,
        "review",
        draft={"source": "all"},
        parameters=_parameters(path, effect=effect),
    )
    assert reviewed["stage"] == "review", reviewed["message"]
    revision = view.addons.molsysmt.get_sync_status()["target_revision"]
    result = act(view, sent, "apply", token=reviewed["review"]["token"])
    assert result["stage"] == "error"
    assert "non-collinear" in result["message"]
    np.testing.assert_array_equal(coords(view), before)
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"
    assert not view.addons.manager.presentations.records()


def test_reference_without_coordinates_is_rejected_before_editing(case, tmp_path):
    import h5py

    view, sent, _, before, _, _, path, _ = _prepare(case, tmp_path, full=True)
    with h5py.File(path, "r+") as file:
        del file["structures/coordinates"]
    packet = act(
        view, sent, "review", draft={"source": "all"}, parameters=_parameters(path)
    )
    assert packet["stage"] == "error"
    np.testing.assert_array_equal(coords(view), before)


def test_empty_moving_selection_does_not_read_an_external_file(case, monkeypatch):
    view, sent = case

    def forbidden(*args, **kwargs):
        pytest.fail("An empty moving population needs no reference I/O.")

    monkeypatch.setattr(
        "molsysviewer_molsysmt._geometry_panel._reference_file_identity", forbidden
    )
    packet = act(
        view,
        sent,
        "review",
        draft={"source": "indices", "indices": ""},
        parameters={"task": "fit", "fit_reference_kind": "file"},
    )
    assert packet["stage"] == "no_matches", packet["message"]


def test_explicit_source_order_can_pair_with_an_expression_on_a_full_reference(
    case, tmp_path
):
    view, sent, _, before, reference, _, path, _ = _prepare(case, tmp_path, full=True)
    # Source order follows the five atoms' declared order in the reference file.
    parameters = {
        **_parameters(path),
        "fit_expression": "[7,19,0,11,3]",
        "fit_reference_expression": "atom_index in [0,1,2,3,4]",
    }
    reviewed = act(view, sent, "review", draft={"source": "all"}, parameters=parameters)
    assert reviewed["stage"] == "review", reviewed["message"]
    panel = view._active_panel_widgets[None][2]
    assert panel._review.references.fit == (7, 19, 0, 11, 3)
    assert panel._review.references.reference == (0, 1, 2, 3, 4)
    applied = act(view, sent, "apply", token=reviewed["review"]["token"])
    assert applied["stage"] == "done", applied["message"]
    np.testing.assert_allclose(
        coords(view)[0, [7, 19, 0, 11, 3]], reference[4], atol=1e-10
    )
    np.testing.assert_array_equal(coords(view)[1], before[1])


def test_pdb_reference_uses_its_native_form_and_units(case, tmp_path):
    view, sent, _, before, _, _, path, _ = _prepare(case, tmp_path, full=True)
    pdb = tmp_path / "reference.pdb"
    msm.convert(path, to_form="file:pdb", structure_indices=[4], output_filename=pdb)
    reference = puw.get_value(
        msm.get(pdb, element="atom", structure_indices=[0], coordinates=True),
        to_unit="nm",
    )[0, [1, 4, 3, 2, 0]]
    expected = before.copy()
    target_center = reference.mean(axis=0)
    for structure in [2, 0]:
        anchors = before[structure, [19, 3, 11, 0, 7]]
        center = anchors.mean(axis=0)
        u, _, vt = np.linalg.svd((anchors - center).T @ (reference - target_center))
        proper = np.eye(3)
        proper[-1, -1] = np.linalg.det(u @ vt)
        expected[structure] = (before[structure] - center) @ (
            u @ proper @ vt
        ) + target_center
    digest = hashlib.sha256(pdb.read_bytes()).hexdigest()
    reviewed = act(
        view,
        sent,
        "review",
        draft={"source": "all"},
        parameters=_parameters(pdb, count=1),
    )
    assert reviewed["stage"] == "review", reviewed["message"]
    applied = act(view, sent, "apply", token=reviewed["review"]["token"])
    assert applied["stage"] == "done", applied["message"]
    np.testing.assert_allclose(coords(view), expected, atol=1e-10)
    assert hashlib.sha256(pdb.read_bytes()).hexdigest() == digest


def test_projection_retry_neither_refits_nor_requires_the_external_file(
    case, tmp_path, monkeypatch
):
    view, sent, _, _, _, _, path, _ = _prepare(case, tmp_path)
    reviewed = act(
        view, sent, "review", draft={"source": "all"}, parameters=_parameters(path)
    )
    assert reviewed["stage"] == "review", reviewed["message"]
    rebuild = view._rebuild_view_from_current_molsys
    native = msm.structure.least_rmsd_fit
    calls = []

    def fit(*args, **kwargs):
        calls.append(kwargs)
        return native(*args, **kwargs)

    def reject_projection(*args, **kwargs):
        raise RuntimeError("Injected projection failure after the native external fit")

    monkeypatch.setattr(msm.structure, "least_rmsd_fit", fit)
    monkeypatch.setattr(view, "_rebuild_view_from_current_molsys", reject_projection)
    failed = act(view, sent, "apply", token=reviewed["review"]["token"])
    assert failed["stage"] == "sync_required", failed["message"]
    assert len(calls) == 1
    before_retry = coords(view)
    revision = view.addons.molsysmt.get_sync_status()["target_revision"]
    path.unlink()

    def forbidden(*args, **kwargs):
        pytest.fail("Projection-only recovery must not reopen a scientific reference.")

    monkeypatch.setattr(
        "molsysviewer_molsysmt._geometry_panel._reference_file_identity", forbidden
    )
    monkeypatch.setattr(view, "_rebuild_view_from_current_molsys", rebuild)
    view._handle_frontend_event(
        {"event": "interaction_context_action", "action": "sync_system_edits"}
    )
    assert len(calls) == 1
    np.testing.assert_array_equal(coords(view), before_retry)
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision
