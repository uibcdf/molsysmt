"""Qualify Boolean contact maps without converting them into distance observations."""

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
from tests.molsysviewer_molsysmt.test_analysis_panel import case as _analysis_case
from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
    same,
    snapshot,
    unchanged,
)

case = _analysis_case
puw = msm.pyunitwizard


def _expected(view, first, second, frames, cutoff, *, paired=False, center=None):
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm")
    a, b = xyz[frames][:, first], xyz[frames][:, second]
    if center:
        weights = (
            None
            if center == "geometric"
            else msm.physchem.get_mass(view.molsys, element="atom", selection=first)
        )
        weights_2 = (
            None
            if center == "geometric"
            else msm.physchem.get_mass(view.molsys, element="atom", selection=second)
        )
        a = np.average(
            a,
            axis=1,
            weights=None if weights is None else puw.get_value(weights, to_unit="Da"),
        )[:, None]
        b = np.average(
            b,
            axis=1,
            weights=None
            if weights_2 is None
            else puw.get_value(weights_2, to_unit="Da"),
        )[:, None]
    delta = a - b if paired else a[:, :, None] - b[:, None]
    return np.linalg.norm(delta, axis=-1) <= cutoff


@pytest.mark.parametrize(
    "unit,cutoff", [("nm", "0.35"), ("angstrom", "3.5"), ("pm", "350")]
)
@pytest.mark.parametrize("pairing", ["cartesian", "paired"])
def test_contact_maps_match_coordinates_retain_boolean_axes_and_units(
    case, unit, cutoff, pairing
):
    view, _, panel = case
    first, second = [4, 0, 4], [5, 2, 5] if pairing == "paired" else [5, 2]
    before = snapshot(view)
    expected = _expected(view, first, second, FRAMES, 0.35, paired=pairing == "paired")
    with puw.context(standard_units=[unit, "ps", "radians"]):
        result = calculate(
            case,
            "contacts",
            b={**B, "indices": " ".join(map(str, second))},
            pairing=pairing,
            cutoff=cutoff,
            cutoff_unit=unit,
        )
    assert panel._report.values.dtype == np.dtype("bool")
    np.testing.assert_array_equal(panel._report.values, expected)
    assert result["report"]["family"] == "contact"
    assert result["report"]["unit"] is None
    assert result["report"]["contacts"] == int(expected.sum())
    assert result["report"]["evaluated_pairs"] == expected.size
    assert result["report"]["threshold"] == {
        "value": float(cutoff),
        "unit": unit,
        "comparison": "<=",
    }
    assert result["report"]["structure_indices"] == FRAMES
    rows = result["page"]["rows"]
    for position, row in enumerate(rows):
        if pairing == "paired":
            structure, a = np.unravel_index(position, expected.shape)
            b = a
        else:
            structure, a, b = np.unravel_index(position, expected.shape)
        assert row == [
            FRAMES[structure],
            first[a],
            second[b],
            bool(expected.flat[position]),
        ]
        assert type(row[3]) is bool
    assert "Contact" in result["page"]["columns"][-1]
    unchanged(view, before)


@pytest.mark.parametrize("endpoint", ["geometric", "mass"])
def test_center_contacts_keep_population_identity_without_fictitious_atom_labels(
    case, endpoint
):
    view, _, panel = case
    before = snapshot(view)
    expected = _expected(view, [4, 0, 4], [5, 2], FRAMES, 0.35, center=endpoint)
    result = calculate(
        case, "contacts", first_endpoint=endpoint, second_endpoint=endpoint
    )
    np.testing.assert_array_equal(panel._report.values, expected)
    assert all(row[1:3] == ["Center A", "Center B"] for row in result["page"]["rows"])
    unchanged(view, before)


@pytest.mark.parametrize(
    "unit,cutoff", [("nm", "0.5"), ("angstrom", "5"), ("pm", "500")]
)
def test_inclusive_boundary_and_zero_contact_scope_are_explicit(case, unit, cutoff):
    view, _, panel = case
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm").copy()
    xyz[:, 0] = [0, 0, 0]
    xyz[:, 1] = [0.5, 0, 0]
    xyz[:, 2] = [1, 0, 0]
    view.molsys.structures.coordinates = puw.quantity(xyz, "nm")
    before = snapshot(view)
    result = calculate(
        case,
        "contacts",
        a={**A, "indices": "0"},
        b={**B, "indices": "1 2"},
        cutoff=cutoff,
        cutoff_unit=unit,
    )
    np.testing.assert_array_equal(
        panel._report.values, np.tile([[[True, False]]], (3, 1, 1))
    )
    assert [row[3] for row in result["page"]["rows"]] == [True, False] * 3
    empty = calculate(
        case,
        "contacts",
        a={**A, "indices": "0"},
        b={**B, "indices": "1 2"},
        cutoff="0",
        cutoff_unit=unit,
    )
    assert empty["stage"] == "report" and empty["report"]["contacts"] == 0
    assert empty["report"]["evaluated_pairs"] == 6
    assert empty["page"]["rows"] and all(
        row[3] is False for row in empty["page"]["rows"]
    )
    unchanged(view, before)


