"""Compare compact model inspection with independently constructed engine truth."""

import numpy as np
import pytest

import molsysmt as msm


@pytest.mark.parametrize("policy", ["hbonds", "all_bonds", "none"])
def test_recipe_constraints_match_independent_engine_construction(policy):
    from openmm import app

    model = msm.convert(msm.systems["alanine dipeptide"]["alanine_dipeptide.h5msm"])
    model.molecular_mechanics.constraints = policy
    recipe = msm.molecular_mechanics.get_model_recipe(model)
    reference = app.ForceField("amber14-all.xml", "amber14/tip3p.xml").createSystem(
        msm.convert(model, to_form="openmm.Topology"),
        nonbondedMethod=app.NoCutoff,
        constraints={"hbonds": app.HBonds, "all_bonds": app.AllBonds, "none": None}[
            policy
        ],
    )
    assert recipe["effective"]["n_particles"] == reference.getNumParticles() == 22
    assert recipe["effective"]["n_constraints"] == reference.getNumConstraints()
    if policy == "none":
        assert recipe["effective"]["n_constraints"] == 0
    assert recipe["effective"]["nonbonded"][0]["method"] == "no_cutoff"


def test_recipe_retains_a_known_triclinic_physical_box():
    import openmm
    from openmm import unit

    system = openmm.System()
    system.addParticle(1.0)
    force = openmm.NonbondedForce()
    force.addParticle(0.0, 0.2, 0.0)
    force.setNonbondedMethod(force.CutoffPeriodic)
    force.setCutoffDistance(0.7)
    system.addForce(force)
    rows = np.array([[3.0, 0, 0], [0.2, 3.2, 0], [0.1, 0.3, 3.4]])
    system.setDefaultPeriodicBoxVectors(*(rows * unit.nanometer))
    result = msm.molecular_mechanics.get_model_recipe(system)["effective"]
    assert result["periodic"]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result["default_box"], to_unit="nm"),
        rows,
        rtol=0,
        atol=1e-13,
    )
    assert (
        msm.pyunitwizard.get_value(
            result["nonbonded"][0]["cutoff_distance"], to_unit="nm"
        )
        == 0.7
    )
