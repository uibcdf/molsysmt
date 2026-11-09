"""Receive directed vector and explicit angular observations through real panels."""

import json

import numpy as np
import pytest

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_analysis_panel import (
    FRAMES,
    A,
    B,
    act,
    calculate,
)
from tests.molsysviewer_molsysmt.test_analysis_panel import (
    case as case,
)
from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
    same,
    snapshot,
    unchanged,
)

puw = msm.pyunitwizard


def atoms(indices):
    return {
        "source": "indices",
        "indices": " ".join(map(str, indices)),
        "context": "index",
        "structure_index": 0,
    }


def geometry(view):
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm").copy()
    xyz[:, :4] = [[1, 0, 0], [0, 0, 0], [0, 1, 0], [0, 1, 1]]
    xyz[1:, 3, 2] = -1
    msm.set(view.molsys, coordinates=puw.quantity(xyz, "nm"))
    return xyz


@pytest.mark.parametrize("policy", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("paired", [False, True])
def test_vector_direction_source_axes_units_and_native_parity(case, policy, paired):
    view, _, panel = case
    before = snapshot(view)
    first, second = [4, 0, 4], [5, 2, 5] if paired else [5, 2]
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm")
    with puw.context(standard_units=[policy, "ps"]):
        active = puw.configure.report()
        result = calculate(
            case,
            "vectors",
            b=atoms(second),
            pairing="paired" if paired else "cartesian",
        )
        native = msm.structure.get_vectors(
            view.molsys,
            selection=first,
            selection_2=second,
            structure_indices=FRAMES,
            pairs=paired,
            pbc=False,
            heavy_mode="force",
        )
        same(panel._report.values, native)
        assert puw.configure.report() == active
    q, r = xyz[FRAMES][:, first], xyz[FRAMES][:, second]
    expected = r - q if paired else r[:, None] - q[:, :, None]
    np.testing.assert_allclose(
        puw.get_value(panel._report.values, to_unit="nm"), expected
    )
    shown = np.asarray([row[-3:] for row in result["page"]["rows"]], dtype=float)
    np.testing.assert_allclose(shown, expected.reshape(-1, 3), rtol=1e-8, atol=1e-9)
    assert result["report"]["family"] == "vector"
    assert result["page"]["columns"][-3:] == ["X (nm)", "Y (nm)", "Z (nm)"]
    assert result["report"]["rows"] == len(expected.reshape(-1, 3))
    unchanged(view, before)


@pytest.mark.parametrize("endpoint", ["geometric", "mass"])
def test_center_vectors_preserve_repeated_atom_weighting(case, endpoint):
    view, _, panel = case
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[FRAMES]
    weights_a = weights_b = None
    if endpoint == "mass":
        weights_a = puw.get_value(
            msm.physchem.get_mass(view.molsys, element="atom", selection=[4, 0, 4])
        )
        weights_b = puw.get_value(
            msm.physchem.get_mass(view.molsys, element="atom", selection=[5, 2])
        )
    expected = np.average(xyz[:, [5, 2]], axis=1, weights=weights_b) - np.average(
        xyz[:, [4, 0, 4]], axis=1, weights=weights_a
    )
    result = calculate(
        case, "vectors", first_endpoint=endpoint, second_endpoint=endpoint
    )
    np.testing.assert_allclose(
        puw.get_value(panel._report.values, to_unit="nm")[:, 0, 0], expected
    )
    assert [row[1:3] for row in result["page"]["rows"]] == [
        ["Center A", "Center B"]
    ] * 3


def test_vectors_keep_periodic_direction_with_a_real_box(case):
    view, _, panel = case
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm").copy()
    xyz[:, 0], xyz[:, 1] = [0.9, 0, 0], [0.1, 0, 0]
    msm.set(
        view.molsys,
        coordinates=puw.quantity(xyz, "nm"),
        box=puw.quantity(np.tile(np.eye(3), (3, 1, 1)), "nm"),
    )
    result = calculate(case, "vectors", a=atoms([0]), b=atoms([1]), pbc=True)
    assert result["report"]["periodic"]
    np.testing.assert_allclose(
        puw.get_value(panel._report.values, to_unit="nm")[:, 0, 0],
        [[0.2, 0, 0]] * 3,
        atol=1e-15,
    )


def test_within_vectors_preserve_zero_diagonal_and_reverse_direction(case):
    view, _, panel = case
    result = calculate(case, "vectors", relation="within")
    values = puw.get_value(panel._report.values, to_unit="nm")
    np.testing.assert_array_equal(
        values + values.transpose(0, 2, 1, 3), np.zeros_like(values)
    )
    np.testing.assert_array_equal(
        values[:, np.arange(3), np.arange(3)], np.zeros((3, 3, 3))
    )
    assert result["report"]["rows"] == 27


@pytest.mark.parametrize("task", ["angles", "torsions"])
@pytest.mark.parametrize("periodic", [False, True])
def test_angular_periodic_images_have_independent_analytical_values(
    case, task, periodic
):
    view, _, panel = case
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm").copy()
    if task == "angles":
        xyz[:, :3] = [[0.9, 0, 0], [0.1, 0, 0], [0.2, 0.1, 0]]
        row, expected = [0, 1, 2], 135.0 if periodic else 45.0
    else:
        xyz[:, :4] = [[0.9, 0, 0], [0.1, 0, 0], [0.1, 0.2, 0], [0.1, 0.2, 0.2]]
        row, expected = [0, 1, 2, 3], 90.0 if periodic else -90.0
    msm.set(
        view.molsys,
        coordinates=puw.quantity(xyz, "nm"),
        box=puw.quantity(np.tile(np.eye(3), (3, 1, 1)), "nm"),
    )
    result = calculate(case, task, atom_tuples=json.dumps([row]), pbc=periodic)
    assert result["report"]["periodic"] == periodic
    np.testing.assert_allclose(
        puw.get_value(panel._report.values, to_unit="degrees"),
        np.full((3, 1), expected),
        atol=1e-12,
    )


@pytest.mark.parametrize(
    "task,tuples",
    [
        ("angles", [[0, 1, 2], [2, 1, 0]]),
        ("torsions", [[0, 1, 2, 3], [3, 2, 1, 0]]),
    ],
)
@pytest.mark.parametrize("unit", ["degrees", "radians"])
@pytest.mark.parametrize("policy", ["radians", "degrees"])
def test_analytical_angles_order_signs_native_units_and_no_primary_selection(
    case, task, tuples, unit, policy
):
    view, sent, panel = case
    geometry(view)
    before = snapshot(view)
    with puw.context(standard_units=["pm", "ps", policy]):
        active = puw.configure.report()
        result = act(
            view,
            sent,
            draft={"source": "none"},
            parameters={
                "task": task,
                "structures": "indices",
                "indices": "2,0,2",
                "atom_tuples": json.dumps(tuples),
                "angle_unit": unit,
            },
        )
        assert result["stage"] == "report", result["message"]
        arguments = {
            "triplets" if task == "angles" else "dihedral_quartets": tuples,
            "structure_indices": FRAMES,
            "use_gpu": False,
        }
        native = getattr(
            msm.structure, "get_angles" if task == "angles" else "get_dihedral_angles"
        )(view.molsys, **arguments)
        same(panel._report.values, native)
        assert puw.get_unit(panel._report.values) == puw.unit(policy)
        assert puw.configure.report() == active
    expected = np.tile(
        [[90.0], [90.0], [90.0]] if task == "angles" else [[90.0], [-90.0], [90.0]],
        (1, 2),
    )
    np.testing.assert_allclose(
        puw.get_value(panel._report.values, to_unit="degrees"), expected
    )
    shown = np.asarray([row[-1] for row in result["page"]["rows"]], dtype=float)
    np.testing.assert_allclose(
        shown,
        (np.deg2rad(expected) if unit == "radians" else expected).ravel(),
        rtol=1e-8,
    )
    assert result["report"]["structure_indices"] == FRAMES
    assert [r[1:-1] for r in result["page"]["rows"]] == tuples * 3
    assert (
        result["report"]["family"] == "angular" and result["report"]["tuple_count"] == 2
    )
    unchanged(view, before)


@pytest.mark.parametrize(
    "task,tuples", [("angles", [[0, 1, 1]]), ("torsions", [[0, 1, 1, 3]])]
)
def test_undefined_native_angular_observations_are_not_zero(case, task, tuples):
    view, _, panel = case
    geometry(view)
    result = calculate(case, task, atom_tuples=json.dumps(tuples))
    assert np.isnan(puw.get_value(panel._report.values)).all()
    assert [row[-1] for row in result["page"]["rows"]] == ["undefined"] * 3


@pytest.mark.parametrize("task", ["angles", "torsions"])
@pytest.mark.parametrize(
    "bad",
    [
        "",
        "[]",
        "[0,1,2]",
        "[[0,1]]",
        "[[0,1,2,3,4]]",
        "[[true,1,2]]",
        "[[0,1,-1]]",
        "[[0,1,100000]]",
        "[[0,1,1.5]]",
        "null",
    ],
)
def test_invalid_tuple_requests_leave_source_and_scene_unchanged(case, task, bad):
    view, sent, panel = case
    before = snapshot(view)
    result = act(view, sent, parameters={"task": task, "atom_tuples": bad})
    assert result["stage"] == "error"
    assert panel._report is None
    unchanged(view, before)


@pytest.mark.parametrize("task", ["vectors", "angles", "torsions"])
def test_source_index_paging_and_participant_actions_reuse_native_result(
    case, task, monkeypatch
):
    view, sent, panel = case
    geometry(view)
    if task == "vectors":
        result = calculate(case, task, a=atoms(list(range(22))), b=atoms([30]))
        expected = {6, 30}
    else:
        row = [0, 1, 2] if task == "angles" else [0, 1, 2, 3]
        result = calculate(case, task, atom_tuples=json.dumps([row] * 55))
        expected = set(row)
    assert len(result["page"]["rows"]) == 50
    token = result["report"]["id"]
    result = act(view, sent, "page", report_id=token, offset=50)
    assert result["page"]["offset"] == 50
    assert result["page"]["rows"][0][0] == 2
    xyz = puw.get_value(view.molsys.structures.coordinates).copy()

    def no_replay(*args, **kwargs):
        raise AssertionError(
            "Participant actions must not repeat the native calculation."
        )

    name = {
        "vectors": "get_vectors",
        "angles": "get_angles",
        "torsions": "get_dihedral_angles",
    }[task]
    monkeypatch.setattr(view.addons.molsysmt.structure, name, no_replay)
    for action in ["select_participants", "focus_participants"]:
        done = act(view, sent, action, report_id=token, row_index=50)
        assert done["stage"] == "scene", done["message"]
    assert set(view.active_selection.atom_indices) == expected
    np.testing.assert_array_equal(
        puw.get_value(view.molsys.structures.coordinates), xyz
    )
    denied = act(view, sent, "add_live_distance", report_id=token, row_index=50)
    assert denied["stage"] == "error" and not view.measurements.info()


@pytest.mark.parametrize("task", ["vectors", "angles", "torsions"])
def test_pending_readers_and_stale_result_tokens(case, task):
    view, sent, _ = case
    geometry(view)
    view.addons.molsysmt.structure.translate(
        translation="[1, 0, 0] nm", in_place=True, update_view=False
    )
    before = snapshot(view)
    row = [0, 1, 2] if task == "angles" else [0, 1, 2, 3]
    result = calculate(case, task, a=A, b=B, atom_tuples=json.dumps([row]))
    unchanged(view, before)
    token = result["report"]["id"]
    denied = act(view, sent, "select_participants", report_id=token, row_index=0)
    # The host refuses non-reader actions before dispatch while pending. It
    # does not promise an addon error packet for a request it never delivered.
    unchanged(view, before)
    assert denied["report"]["id"] == token
    view.addons.molsysmt.structure.translate(
        translation="[1, 0, 0] nm", in_place=True, update_view=False
    )
    expired = act(
        view,
        sent,
        "page",
        report_id=token,
        offset=0,
        request_id=result["request_id"] + 10,
    )
    assert expired["stage"] == "error" and "expired" in expired["message"]
