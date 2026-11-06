"""Check actual OBC I forces rather than the presence of a solvent label."""

import json
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm

openmm = pytest.importorskip("openmm")
from openmm import app, unit  # noqa: E402

DATA = Path(__file__).parent / "data"
AMBER_FIELDS = [
    "AMBER14",
    "AMBER10",
    "AMBER03",
    "AMBER99SB",
    "AMBER99SBILDN",
    "AMBER99SBNMR",
    "AMBER96",
]


@pytest.fixture(scope="module")
def alanine_source():
    return msm.convert(app.PDBFile(str(DATA / "obc1_alanine.pdb")))


@pytest.mark.parametrize("forcefield", AMBER_FIELDS)
@pytest.mark.parametrize("model", ["OBC1", "OBC2"])
def test_requested_obc_model_constructs_the_selected_force(
    alanine_source, forcefield, model
):
    system = msm.convert(
        alanine_source,
        to_form="openmm.System",
        forcefield=forcefield,
        implicit_solvent=model,
    )
    solvent = [f for f in system.getForces() if isinstance(f, openmm.CustomGBForce)]
    assert len(solvent) == 1
    assert solvent[0].getNumParticles() == system.getNumParticles() == 22
    assert not any(isinstance(f, openmm.GBSAOBCForce) for f in system.getForces())
    name, expression, _ = solvent[0].getComputedValueParameters(1)
    assert name == "B"
    assert ("2.909125" in expression) == (model == "OBC1")
    assert ("4.85" in expression) == (model == "OBC2")


def _state(system, positions):
    integrator = openmm.VerletIntegrator(0.001 * unit.picoseconds)
    context = openmm.Context(
        system, integrator, openmm.Platform.getPlatformByName("Reference")
    )
    try:
        context.setPositions(positions)
        return context.getState(getEnergy=True, getForces=True)
    finally:
        del context, integrator


def test_obc1_matches_frozen_upstream_reference_forces(alanine_source):
    record = json.loads((DATA / "obc1_reference_forces.json").read_text())
    system = msm.convert(
        alanine_source,
        to_form="openmm.System",
        forcefield="AMBER96",
        implicit_solvent="OBC1",
        non_bonded_method="cutoff non-periodic",
        constraints=None,
    )
    coordinates = msm.get(alanine_source, coordinates=True)
    positions = msm.pyunitwizard.convert(coordinates[0], to_form="openmm.unit")
    state = _state(system, positions)
    actual = state.getForces(asNumpy=True).value_in_unit(
        unit.kilojoules_per_mole / unit.nanometer
    )
    expected = np.asarray(record["forces"])
    assert actual.shape == expected.shape == (22, 3)
    assert np.isfinite(
        state.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)
    )
    difference = np.linalg.norm(actual - expected, axis=1)
    tolerance = record["tolerance"]
    assert np.all(
        (difference < tolerance["absolute_vector_norm"])
        | (
            difference
            < tolerance["relative_vector_norm"] * np.linalg.norm(expected, axis=1)
        )
    )


@pytest.mark.parametrize("model", ["OBC1", "OBC2"])
def test_direct_topology_default_uses_no_cutoff_despite_box(alanine_source, model):
    from molsysmt.form.openmm_Topology.to_openmm_System import to_openmm_System

    top = msm.convert(alanine_source, to_form="openmm.Topology")
    top.setPeriodicBoxVectors(np.eye(3) * 4 * unit.nanometers)
    system = to_openmm_System(top, implicit_solvent=model)
    nb = next(f for f in system.getForces() if isinstance(f, openmm.NonbondedForce))
    gb = next(f for f in system.getForces() if isinstance(f, openmm.CustomGBForce))
    assert nb.getNonbondedMethod() == openmm.NonbondedForce.NoCutoff
    assert gb.getNonbondedMethod() == openmm.CustomGBForce.NoCutoff


