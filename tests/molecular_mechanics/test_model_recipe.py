"""Requested model controls must be consumed or rejected before engine use."""

import numpy as np
import pytest

import molsysmt as msm


def _model():
    model = msm.convert(msm.systems["alanine dipeptide"]["alanine_dipeptide.h5msm"])
    model.molecular_mechanics.implicit_solvent = "OBC2"
    return model


@pytest.mark.parametrize("route", ["system", "context", "energy", "forces"])
def test_unused_native_model_control_is_refused(route):
    model = _model()
    model.molecular_mechanics.solute_dielectric = 2.0
    before = msm.pyunitwizard.get_value(
        model.structures.coordinates, to_unit="nm"
    ).copy()
    with pytest.raises(msm.NotImplementedMethodError, match="solute_dielectric"):
        if route == "system":
            msm.convert(model, to_form="openmm.System")
        elif route == "context":
            msm.convert(model, to_form="openmm.Context", platform="CPU")
        elif route == "energy":
            msm.molecular_mechanics.get_potential_energy(model, platform="CPU")
        else:
            msm.molecular_mechanics.get_forces(model, platform="CPU")
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(model.structures.coordinates, to_unit="nm"), before
    )


def test_recipe_reads_the_compiled_model_and_preserves_the_source():
    import openmm.app as app

    model = _model()
    model.molecular_mechanics.constraints = "all_bonds"
    before = model.copy()
    recipe = msm.molecular_mechanics.get_model_recipe(model)
    topology = msm.convert(model, to_form="openmm.Topology")
    reference = app.ForceField("amber14-all.xml", "implicit/obc2.xml").createSystem(
        topology, nonbondedMethod=app.NoCutoff, constraints=app.AllBonds
    )
    assert recipe["schema"] == "molsysmt.model_recipe@1"
    assert recipe["requested"]["constraints"] == dict(
        value="all_bonds", origin="stored"
    )
    assert recipe["effective"]["n_constraints"] == reference.getNumConstraints()
    assert recipe["effective"]["n_particles"] == reference.getNumParticles() == 22
    assert recipe["effective"]["nonbonded"][0]["method"] == "no_cutoff"
    assert recipe["resources"] == ["amber14-all.xml", "implicit/obc2.xml"]
    assert recipe["source_structure_indices"].tolist() == [0]
    assert recipe["software"]["openmm"]
    assert model.chemical_states._inventory_equals(before.chemical_states)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(model.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(before.structures.coordinates, to_unit="nm"),
    )
    assert model.molecular_mechanics.to_dict() == before.molecular_mechanics.to_dict()


def test_existing_system_keeps_unknown_construction_provenance_and_creates_no_context(
    monkeypatch,
):
    import openmm

    system = openmm.System()
    system.addParticle(1.0)
    force = openmm.NonbondedForce()
    force.addParticle(0.0, 0.2, 0.0)
    force.setNonbondedMethod(openmm.NonbondedForce.CutoffNonPeriodic)
    force.setCutoffDistance(0.75)
    system.addForce(force)

    def forbidden(*args, **kwargs):
        pytest.fail("Model inspection must not create an execution Context")

    monkeypatch.setattr(openmm.Context, "__init__", forbidden)
    recipe = msm.molecular_mechanics.get_model_recipe(system)
    assert recipe["requested"] == {}
    assert recipe["consumed_controls"] == []
    assert recipe["provenance"] == "provided_parameterized_model"
    assert recipe["effective"]["nonbonded"][0]["method"] == "cutoff_nonperiodic"
    assert (
        msm.pyunitwizard.get_value(
            recipe["effective"]["nonbonded"][0]["cutoff_distance"], to_unit="nm"
        )
        == 0.75
    )


def test_model_length_units_follow_the_application_policy():
    import openmm

    system = openmm.System()
    system.addParticle(1.0)
    force = openmm.NonbondedForce()
    force.addParticle(0.0, 0.2, 0.0)
    force.setNonbondedMethod(openmm.NonbondedForce.CutoffNonPeriodic)
    force.setCutoffDistance(0.75)
    system.addForce(force)
    puw = msm.pyunitwizard
    with puw.context(standard_units=["pm", "ps", "Da", "K", "e", "radians"]):
        recipe = msm.molecular_mechanics.get_model_recipe(system)
        cutoff = recipe["effective"]["nonbonded"][0]["cutoff_distance"]
        assert puw.get_unit(cutoff) == puw.unit("pm")
        assert puw.get_value(cutoff, to_unit="nm") == 0.75


@pytest.mark.parametrize("indices", [[-1], [1], [0, 0], [0.2], []])
def test_recipe_structure_scope_is_one_valid_context(indices):
    with pytest.raises(msm.ArgumentError):
        msm.molecular_mechanics.get_model_recipe(_model(), structure_indices=indices)


def test_optional_attribution_failure_preserves_the_completed_recipe(monkeypatch):
    import openmm

    from molsysmt import _ackredit
    from molsysmt._private.smonitor.warnings import AckreditTrackingWarning

    system = openmm.System()
    system.addParticle(1.0)

    def broken():
        raise RuntimeError("receiving attribution failure")

    monkeypatch.setattr(_ackredit, "backend", broken)
    with pytest.warns(AckreditTrackingWarning):
        recipe = msm.molecular_mechanics.get_model_recipe(system)
    assert recipe["effective"]["n_particles"] == 1
    assert recipe["attribution"]["items"][0]["roles"] == ["executed_software"]


