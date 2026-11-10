"""Native PCA spectra and feature coefficients through the real task protocol."""

import json
import subprocess

import numpy as np
import pytest

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_analysis_panel import FRAMES, A, act, calculate
from tests.molsysviewer_molsysmt.test_analysis_panel import case as case
from tests.molsysviewer_molsysmt.test_build_assignment_tools import snapshot, unchanged

puw = msm.pyunitwizard


@pytest.mark.parametrize("policy", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("weights", [None, [1, 4, 0]])
def test_pca_retains_native_axes_and_independent_population_covariance(
    case, policy, weights
):
    view, _, panel = case
    before = snapshot(view)
    atoms = [4, 0, 4]
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[FRAMES][
        :, atoms
    ]
    features = xyz.transpose(0, 2, 1).reshape(len(FRAMES), -1)
    factors = np.ones(3) if weights is None else np.asarray(weights)
    centered = (features - features.mean(axis=0)) * np.sqrt(np.tile(factors, 3))
    covariance = centered.T @ centered / len(FRAMES)
    with puw.context(standard_units=[policy, "ps"]):
        active = puw.configure.report()
        result = calculate(
            case,
            "pca",
            pca_weighting="uniform" if weights is None else "custom",
            pca_weights="" if weights is None else json.dumps(weights),
        )
        assert puw.configure.report() == active
    report = panel._report
    values = puw.get_value(report.values, to_unit="nm**2")
    vectors = report.auxiliary
    np.testing.assert_allclose(vectors @ vectors.T, np.eye(9), atol=1e-12)
    np.testing.assert_allclose(covariance @ vectors.T, vectors.T * values, atol=1e-12)
    np.testing.assert_allclose(
        vectors.T @ np.diag(values) @ vectors, covariance, atol=1e-12
    )
    np.testing.assert_allclose(values, np.linalg.eigvalsh(covariance)[::-1], atol=1e-12)
    assert result["report"]["result_axis"] == "mode"
    assert result["report"]["family"] == "pca"
    assert result["report"]["structure_indices"] == FRAMES
    assert result["report"]["first_atoms"] == 3
    np.testing.assert_allclose(
        [float(row[1]) for row in result["page"]["rows"]], values, rtol=1e-8, atol=1e-12
    )
    assert result["page"]["columns"][-1] == "Eigenvalue (nm²)"
    unchanged(view, before)


def test_component_paging_reuses_arrays_preserves_repeated_atoms_and_expires_rows(case):
    view, sent, panel = case
    atoms = list(range(18)) + [0]
    draft = dict(A, indices=" ".join(map(str, atoms)))
    result = calculate(case, "pca", a=draft)
    original = panel._report
    assert result["page"]["total"] == 57 and len(result["page"]["rows"]) == 50
    page = act(view, sent, "page", report_id=original.token, offset=50)
    assert page["page"]["rows"][0][0] == 51
    result = act(view, sent, "component", report_id=original.token, component=0)
    assert result["report"]["id"] != original.token
    assert result["report"]["result_axis"] == "feature"
    assert panel._report.native_values is original.native_values
    assert result["page"]["offset"] == 0
    page = act(view, sent, "page", report_id=panel._report.token, offset=50)
    for position, row in enumerate(page["page"]["rows"], start=50):
        assert row[:4] == [
            1,
            "XYZ"[position // len(atoms)],
            position % len(atoms),
            atoms[position % len(atoms)],
        ]
        assert float(row[4]) == pytest.approx(
            original.auxiliary[0, position], rel=1e-8, abs=1e-12
        )
    rejected = act(
        view, sent, "select_participants", report_id=original.token, row_index=50
    )
    assert rejected["stage"] == "error" and "expired" in rejected["message"]
    selected = act(
        view, sent, "select_participants", report_id=panel._report.token, row_index=56
    )
    assert selected["stage"] == "scene"
    assert view.player.index == 0
    np.testing.assert_array_equal(view.active_selection.atom_indices, [0])


@pytest.mark.parametrize(
    "weights",
    ["[1]", "[-1, 1, 1]", "[0, 0, 0]", "[1, NaN, 1]", '"masses"', "{}", "[1, 2"],
)
def test_invalid_weights_reject_without_mutation_or_result(case, weights):
    view, sent, panel = case
    before = snapshot(view)
    result = act(
        view,
        sent,
        draft=A,
        parameters={"task": "pca", "pca_weighting": "custom", "pca_weights": weights},
    )
    assert result["stage"] == "error" and panel._report is None
    unchanged(view, before)


@pytest.mark.parametrize("component", [-1, 9, True, 1.5, "1", {}])
def test_invalid_components_keep_the_native_result(case, component):
    view, sent, panel = case
    result = calculate(case, "pca")
    before = snapshot(view)
    original = panel._report
    rejected = act(
        view, sent, "component", report_id=result["report"]["id"], component=component
    )
    assert rejected["stage"] == "error"
    assert panel._report is original
    unchanged(view, before)


def test_one_structure_zero_covariance_is_not_missing_or_a_structure_plot(case):
    view, sent, panel = case
    result = calculate(case, "pca", structures="current")
    np.testing.assert_array_equal(
        puw.get_value(panel._report.values, to_unit="nm**2"), np.zeros(9)
    )
    assert result["report"]["rows"] == 9
    assert result["report"]["plot_unavailable"]
    rejected = act(view, sent, "add_structure_plot", report_id=panel._report.token)
    assert rejected["stage"] == "error"
    assert not view.trajectory_plot.records()
    act(view, sent, "clear")
    assert panel._report is None


def test_pca_reads_explicit_pending_data_but_does_not_adopt_it(case):
    view, sent, panel = case
    tools = view.addons.molsysmt
    tools.basic.remove(selection=[1], in_place=True, update_view=False)
    before = puw.get_value(view.molsys.structures.coordinates, to_unit="nm").copy()
    status = tools.get_sync_status()
    assert status["state"] == "pending"
    result = calculate(case, "pca")
    assert result["report"]["source_revision"] == status["target_revision"]
    report = panel._report
    shown = act(view, sent, "component", report_id=report.token, component=0)
    assert shown["report"]["result_axis"] == "feature"
    rejected = act(
        view, sent, "focus_participants", report_id=panel._report.token, row_index=0
    )
    # The host rejects non-reader actions before invoking the panel handler.
    assert rejected["report"]["id"] == shown["report"]["id"]
    assert rejected["context"]["state"] == "pending"
    assert tools.get_sync_status() == status
    np.testing.assert_array_equal(
        puw.get_value(view.molsys.structures.coordinates, to_unit="nm"), before
    )


def test_clearing_pca_releases_the_native_coefficient_owner(case):
    import gc
    from weakref import ref

    view, sent, panel = case
    calculate(case, "pca")
    coefficients = ref(panel._report.auxiliary)
    act(view, sent, "clear")
    gc.collect()
    assert coefficients() is None


def test_pca_frontend_is_a_valid_module_and_names_units_and_axes():
    from molsysviewer_molsysmt._analysis_panel_frontend import ESM

    result = subprocess.run(
        ["node", "--input-type=module", "--check"],
        input=ESM,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    assert "data-pca-component" in ESM
    assert "dimensionless" in ESM and "nm²" in ESM
    assert "not structure indices" in ESM