@pytest.mark.parametrize("model", ["OBC1", "OBC2"])
@pytest.mark.parametrize("method", ["PME", "Ewald", "LJPME", "unknown"])
def test_incompatible_methods_fail_with_native_diagnostic(
    alanine_source, model, method
):
    from molsysmt._private.smonitor import ArgumentChoiceError

    with pytest.raises(ArgumentChoiceError, match="non_bonded_method"):
        msm.convert(
            alanine_source,
            to_form="openmm.System",
            implicit_solvent=model,
            non_bonded_method=method,
        )


@pytest.mark.parametrize("model", ["OBC1", "OBC2"])
def test_energy_forces_match_explicit_engine_recipe_and_distinguish_models(
    alanine_source, model
):
    top = msm.convert(alanine_source, to_form="openmm.Topology")
    positions = msm.pyunitwizard.convert(
        msm.get(alanine_source, coordinates=True)[0], to_form="openmm.unit"
    )
    actual = msm.convert(
        alanine_source, to_form="openmm.System", implicit_solvent=model
    )
    reference = app.ForceField(
        "amber14-all.xml", f"implicit/{model.lower()}.xml"
    ).createSystem(top, nonbondedMethod=app.NoCutoff, constraints=app.HBonds)
    observed, expected = _state(actual, positions), _state(reference, positions)
    np.testing.assert_allclose(
        observed.getForces(asNumpy=True).value_in_unit(
            unit.kilojoules_per_mole / unit.nanometer
        ),
        expected.getForces(asNumpy=True).value_in_unit(
            unit.kilojoules_per_mole / unit.nanometer
        ),
        rtol=1e-10,
        atol=1e-8,
    )
    assert observed.getPotentialEnergy().value_in_unit(
        unit.kilojoules_per_mole
    ) == pytest.approx(
        expected.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole), abs=1e-8
    )
    other = "OBC2" if model == "OBC1" else "OBC1"
    different = msm.convert(
        alanine_source, to_form="openmm.System", implicit_solvent=other
    )
    assert (
        abs(
            (
                observed.getPotentialEnergy()
                - _state(different, positions).getPotentialEnergy()
            ).value_in_unit(unit.kilojoules_per_mole)
        )
        > 0.01
    )


@pytest.mark.parametrize(
    "policy,engine_policy",
    [
        (None, None),
        ("none", None),
        ("hbonds", app.HBonds),
        ("all bonds", app.AllBonds),
        ("h angles", app.HAngles),
    ],
)
def test_constraint_policy_matches_the_requested_physical_constraints(
    alanine_source, policy, engine_policy
):
    top = msm.convert(alanine_source, to_form="openmm.Topology")
    result = msm.convert(alanine_source, to_form="openmm.System", constraints=policy)
    reference = app.ForceField("amber14-all.xml").createSystem(
        top, nonbondedMethod=app.NoCutoff, constraints=engine_policy
    )
    assert [
        result.getConstraintParameters(i) for i in range(result.getNumConstraints())
    ] == [
        reference.getConstraintParameters(i)
        for i in range(reference.getNumConstraints())
    ]


def test_unknown_constraint_policy_is_not_silently_replaced(alanine_source):
    from molsysmt._private.smonitor import ArgumentChoiceError

    with pytest.raises(ArgumentChoiceError, match="constraints"):
        msm.convert(alanine_source, to_form="openmm.System", constraints="unknown")