def test_within_population_retains_native_diagonal_and_directed_occurrences(case):
    view, _, panel = case
    before = snapshot(view)
    first = [4, 0, 4]
    result = calculate(case, "contacts", relation="within", cutoff="0")
    expected = _expected(view, first, first, FRAMES, 0)
    np.testing.assert_array_equal(panel._report.values, expected)
    assert np.all(np.diagonal(panel._report.values, axis1=1, axis2=2))
    assert result["report"]["evaluated_pairs"] == 27
    unchanged(view, before)


def test_contact_rows_select_and_focus_but_cannot_create_a_live_distance(case):
    view, sent, _ = case
    calculate(case, "contacts", cutoff="0")
    before = snapshot(view)
    result = act(
        view, sent, "focus_participants", report_id=case[2]._report.token, row_index=0
    )
    assert result["scene_action"]["structure_index"] == 0
    assert result["scene_action"]["observation_structure_index"] == 2
    assert view.player.index == 0
    denied = act(
        view, sent, "add_live_distance", report_id=case[2]._report.token, row_index=0
    )
    assert denied["stage"] == "error" and "Boolean cutoff" in denied["message"]
    assert not view.measurements.info()
    selected = act(
        view, sent, "select_participants", report_id=case[2]._report.token, row_index=0
    )
    assert selected["stage"] == "scene"
    assert view.active_selection.atom_indices == [4, 5]
    same(view.molsys, before[1])
    assert view.addons.molsysmt.get_sync_status() == before[3]


@pytest.mark.parametrize("cutoff", ["nan", "inf", "-0.01", "invalid"])
def test_invalid_thresholds_do_not_change_molecules_or_scene(case, cutoff):
    view, sent, _ = case
    before = snapshot(view)
    result = act(
        view, sent, draft=A, second=B, parameters={"task": "contacts", "cutoff": cutoff}
    )
    assert result["stage"] == "error" and "finite, nonnegative" in result["message"]
    unchanged(view, before)


def test_contact_pages_bound_rows_and_retain_global_indices_and_boolean_values(case):
    view, sent, _ = case
    before = snapshot(view)
    first, second = list(range(55)), [60, 61]
    expected = _expected(view, first, second, FRAMES, 0.35)
    result = calculate(
        case,
        "contacts",
        a={**A, "indices": " ".join(map(str, first))},
        b={**B, "indices": "60 61"},
    )
    assert result["report"]["rows"] == expected.size == 330
    assert len(result["page"]["rows"]) == 50
    page = act(view, sent, "page", report_id=result["report"]["id"], offset=50)
    assert page["page"]["offset"] == 50 and len(page["page"]["rows"]) == 50
    for position, row in enumerate(page["page"]["rows"], 50):
        f, a, b = np.unravel_index(position, expected.shape)
        assert row == [FRAMES[f], first[a], second[b], bool(expected.flat[position])]
    cleared = act(view, sent, "clear")
    assert cleared["report"] is None and case[2]._report is None
    unchanged(view, before)


@pytest.mark.parametrize("box", [True, False])
def test_contacts_use_native_periodic_images_and_report_missing_box_fallback(case, box):
    view, _, panel = case
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm").copy()
    xyz[:, 0] = [0.1, 0, 0]
    xyz[:, 1] = [0.9, 0, 0]
    view.molsys.structures.coordinates = puw.quantity(xyz, "nm")
    view.molsys.structures.box = (
        puw.quantity(np.tile(np.eye(3), (3, 1, 1)), "nm") if box else None
    )
    before = snapshot(view)
    result = calculate(
        case,
        "contacts",
        a={**A, "indices": "0"},
        b={**B, "indices": "1"},
        cutoff="0.25",
        pbc=True,
    )
    np.testing.assert_array_equal(
        panel._report.values, np.full((3, 1, 1), box, dtype=bool)
    )
    assert result["report"]["requested_pbc"] is True
    assert result["report"]["periodic"] is box
    assert all(row[3] is box for row in result["page"]["rows"])
    unchanged(view, before)


def test_contacts_preserve_native_resident_output_budget_refusal(case):
    view, sent, panel = case
    before = snapshot(view)
    with msm.configure.context(max_ram_usage=2):
        result = act(
            view,
            sent,
            draft=A,
            second=B,
            parameters={"task": "contacts", "structures": "all"},
        )
    assert result["stage"] == "error" and "budget" in result["message"].lower()
    assert result["report"] is None and panel._report is None
    unchanged(view, before)
