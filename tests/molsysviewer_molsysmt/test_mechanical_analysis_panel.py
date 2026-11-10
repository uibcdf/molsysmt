"""Review model requests before source-preserving mechanical observations."""

import json
import subprocess

import numpy as np
import pytest

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_analysis_panel import A, act
from tests.molsysviewer_molsysmt.test_analysis_panel import case as case
from tests.molsysviewer_molsysmt.test_build_assignment_tools import snapshot, unchanged
from tests.molsysviewer_molsysmt.test_molecular_mechanics_tools import (
    direct_openmm_energies,
    energy_units,
)

puw = msm.pyunitwizard


def review(case, task="potential_energy", **parameters):
    view, sent, _ = case
    response = act(
        view,
        sent,
        "review_model",
        draft=A,
        parameters={
            "task": task,
            "structures": "indices",
            "indices": "2",
            **parameters,
        },
    )
    assert response["stage"] == "review_model", response["message"]
    return response


def calculate(case, packet):
    view, sent, _ = case
    response = act(view, sent, review_token=packet["mechanical_review"]["token"])
    assert response["stage"] == "report", response["message"]
    return response


@pytest.mark.parametrize("task", ["potential_energy", "energy_terms"])
@pytest.mark.parametrize("length", ["nm", "pm"])
def test_energy_at_explicit_structure_matches_independent_openmm_and_units(
    case, task, length
):
    import openmm

    view, sent, panel = case
    before = snapshot(view)
    expected, terms = direct_openmm_energies(
        msm.extract(view.molsys, structure_indices=[2]), openmm, "Reference"
    )
    with puw.context(standard_units=[length, *energy_units("kcal/mol")[1:]]):
        policy = puw.configure.report()
        packet = review(case, task)
        model = {item["name"]: item for item in packet["mechanical_review"]["model"]}
        assert model["constraints"]["value"] == "hbonds"
        assert model["constraints"]["source"] == "native_default"
        assert model["time_step"]["unit"] == "ps"
        assert packet["mechanical_review"]["atom_count"] == view.molsys.get_n_atoms()
        packet = calculate(case, packet)
        assert packet["report"]["family"] == "mechanical"
        assert packet["report"]["structure_indices"] == [2]
        assert packet["report"]["unit"] == "kJ/mol"
        actual = dict(
            zip(panel._report.auxiliary["terms"], panel._report.values, strict=True)
        )
        if task == "potential_energy":
            assert actual["Total potential energy"] == pytest.approx(expected, rel=1e-9)
        else:
            assert actual == pytest.approx(terms, rel=1e-9)
            assert sum(actual.values()) == pytest.approx(expected, rel=1e-9)
        assert packet["report"]["software"]["openmm"] == openmm.__version__
        assert len(json.dumps(packet)) < 65536
        unchanged(view, before)
        assert puw.configure.report() == policy


@pytest.mark.parametrize("magnitude", [False, True])
@pytest.mark.parametrize("length", ["nm", "pm"])
def test_forces_keep_selected_source_axes_and_match_direct_engine(
    case, magnitude, length
):
    from openmm import Context, Platform, VerletIntegrator, app, unit

    view, sent, panel = case
    topology = msm.convert(
        msm.extract(view.molsys, structure_indices=[0]), to_form="openmm.Topology"
    )
    system = app.ForceField("amber14-all.xml", "amber14/tip3p.xml").createSystem(
        topology, nonbondedMethod=app.NoCutoff, constraints=app.HBonds
    )
    integrator = VerletIntegrator(0.001)
    context = Context(system, integrator, Platform.getPlatformByName("Reference"))
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm")
    expected = []
    try:
        for frame in [2, 0, 2]:
            context.setPositions(xyz[frame] * unit.nanometer)
            forces = (
                context.getState(getForces=True)
                .getForces(asNumpy=True)
                .value_in_unit(unit.kilojoule_per_mole / unit.nanometer)
            )
            expected.append(forces[[4, 0, 4]])
    finally:
        del context, integrator
    expected = np.asarray(expected)
    if magnitude:
        expected = np.linalg.norm(expected, axis=-1)
    before = snapshot(view)
    with puw.context(standard_units=[length, *energy_units("kcal/mol")[1:]]):
        packet = review(
            case,
            "forces",
            indices="2,0,2",
            force_output="magnitude" if magnitude else "components",
        )
        packet = calculate(case, packet)
        np.testing.assert_allclose(panel._report.values, expected, rtol=1e-9, atol=1e-8)
        assert packet["report"]["rows"] == 9
        assert packet["report"]["unit"] == "kJ/(mol*nm)"
        assert [row[:2] for row in packet["page"]["rows"]] == [
            [f, a] for f in [2, 0, 2] for a in [4, 0, 4]
        ]
        response = act(
            view,
            sent,
            "select_participants",
            report_id=panel._report.token,
            row_index=4,
        )
        assert response["stage"] == "scene", response["message"]
        assert view.active_selection.atom_indices == [0]
        act(view, sent, "clear")
        assert panel._report is None
        # Selection is a deliberate scene change; molecular data still match.
        from tests.molsysviewer_molsysmt.test_build_assignment_tools import same

        same(view.molsys, before[1])


