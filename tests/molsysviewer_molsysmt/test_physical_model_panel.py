"""Receive native compiled settings without changing science or scene ownership."""

import json

import numpy as np
import pytest

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_analysis_panel import act
from tests.molsysviewer_molsysmt.test_analysis_panel import case as case
from tests.molsysviewer_molsysmt.test_build_assignment_tools import snapshot, unchanged
from tests.molsysviewer_molsysmt.test_mechanical_analysis_panel import calculate, review


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_physical_recipe_has_native_origins_and_independent_compiled_counts(case, unit):
    from openmm import app

    view, _, panel = case
    before = snapshot(view)
    with msm.pyunitwizard.context(standard_units=[unit, "ps"]):
        packet = calculate(case, review(case, "model_recipe"))
    report = packet["report"]
    recipe = panel._report.native_values
    assert report["method"].endswith(".get_model_recipe")
    assert report["result_axis"] == "model" and report["platform"] is None
    assert report["physical_model"]["construction_structures"] == [2]
    assert recipe["source_structure_indices"].tolist() == [2]
    reference = app.ForceField("amber14-all.xml", "amber14/tip3p.xml").createSystem(
        msm.convert(view.molsys, to_form="openmm.Topology", structure_indices=[2]),
        nonbondedMethod=app.NoCutoff,
        constraints=app.HBonds,
    )
    assert recipe["effective"]["n_particles"] == reference.getNumParticles()
    assert recipe["effective"]["n_constraints"] == reference.getNumConstraints()
    assert recipe["effective"]["periodic"] is False
    assert recipe["effective"]["default_box"] is None
    rows = {r[1]: r[2:] for r in packet["page"]["rows"]}
    assert rows["Compiled: n_particles"][0] == str(reference.getNumParticles())
    assert rows["Requested: constraints"][-1] == "molsysmt_default"
    assert "Context" in report["physical_model"]["notice"]
    assert len(json.dumps(packet)) < 65536
    unchanged(view, before)


@pytest.mark.parametrize(
    "task", ["potential_energy", "energy_terms", "forces", "mechanical_dof"]
)
def test_every_mechanical_report_retains_separate_inspection_and_source_structure(
    case, task
):
    view, _, panel = case
    before = snapshot(view)
    response = calculate(case, review(case, task))
    physical = response["report"]["physical_model"]
    assert physical["method"] == "molsysmt.molecular_mechanics.get_model_recipe"
    assert physical["construction_structures"] == [2]
    assert physical["provenance"] == "constructed_from_declared_controls"
    assert (
        panel._report.auxiliary["native_physical_recipe"]["schema"]
        == "molsysmt.model_recipe@1"
    )
    assert "not a snapshot" in physical["notice"]
    unchanged(view, before)


def test_implicit_model_uses_native_inapplicable_water_default_for_degree_count(case):
    view, _, panel = case
    msm.set(view.molsys, implicit_solvent="OBC1")
    before = snapshot(view)
    response = calculate(case, review(case, "mechanical_dof"))
    recipe = panel._report.auxiliary["native_physical_recipe"]
    assert recipe["requested"]["water_model"]["origin"] == "inapplicable_default"
    assert recipe["requested"]["water_model"]["value"] is None
    assert response["page"]["rows"][0][-1] == (
        3 * recipe["effective"]["n_particles"] - recipe["effective"]["n_constraints"]
    )
    unchanged(view, before)


def test_model_recipe_requires_single_structure_and_expires_after_managed_edit(case):
    view, sent, panel = case
    response = act(
        view,
        sent,
        "review_model",
        parameters={"task": "model_recipe", "structures": "all"},
    )
    assert (
        response["stage"] == "error" and "one explicit structure" in response["message"]
    )
    assert panel._report is None
    calculate(case, review(case, "model_recipe"))
    retained = panel._report.native_values
    count = retained["effective"]["n_particles"]
    view.addons.molsysmt.structure.translate(translation="[1,0,0] nm", in_place=True)
    response = act(view, sent, "refresh")
    assert response["report"] is None
    assert retained["effective"]["n_particles"] == count
    assert panel._report is None


def test_periodic_physical_box_rows_are_explicit_nm_under_pm_policy(case):
    view, _, _ = case
    msm.set(
        view.molsys,
        box=msm.pyunitwizard.quantity(
            np.repeat((np.eye(3) * 3)[None], 3, axis=0), "nm"
        ),
        non_bonded_method="PME",
    )
    with msm.pyunitwizard.context(standard_units=["pm", "ps"]):
        response = calculate(case, review(case, "model_recipe"))
    rows = response["report"]["physical_model"]["rows"]
    box = next(row for row in rows if row[0] == "Compiled: default_box")
    assert box[2] == "nm"
    np.testing.assert_allclose(json.loads(box[1]), np.eye(3) * 3)