@pytest.mark.parametrize(
    "control, value",
    [
        ("cutoff_distance", "0.8 nm"),
        ("salt_concentration", "0.1 mole/liter"),
        ("kappa", "1/nm"),
        ("solute_dielectric", 2.0),
        ("solvent_dielectric", 60.0),
        ("hydrogen_mass", "3 Da"),
        ("rigid_water", False),
        ("flexible_constraints", True),
    ],
)
def test_every_independent_unconsumed_physical_request_has_an_explicit_refusal(
    control, value
):
    model = _model()
    setattr(model.molecular_mechanics, control, value)
    with pytest.raises(msm.UnsupportedMechanicalControlError, match=control):
        msm.molecular_mechanics.get_model_recipe(model)


def test_chemical_assignments_are_not_silently_reinterpreted_as_forcefield_parameters():
    model = _model()
    model.molecular_mechanics.formal_charge = np.zeros(model.get(n_atoms=True))
    with pytest.raises(
        msm.UnsupportedMechanicalControlError, match="MolecularMechanics.formal_charge"
    ):
        msm.molecular_mechanics.get_model_recipe(model)


def test_competing_solvent_requests_are_not_both_reported_as_consumed():
    model = _model()
    model.molecular_mechanics.water_model = "TIP3P"
    with pytest.raises(msm.ArgumentConflictError, match="water_model"):
        msm.molecular_mechanics.get_model_recipe(model)


def test_constructed_obc_recipe_retains_the_executed_scientific_reference():
    recipe = msm.molecular_mechanics.get_model_recipe(_model())
    assert any(
        item["id"] == "doi:10.1002/prot.20033"
        and item["roles"] == ["scientific_criterion"]
        for item in recipe["attribution"]["items"]
    )


@pytest.mark.parametrize("kind", ["partial_charge", "atom_ff_type"])
def test_unconsumed_atom_parameters_are_not_silently_discarded(kind):
    model = _model()
    count = model.get(n_atoms=True)
    value = np.zeros(count) if kind == "partial_charge" else ["CT"] * count
    setattr(model.molecular_mechanics, kind, value)
    with pytest.raises(msm.UnsupportedMechanicalControlError, match=kind):
        msm.convert(model, to_form="openmm.System")


def test_inapplicable_global_water_default_is_not_a_second_solvent_request():
    model = _model()
    result = msm.molecular_mechanics.get_model_recipe(model)
    assert result["requested"]["water_model"] == {
        "value": None,
        "origin": "inapplicable_default",
        "inactive_default": "TIP3P",
    }
    assert model.molecular_mechanics.water_model is None


def test_compiled_periodic_box_uses_rows_and_the_active_length_policy():
    import openmm
    from openmm import unit

    system = openmm.System()
    system.addParticle(1.0)
    force = openmm.NonbondedForce()
    force.addParticle(0.0, 0.2, 0.0)
    force.setNonbondedMethod(force.CutoffPeriodic)
    system.addForce(force)
    rows = np.array([[3.0, 0, 0], [0.2, 3.2, 0], [0.1, 0.3, 3.4]])
    system.setDefaultPeriodicBoxVectors(*(rows * unit.nanometer))
    result = msm.molecular_mechanics.get_model_recipe(system)
    assert result["effective"]["periodic"]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result["effective"]["default_box"], to_unit="nm"),
        rows,
    )


def test_modular_file_reads_only_the_requested_structure_and_no_analyses(
    tmp_path, monkeypatch
):
    import h5py

    model = _model()
    model = msm.extract(model, structure_indices=[0, 0, 0])
    filename = str(tmp_path / "recipe.h5msm")
    msm.h5msm.write(model, filename, format_version="0.6")
    original = h5py.Dataset.__getitem__
    reads = []

    def read(dataset, key):
        if dataset.name.endswith("/coordinates"):
            reads.append(key)
            np.testing.assert_array_equal(key, [2])
        if "/interactions/" in dataset.name:
            pytest.fail("Model inspection must not load unrelated named analyses")
        return original(dataset, key)

    monkeypatch.setattr(h5py.Dataset, "__getitem__", read)
    result = msm.molecular_mechanics.get_model_recipe(filename, structure_indices=[2])
    assert result["source_structure_indices"].tolist() == [2]
    assert result["effective"]["n_particles"] == 22
    assert reads


def test_nonreference_structure_is_refused_without_changing_state():
    model = _model()
    state = model.chemical_states.append_state()
    msm.set(model, structure_chemical_state_index=[state])
    with pytest.raises(msm.ArgumentConflictError):
        msm.molecular_mechanics.get_model_recipe(model)
    assert model.chemical_states.reference_chemical_state_index == 0


def test_stored_requests_are_redigested_at_the_engine_boundary():
    model = _model()
    model.molecular_mechanics.constraints = "unknown"
    with pytest.raises(msm.ArgumentChoiceError, match="constraints"):
        msm.molecular_mechanics.get_model_recipe(model)