def test_degrees_of_freedom_matches_particle_constraint_count(case):
    from openmm import app

    view, _, panel = case
    topology = msm.convert(
        msm.extract(view.molsys, structure_indices=[0]), to_form="openmm.Topology"
    )
    system = app.ForceField("amber14-all.xml", "amber14/tip3p.xml").createSystem(
        topology, nonbondedMethod=app.NoCutoff, constraints=app.HBonds
    )
    expected = 3 * system.getNumParticles() - system.getNumConstraints()
    before = snapshot(view)
    result = calculate(case, review(case, "mechanical_dof"))
    assert result["page"]["rows"][0][-1] == expected
    assert panel._report.values.tolist() == [expected]
    assert "not a thermodynamic" in result["report"]["notice"]
    unchanged(view, before)


@pytest.mark.parametrize(
    "task", ["potential_energy", "energy_terms", "forces", "mechanical_dof"]
)
def test_calculation_requires_matching_single_use_review(case, task):
    view, sent, panel = case
    before = snapshot(view)
    packet = act(view, sent, parameters={"task": task})
    assert packet["stage"] == "error" and "Review" in packet["message"]
    assert panel._report is None
    packet = review(case, task)
    token = packet["mechanical_review"]["token"]
    packet = act(view, sent, review_token=token + "wrong")
    assert packet["stage"] == "error"
    unchanged(view, before)
    packet = review(case, task)
    calculate(case, packet)
    packet = act(view, sent, review_token=packet["mechanical_review"]["token"])
    assert packet["stage"] == "error" and "Review" in packet["message"]
    unchanged(view, before)


@pytest.mark.parametrize("task", ["potential_energy", "energy_terms", "mechanical_dof"])
def test_legacy_single_structure_readers_refuse_ensemble_before_engine(case, task):
    view, sent, panel = case
    before = snapshot(view)
    response = act(
        view, sent, "review_model", parameters={"task": task, "structures": "all"}
    )
    assert (
        response["stage"] == "error" and "one explicit structure" in response["message"]
    )
    assert panel._mechanics_review is None and panel._report is None
    unchanged(view, before)


@pytest.mark.parametrize(
    "field,value",
    [
        ("solute_dielectric", 1.0),
        ("solvent_dielectric", 78.5),
        ("kappa", "0.1/nm"),
        ("salt_concentration", "0.1 mol/liter"),
        ("cutoff_distance", "1 nm"),
    ],
)
def test_unsupported_independent_controls_refuse_before_calculation(case, field, value):
    view, sent, panel = case
    setattr(view.molsys.molecular_mechanics, field, value)
    before = snapshot(view)
    response = act(view, sent, "review_model", parameters={"task": "potential_energy"})
    assert response["stage"] == "error" and "#582" in response["message"]
    assert panel._report is None
    unchanged(view, before)


def test_changed_native_default_invalidates_review_without_mutation(case):
    view, sent, panel = case
    packet = review(case)
    before = snapshot(view)
    original = msm.configure.default_attribute["temperature"]
    try:
        msm.configure.default_attribute["temperature"] = "310 K"
        response = act(view, sent, review_token=packet["mechanical_review"]["token"])
        assert response["stage"] == "error" and "changed" in response["message"]
        assert panel._report is None
        unchanged(view, before)
    finally:
        msm.configure.default_attribute["temperature"] = original


@pytest.mark.parametrize(
    "parameters",
    [
        {"mechanical_platform": "CUDA"},
        {"mechanical_platform": []},
        {"force_output": "sum"},
        {"force_output": None},
    ],
)
def test_invalid_model_controls_reject_at_panel_boundary(case, parameters):
    view, sent, _ = case
    before = snapshot(view)
    response = act(
        view, sent, "review_model", parameters={"task": "forces", **parameters}
    )
    assert response["stage"] == "error"
    unchanged(view, before)


def test_mechanical_frontend_is_valid_esm_and_does_not_execute_on_family_change(
    tmp_path,
):
    from molsysviewer_molsysmt._analysis_panel_frontend import ESM

    module = tmp_path / "mechanical.mjs"
    module.write_text(ESM)
    subprocess.run(
        ["node", "--check", str(module)], check=True, capture_output=True, text=True
    )
