"""Native report colors and scalar series adopt only explicit compatible axes."""

from copy import deepcopy

import molsysviewer as msv
import numpy as np
import pytest
from molsysviewer.colors import scalar_to_color_list

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_analysis_panel import A, B, act, calculate
from tests.molsysviewer_molsysmt.test_analysis_panel import case as case
from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
    same,
    snapshot,
    unchanged,
)
from tests.molsysviewer_molsysmt.test_property_analysis_panel import ATOMS

puw = msm.pyunitwizard


def property_result(case, task="mass", **parameters):
    view, sent, panel = case
    response = act(view, sent, draft=ATOMS, parameters={"task": task, **parameters})
    assert response["stage"] == "report", response["message"]
    return response


@pytest.mark.parametrize("policy", ["nm", "pm"])
@pytest.mark.parametrize("palette", ["viridis", "blue_red"])
def test_quantity_colors_use_exact_destination_order_units_and_one_core_undo(
    case, policy, palette
):
    view, sent, panel = case
    region = view.regions.add(
        selection=[20, 6, 10], tag="property", representation="ball-and-stick"
    )
    region.set_color("green")
    before_colors = deepcopy(view._atom_color_layers)
    with puw.context(standard_units=[policy, "ps", "dalton", "radians"]):
        property_result(case)
        report = panel._report
        values = {
            int(a): float(v) for a, v in zip(report.first, report.values, strict=True)
        }
        expected = scalar_to_color_list(
            puw.quantity([values[a] for a in region.atom_indices], "dalton"),
            palette="viridis"
            if palette == "viridis"
            else ["#2166ac", "#f7f7f7", "#b2182b"],
            value_range=puw.quantity([0, 20], "dalton"),
        )
        source = snapshot(view)
        response = act(
            view,
            sent,
            "apply_report_colors",
            report_id=report.token,
            row_index=0,
            visual_options={
                "destination": "region",
                "region": "property",
                "palette": palette,
                "range": "manual",
                "minimum": "0",
                "maximum": "20",
            },
        )
        assert response["stage"] == "scene", response["message"]
        assert "fixed color snapshot" in response["message"]
        assert view._atom_color_layers["property"] == dict(
            zip(region.atom_indices, expected, strict=True)
        )
        assert view._atom_color_layers.get("whole") == before_colors.get("whole")
        assert panel._report is report
        same(view.molsys, source[1])
        assert view.history.undo()
        assert view._atom_color_layers == before_colors
        assert view.history.redo()
        assert view._atom_color_layers["property"] == dict(
            zip(region.atom_indices, expected, strict=True)
        )
        act(view, sent, "clear")
        assert panel._report is None
        assert view._atom_color_layers["property"] == dict(
            zip(region.atom_indices, expected, strict=True)
        )


@pytest.mark.parametrize(
    "options",
    [
        {},
        {"destination": "region", "region": "missing"},
        {"destination": "region", "region": "chosen"},
        {"palette": "unknown"},
        {"range": "manual", "minimum": "nan"},
        {"range": "manual", "minimum": "20", "maximum": "1"},
        {"region": "x" * 201},
        {"extra": True},
    ],
)
def test_color_adoption_refuses_incomplete_scope_or_invalid_fields_without_mutation(
    case, options
):
    view, sent, panel = case
    response = property_result(case)
    before = snapshot(view)
    response = act(
        view,
        sent,
        "apply_report_colors",
        report_id=response["report"]["id"],
        row_index=0,
        visual_options=options,
    )
    assert response["stage"] == "error"
    unchanged(view, before)


def test_sasa_colors_use_selected_observation_and_remain_static_across_navigation(case):
    view, sent, panel = case
    view.regions.add(selection=[6, 10, 20], tag="surface")
    property_result(case, "sasa", structures="all")
    report = panel._report
    mapping = dict(zip(report.first, report.values[1], strict=True))
    region = view.regions["surface"]
    expected = scalar_to_color_list(
        puw.quantity([mapping[a] for a in region.atom_indices], "nm**2")
    )
    response = act(
        view,
        sent,
        "apply_report_colors",
        report_id=report.token,
        row_index=4,
        visual_options={"destination": "region", "region": "surface"},
    )
    assert response["stage"] == "scene", response["message"]
    assert response["scene_action"]["observation_structure_index"] == 1
    assert view._atom_color_layers["surface"] == dict(
        zip(region.atom_indices, expected, strict=True)
    )
    before = deepcopy(view._atom_color_layers)
    view.player.go_to_structure(2)
    assert view._atom_color_layers == before


@pytest.mark.parametrize("task", ["distances", "vectors", "angles", "torsions", "sasa"])
@pytest.mark.parametrize("policy", ["nm", "pm"])
def test_selected_series_preserves_native_scope_units_and_core_ownership(
    case, task, policy
):
    view, sent, panel = case
    with puw.context(standard_units=[policy, "ps", "radians"]):
        result = (
            calculate(
                case,
                task,
                a=A,
                b=B,
                structures="all",
                atom_tuples="[[0,1,2],[2,3,4]]"
                if task == "angles"
                else "[[0,1,2,3],[2,3,4,5]]"
                if task == "torsions"
                else "",
            )
            if task != "sasa"
            else property_result(case, "sasa", structures="all")
        )
        report = panel._report
        assert not result["report"]["selected_plot_unavailable"]
        source = snapshot(view)
        if task == "sasa":
            expected, unit = report.values[:, 0], "nm**2"
        else:
            _, a, b, _ = panel._row(0)
            native = (
                report.native_values[:, a]
                if task in {"angles", "torsions"}
                else report.native_values[:, a, b]
            )
            unit = "degrees" if task in {"angles", "torsions"} else "nm"
            expected = puw.get_value(puw.quantity(native, report.unit), to_unit=unit)
            if task == "vectors":
                expected = expected[:, 2]
        response = act(
            view,
            sent,
            "add_result_plot",
            report_id=report.token,
            row_index=0,
            plot_component="z",
        )
        assert response["stage"] == "scene", response["message"]
        record = view.trajectory_plot.records()[0]
        assert record["tag"] == response["scene_action"]["plot_tag"]
        assert record["x_label"] == "Structure index" and unit in record["y_label"]
        np.testing.assert_allclose(record["series"][0]["values"], expected, atol=1e-12)
        assert view.player.index == 0 and panel._report is report
        same(view.molsys, source[1])
        act(view, sent, "clear")
        assert len(view.trajectory_plot.records()) == 1


