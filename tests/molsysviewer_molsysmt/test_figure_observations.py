"""Native recipes remain with figures after their mounted reports are cleared."""

import json
from copy import deepcopy

import numpy as np
import pytest

import molsysmt as msm
from molsysviewer_molsysmt._figure_observation import (
    encode,
    ordered_indices,
    plot_context,
)
from tests.molsysviewer_molsysmt.test_analysis_panel import A, act, calculate
from tests.molsysviewer_molsysmt.test_analysis_panel import case as case


def indices(record):
    # Independent expansion of the documented wire grammar, not its encoder.
    assert record["encoding"] == "ordered_arithmetic_runs@1"
    result = [
        start + offset * step
        for start, step, count in record["runs"]
        for offset in range(count)
    ]
    assert len(result) == record["length"]
    return result


def test_ordered_population_encoding_preserves_repetitions_and_is_sparse():
    for values in [[], [4], [4, 0, 4], [8, 3, 3, 0], [0, 1, 2, 7, 7]]:
        assert indices(ordered_indices(values)) == values
    assert len(json.dumps(ordered_indices(np.arange(100_000)))) < 150
    encoded = encode(np.array([-0.0, 1.0, np.nextafter(1.0, 2.0)]))
    assert encoded["encoding"] == "binary64_array_hex@1"
    assert [float.fromhex(item).hex() for item in encoded["values"]] == [
        float(value).hex() for value in [-0.0, 1.0, np.nextafter(1.0, 2.0)]
    ]


@pytest.mark.parametrize("length,mass_unit", [("nm", "dalton"), ("pm", "kg")])
def test_weighted_native_figure_has_exact_forwarded_masses_units_and_independent_values(
    case, length, mass_unit
):
    view, sent, panel = case
    puw = msm.pyunitwizard
    with puw.context(standard_units=[length, "ps", mass_unit, "radians"]):
        before = puw.get_value(view.molsys.structures.coordinates, to_unit="nm").copy()
        result = calculate(case, "gyration", structures="all", weighting="masses")
        report = panel._report
        reply = act(view, sent, "add_structure_plot", report_id=result["report"]["id"])
        assert reply["stage"] == "scene", reply["message"]
        series = view.trajectory_plot.records()[0]["series"][0]
        context = series["observation"]
        assert context["schema"] == "molsysmt.figure_observation@1"
        assert context["method"] == "molsysmt.structure.get_radius_of_gyration"
        assert indices(context["populations"]["first"]) == [4, 0, 4]
        assert indices(context["structure_indices"]) == [0, 1, 2]
        weight_record = puw.QuantityRecord.from_dict(
            context["arguments"]["weights"]["quantity_record"]
        )
        weight_quantity = weight_record.to_quantity(
            field="molsysmt.figure.arguments.weights", unit=mass_unit
        )
        weights = np.asarray(puw.get_value(weight_quantity, to_unit=mass_unit))
        masses = msm.physchem.get_mass(view.molsys, selection=[4, 0, 4], element="atom")
        np.testing.assert_array_equal(weights, puw.get_value(masses))
        assert context["mass_sources"]["weights"]["unit"] == str(puw.get_unit(masses))
        assert "unit" in context["arguments"]["weights"]["quantity_record"]["manifest"]
        assert context["arguments"]["weights"]["forwarded_as"] == "raw_numeric_weights"
        selected = before[:, [4, 0, 4]]
        centers = np.average(selected, axis=1, weights=weights)
        expected = np.sqrt(
            np.average(
                np.sum((selected - centers[:, None]) ** 2, axis=2),
                axis=1,
                weights=weights,
            )
        )
        np.testing.assert_allclose(series["values"], expected, rtol=2e-12, atol=1e-12)
        assert context["units"]["displayed"] == "nm"
        assert puw.are_compatible(
            puw.quantity(1, context["units"]["native"]), puw.quantity(1, length)
        )
        assert context["source"]["correspondence"] == "declared_not_authenticated"
        assert context["source"]["raw_edits_observed"] is False
        assert context["source"]["managed_revision"] == report.revision
        retained = deepcopy(view.trajectory_plot.records())
        report.calculation_context["arguments"].clear()
        assert view.trajectory_plot.records() == retained
        act(view, sent, "clear")
        assert panel._report is None and view.trajectory_plot.records() == retained
        np.testing.assert_array_equal(
            puw.get_value(view.molsys.structures.coordinates, to_unit="nm"), before
        )


def test_exact_reference_population_and_historical_rows_survive_repeated_extraction(
    case,
):
    view, sent, panel = case
    second = dict(A, indices="5 2 5")
    result = calculate(
        case,
        "rmsd",
        b=second,
        structures="all",
        reference_population="second",
        reference_structure="2",
    )
    reply = act(view, sent, "add_structure_plot", report_id=result["report"]["id"])
    assert reply["stage"] == "scene", reply["message"]
    context = view.trajectory_plot.records()[0]["series"][0]["observation"]
    assert indices(context["reference"]["atom_indices"]) == [5, 2, 5]
    assert context["reference"]["structure_index"] == 2
    assert indices(context["arguments"]["selection"]) == [4, 0, 4]
    assert indices(context["arguments"]["reference_selection"]) == [5, 2, 5]
    with view.extract(structure_indices=[2, 0, 0]) as extracted:
        retained = extracted.trajectory_plot.records()[0]["series"][0]
        assert retained["observation"] == context
        assert retained["observation_rows"] == [2, 0, 0]


def test_nonconsecutive_and_repeated_coverage_is_not_rewritten_for_display(case):
    view, sent, panel = case
    result = calculate(case, "gyration", weighting="masses")
    context = plot_context(panel._report, "nm", {"kind": "structure_scalar"})
    assert indices(context["structure_indices"]) == [2, 0, 2]
    before = view.trajectory_plot.records()
    reply = act(view, sent, "add_structure_plot", report_id=result["report"]["id"])
    assert reply["stage"] == "error" and view.trajectory_plot.records() == before


def test_two_large_exact_mass_vectors_fit_core_record_limits_without_a_new_codec():
    from molsysviewer._private.figure_observation import normalize_observation

    puw = msm.pyunitwizard
    raw = np.tile(np.array([12.011, 1.008, 15.999], dtype=np.float64), 35_000)
    encoded = encode(
        puw.quantity(raw, "dalton"), field="molsysmt.figure.arguments.weights"
    )
    decoded = puw.QuantityRecord.from_dict(encoded["quantity_record"]).to_quantity(
        field="molsysmt.figure.arguments.weights", unit="dalton"
    )
    np.testing.assert_array_equal(puw.get_value(decoded, to_unit="dalton"), raw)
    encoded_second = encode(
        puw.quantity(raw, "dalton"), field="molsysmt.figure.arguments.weights_2"
    )
    decoded_second = puw.QuantityRecord.from_dict(
        encoded_second["quantity_record"]
    ).to_quantity(field="molsysmt.figure.arguments.weights_2", unit="dalton")
    np.testing.assert_array_equal(puw.get_value(decoded_second, to_unit="dalton"), raw)
    context = {
        "schema": "molsysmt.figure_observation@1",
        "arguments": {"weights": encoded, "weights_2": encoded_second},
    }
    retained = normalize_observation(context)
    assert retained == context
    assert "base64" in retained["arguments"]["weights"]["quantity_record"]["values"]