def test_attribution_distinguishes_models_engines_and_metadata_only_lookups(
    alanine_source,
):
    ackredit = pytest.importorskip("ackredit")
    paper = "doi:10.1002/prot.20033"
    with ackredit.session("implicit-solvent-workflow") as session:
        msm.molecular_mechanics.get_engine_forcefield(
            "AMBER14", implicit_solvent="OBC1"
        )
        assert not ackredit.get_used_items()
        for model in ["OBC1", "OBC2"]:
            with ackredit.capture(model) as run:
                result = msm.convert(
                    alanine_source, to_form="openmm.System", implicit_solvent=model
                )
            observed = run.attribution.to_dict()
            method = next(use for use in observed["uses"] if use["item_id"] == paper)
            assert method["roles"] == ["scientific_criterion"]
            assert method["context"]["implicit_solvent"] == model
            assert method["context"]["engine"] == "openmm"
            assert method["context"]["forcefield"] == "AMBER14"
            assert method["context"]["resources"][-1] == f"implicit/{model.lower()}.xml"
            assert any(
                item["id"] == f"software:openmm:{openmm.__version__}"
                for item in observed["items"]
            )
            assert ackredit.current_session() is session
        saved = openmm.XmlSerializer.serialize(result)
    with ackredit.session("reader"):
        restored = openmm.XmlSerializer.deserialize(saved)
        assert restored.getNumParticles() == 22
        assert not ackredit.get_used_items()


def test_failed_construction_does_not_credit_successful_model(alanine_source):
    ackredit = pytest.importorskip("ackredit")
    from molsysmt._private.smonitor import ArgumentChoiceError

    with ackredit.session("refused-model"):
        with pytest.raises(ArgumentChoiceError):
            msm.convert(
                alanine_source,
                to_form="openmm.System",
                implicit_solvent="OBC1",
                non_bonded_method="PME",
            )
        assert not ackredit.get_used_items()


def test_absent_ackredit_preserves_the_constructed_model(alanine_source, monkeypatch):
    import builtins

    from depdigest.core import checker

    original_find_spec, original_import = checker.find_spec, builtins.__import__

    def missing(name, *args, **kwargs):
        return None if name == "ackredit" else original_find_spec(name, *args, **kwargs)

    def guarded(name, *args, **kwargs):
        if name.split(".")[0] == "ackredit":
            raise AssertionError("Absent optional Ackredit must not be imported")
        return original_import(name, *args, **kwargs)

    try:
        monkeypatch.setattr(checker, "find_spec", missing)
        monkeypatch.setattr(builtins, "__import__", guarded)
        checker.is_installed.cache_clear()
        result = msm.convert(
            alanine_source, to_form="openmm.System", implicit_solvent="OBC1"
        )
        assert any(isinstance(f, openmm.CustomGBForce) for f in result.getForces())
    finally:
        monkeypatch.setattr(checker, "find_spec", original_find_spec)
        monkeypatch.setattr(builtins, "__import__", original_import)
        checker.is_installed.cache_clear()


def test_tracking_failure_keeps_completed_model_and_reports_diagnostic(
    alanine_source, monkeypatch
):
    from molsysmt import _ackredit
    from molsysmt._private.smonitor.warnings import AckreditTrackingWarning

    def fail():
        raise RuntimeError("unavailable attribution provider")

    monkeypatch.setattr(_ackredit, "backend", fail)
    with pytest.warns(
        AckreditTrackingWarning, match="unavailable attribution provider"
    ):
        result = msm.convert(
            alanine_source, to_form="openmm.System", implicit_solvent="OBC2"
        )
    assert any(isinstance(f, openmm.CustomGBForce) for f in result.getForces())


def test_nondefault_unit_policy_preserves_the_same_physical_model(alanine_source):
    puw = msm.pyunitwizard
    before = puw.configure.report()
    with puw.context(standard_units=["angstrom", "fs", "e", "kilocalorie/mole"]):
        policy = puw.configure.report()
        result = msm.convert(
            alanine_source,
            to_form="openmm.Context",
            implicit_solvent="OBC1",
            platform="CPU",
        )
        try:
            assert np.isfinite(
                result.getState(getEnergy=True)
                .getPotentialEnergy()
                .value_in_unit(unit.kilojoules_per_mole)
            )
            assert any(
                isinstance(f, openmm.CustomGBForce)
                for f in result.getSystem().getForces()
            )
            assert puw.configure.report() == policy
        finally:
            del result
    assert puw.configure.report() == before