@pytest.mark.parametrize("task", ["distances", "vectors", "angles", "torsions", "sasa"])
def test_noncanonical_structure_series_is_not_reordered_filled_or_deduplicated(
    case, task
):
    view, sent, panel = case
    result = (
        calculate(
            case,
            task,
            atom_tuples="[[0,1,2]]"
            if task == "angles"
            else "[[0,1,2,3]]"
            if task == "torsions"
            else "",
        )
        if task != "sasa"
        else property_result(case, "sasa", structures="indices", indices="2,0,2")
    )
    assert "every loaded structure" in result["report"]["selected_plot_unavailable"]
    before = snapshot(view)
    response = act(
        view, sent, "add_result_plot", report_id=result["report"]["id"], row_index=0
    )
    assert response["stage"] == "error"
    unchanged(view, before)


def test_static_tables_do_not_become_trajectory_series_and_state_retains_colors(
    case, tmp_path
):
    view, sent, panel = case
    view.regions.add(selection=[6, 10, 20], tag="property")
    result = property_result(case)
    response = act(
        view, sent, "add_result_plot", report_id=result["report"]["id"], row_index=0
    )
    assert response["stage"] == "error" and "no compatible" in response["message"]
    response = act(
        view,
        sent,
        "apply_report_colors",
        report_id=result["report"]["id"],
        row_index=0,
        visual_options={"destination": "region", "region": "property"},
    )
    assert response["stage"] == "scene", response["message"]
    state = view.export_state()
    with msv.new_view(view.molsys) as recovered:
        recovered.import_state(state)
        assert recovered._atom_color_layers == view._atom_color_layers
        assert not recovered.trajectory_plot.records()


@pytest.mark.parametrize(
    "options",
    [
        {"range": "manual", "minimum": "nan"},
        {"range": "manual", "minimum": "20", "maximum": "1"},
        {"range": "manual", "minimum": "0", "maximum": "inf"},
        {"palette": "missing"},
    ],
)
def test_color_ranges_are_validated_on_a_fully_covered_destination(case, options):
    view, sent, panel = case
    view.regions.add(selection=[6, 10, 20], tag="covered")
    result = property_result(case)
    before = snapshot(view)
    response = act(
        view,
        sent,
        "apply_report_colors",
        report_id=result["report"]["id"],
        row_index=0,
        visual_options={"destination": "region", "region": "covered", **options},
    )
    assert response["stage"] == "error" and (
        "bound" in response["message"] or "scale" in response["message"]
    )
    unchanged(view, before)


@pytest.mark.parametrize("task", ["minimum", "maximum"])
def test_extreme_plot_keeps_native_extreme_per_structure_without_freezing_one_pair(
    case, task
):
    view, sent, panel = case
    result = calculate(case, task, structures="all")
    expected = puw.get_value(panel._report.values, to_unit="nm")
    response = act(
        view, sent, "add_result_plot", report_id=result["report"]["id"], row_index=0
    )
    assert response["stage"] == "scene", response["message"]
    record = view.trajectory_plot.records()[0]
    np.testing.assert_allclose(record["series"][0]["values"], expected)
    assert "each structure" in record["title"]


def test_undefined_native_angles_are_not_zero_filled_for_plotting(case):
    view, sent, panel = case
    result = calculate(case, "angles", structures="all", atom_tuples="[[0,0,1]]")
    assert any("undefined" in row for row in result["page"]["rows"])
    before = snapshot(view)
    response = act(
        view, sent, "add_result_plot", report_id=result["report"]["id"], row_index=0
    )
    assert response["stage"] == "error" and "finite scalar" in response["message"]
    unchanged(view, before)


@pytest.mark.parametrize("policy", ["nm", "pm"])
def test_rmsf_colors_retain_length_units_and_independent_fluctuation_values(
    case, policy
):
    view, sent, panel = case
    view.regions.add(selection=[0, 4], tag="fluctuations")
    with puw.context(standard_units=[policy, "ps", "radians"]):
        result = calculate(case, "rmsf", structures="all")
        atoms = panel._report.first
        xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[:, atoms]
        expected_values = np.sqrt(
            np.mean(np.sum((xyz - xyz.mean(axis=0)) ** 2, axis=-1), axis=0)
        )
        by_atom = dict(zip(atoms, expected_values, strict=True))
        scope = view.regions["fluctuations"].atom_indices
        expected = scalar_to_color_list(puw.quantity([by_atom[a] for a in scope], "nm"))
        response = act(
            view,
            sent,
            "apply_report_colors",
            report_id=result["report"]["id"],
            row_index=0,
            visual_options={"destination": "region", "region": "fluctuations"},
        )
        assert response["stage"] == "scene", response["message"]
        assert view._atom_color_layers["fluctuations"] == dict(
            zip(scope, expected, strict=True)
        )
