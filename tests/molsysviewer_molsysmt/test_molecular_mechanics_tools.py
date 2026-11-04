"""Receive explicit force-field metadata and qualified mechanical degree counts."""

import inspect
import os
import subprocess
import sys

import molsysviewer as msv
import numpy as np
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from tests.molsysviewer_molsysmt.test_build_assignment_tools import snapshot, unchanged

NAMES = ("get_engine_forcefield", "get_degrees_of_freedom", "get_potential_energy")


def energy_units(energy_unit):
    # Context conversion also standardizes integrator temperature, friction and
    # other mechanical parameters, so supply a complete application policy.
    return [
        "angstrom",
        "ps",
        "radians",
        "dalton",
        "K",
        "mole",
        "e",
        "dimensionless",
        energy_unit,
    ]


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0]) as owner:
            yield owner


@pytest.fixture
def engine():
    return pytest.importorskip("openmm")


@pytest.fixture
def energy_engine(engine, monkeypatch):
    # Bound real CPU contexts in this test process; do not change backend or
    # scientific defaults in the facade or application configuration.
    monkeypatch.setenv("OPENMM_CPU_THREADS", "1")
    return engine


def direct_openmm_energies(molsys, engine):
    """Evaluate the complete NoCutoff model independently of MolSysMT mechanics."""
    from openmm import app, unit

    topology = msm.convert(molsys, to_form="openmm.Topology")
    system = app.ForceField("amber14-all.xml", "amber14/tip3p.xml").createSystem(
        topology, nonbondedMethod=app.NoCutoff, constraints=app.HBonds
    )
    for index, force in enumerate(system.getForces()):
        force.setForceGroup(index)
    integrator = engine.VerletIntegrator(0.001)
    context = engine.Context(
        system, integrator, engine.Platform.getPlatformByName("CPU"), {"Threads": "1"}
    )
    try:
        xyz = msm.pyunitwizard.get_value(molsys.structures.coordinates, to_unit="nm")
        context.setPositions(xyz[0] * unit.nanometer)
        total = (
            context.getState(getEnergy=True)
            .getPotentialEnergy()
            .value_in_unit(unit.kilojoule_per_mole)
        )
        terms = {
            force.getName(): context.getState(getEnergy=True, groups={index})
            .getPotentialEnergy()
            .value_in_unit(unit.kilojoule_per_mole)
            for index, force in enumerate(system.getForces())
        }
        return total, terms
    finally:
        del context
        del integrator


@pytest.mark.parametrize("name", NAMES)
def test_explicit_namespace_signatures_help_and_validation(name):
    with msv.new_view() as view:
        namespace = view.addons.molsysmt.molecular_mechanics
        method = getattr(namespace, name)
        native = inspect.signature(getattr(msm.molecular_mechanics, name))
        parameters = list(native.parameters.values())
        if name != "get_engine_forcefield":
            parameters = parameters[1:]
        assert inspect.signature(method) == native.replace(parameters=parameters)
        assert method.digestion_plan is not None
        assert "molecular_mechanics" in dir(view.addons.molsysmt)
        assert name in dir(namespace)
        assert not hasattr(view.addons.molsysmt, name)
        assert set(dir(namespace)) == set(NAMES)
        text = inspect.getdoc(method)
        assert "View integration" in text
        assert "\nmolecular_system :" not in text
        for parameter in parameters:
            assert f"{parameter.name} :" in text
        inputs = {} if name == "get_potential_energy" else {"forcefield": "AMBER14"}
        for extra in (
            {"molecular_system": None},
            {"update_view": True},
            {"structure_indices": [0]},
        ):
            with pytest.raises(UnknownArgumentError):
                method(**inputs, **extra)
        with pytest.raises(ArgumentError):
            method(**inputs, skip_digestion="yes")


@pytest.mark.parametrize("loaded", [False, True])
@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "parameters,expected",
    [
        ({"forcefield": "AMBER14"}, ["amber14-all.xml"]),
        (
            {"forcefield": "AMBER14", "water_model": "TIP3P"},
            ["amber14-all.xml", "amber14/tip3p.xml"],
        ),
        (
            {"forcefield": "AMBER99SB", "implicit_solvent": "OBC1"},
            ["amber99sb.xml", "amber99_obc.xml"],
        ),
        ({"forcefield": "AMBER14", "engine": "LEaP"}, ["leaprc.protein.ff14SB"]),
        (
            {"forcefield": "AMBER14", "engine": "LEaP", "water_model": "TIP3P"},
            ["leaprc.protein.ff14SB", "leaprc.water.tip3p"],
        ),
    ],
)
def test_resource_lookup_keeps_native_values_and_does_not_read_primary(
    loaded, skip, parameters, expected
):
    with msv.demo["pentalanine"] if loaded else msv.new_view() as view:
        before = snapshot(view)
        result = view.addons.molsysmt.molecular_mechanics.get_engine_forcefield(
            **parameters, skip_digestion=skip
        )
        assert result == expected
        assert result == msm.molecular_mechanics.get_engine_forcefield(
            **parameters, skip_digestion=skip
        )
        # Native return ownership is delegated; this test does not bless the
        # separately reported shared-list defect or mutate the provider registry.
        unchanged(view, before)


@pytest.mark.parametrize(
    "parameters",
    [
        {"forcefield": "not-a-forcefield"},
        {"forcefield": "AMBER14", "engine": "not-an-engine"},
        {"forcefield": "AMBER14", "water_model": "not-a-water-model"},
        {"forcefield": "AMBER14", "implicit_solvent": "not-a-solvent"},
        {"forcefield": []},
    ],
)
def test_resource_lookup_keeps_native_errors_without_an_engine_fallback(parameters):
    with msv.new_view() as view:
        before = snapshot(view)
        with pytest.raises(Exception) as native:
            msm.molecular_mechanics.get_engine_forcefield(**parameters)
        with pytest.raises(type(native.value)) as actual:
            view.addons.molsysmt.molecular_mechanics.get_engine_forcefield(**parameters)
        assert str(actual.value) == str(native.value)
        unchanged(view, before)


def test_resource_lookup_does_not_import_the_selected_engine_in_a_fresh_process():
    code = """
import sys
import molsysviewer as msv
with msv.new_view() as view:
    before = {name for name in sys.modules if name == 'openmm' or name.startswith('openmm.')}
    tools = view.addons.molsysmt.molecular_mechanics
    assert tools.get_engine_forcefield('AMBER14') == ['amber14-all.xml']
    assert tools.get_engine_forcefield('AMBER14', engine='LEaP') == ['leaprc.protein.ff14SB']
    after = {name for name in sys.modules if name == 'openmm' or name.startswith('openmm.')}
    assert after == before
"""
    result = subprocess.run(
        [sys.executable, "-c", code],
        text=True,
        capture_output=True,
        env=os.environ.copy(),
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("energy_unit", ["kJ/mol", "kcal/mol"])
def test_total_energy_matches_direct_openmm_under_application_policy(
    view, energy_engine, skip, energy_unit
):
    puw = msm.pyunitwizard
    expected, _ = direct_openmm_energies(view.molsys, energy_engine)
    with puw.context(standard_units=energy_units(energy_unit)):
        policy = dict(puw.configure.get_standard_units())
        before = snapshot(view)
        actual = view.addons.molsysmt.molecular_mechanics.get_potential_energy(
            skip_digestion=skip
        )
        assert puw.is_quantity(actual)
        assert np.shape(puw.get_value(actual)) == ()
        assert np.isfinite(puw.get_value(actual))
        np.testing.assert_allclose(
            puw.get_value(actual, to_unit="kJ/mol"), expected, rtol=1e-7, atol=1e-5
        )
        assert puw.get_unit(actual) == puw.get_unit(
            puw.standardize(puw.quantity(1, energy_unit))
        )
        assert dict(puw.configure.get_standard_units()) == policy
        unchanged(view, before)


@pytest.mark.parametrize("energy_unit", ["kJ/mol", "kcal/mol"])
def test_decomposition_matches_independent_force_groups_and_total(
    view, energy_engine, energy_unit
):
    puw = msm.pyunitwizard
    expected, terms = direct_openmm_energies(view.molsys, energy_engine)
    with puw.context(standard_units=energy_units(energy_unit)):
        before = snapshot(view)
        actual = view.addons.molsysmt.molecular_mechanics.get_potential_energy(
            decomposition=True
        )
        assert set(actual) == set(terms)
        values = {}
        for name, value in actual.items():
            assert puw.is_quantity(value)
            values[name] = float(puw.get_value(value, to_unit="kJ/mol"))
            assert np.isfinite(values[name])
            np.testing.assert_allclose(values[name], terms[name], rtol=1e-7, atol=1e-5)
        np.testing.assert_allclose(sum(values.values()), expected, rtol=1e-7, atol=1e-5)
        unchanged(view, before)


@pytest.mark.parametrize(
    "parameters",
    [
        {"selection": "all", "syntax": "MDTraj"},
        {"selection": list(range(62))},
        {"selection": np.arange(62, dtype=np.int64)},
    ],
)
def test_full_system_selection_forms_keep_energy_and_source(
    view, energy_engine, parameters
):
    puw = msm.pyunitwizard
    before = snapshot(view)
    actual = view.addons.molsysmt.molecular_mechanics.get_potential_energy(**parameters)
    expected, _ = direct_openmm_energies(view.molsys, energy_engine)
    np.testing.assert_allclose(
        puw.get_value(actual, to_unit="kJ/mol"), expected, rtol=1e-7, atol=1e-5
    )
    unchanged(view, before)


@pytest.mark.parametrize(
    "parameters",
    [
        {"platform": "Reference"},
        {"platform": "OpenCL"},
        {"platform": "not-a-platform"},
        {"engine": "not-an-engine"},
        {"selection": [0, 1]},
        {"selection": []},
    ],
)
def test_energy_native_rejections_do_not_prepare_or_update(
    view, energy_engine, parameters
):
    before = snapshot(view)
    with pytest.raises(Exception) as native:
        msm.molecular_mechanics.get_potential_energy(view.molsys, **parameters)
    with pytest.raises(type(native.value)) as actual:
        view.addons.molsysmt.molecular_mechanics.get_potential_energy(**parameters)
    assert str(actual.value) == str(native.value)
    unchanged(view, before)


def test_energy_reads_pending_geometry_without_synchronization(view, energy_engine):
    puw = msm.pyunitwizard
    tools = view.addons.molsysmt
    original = tools.molecular_mechanics.get_potential_energy()
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm").copy()
    xyz[:, 0, 0] += 0.01
    tools.basic.set(coordinates=puw.quantity(xyz, "nm"), update_view=False)
    assert tools.get_sync_status()["state"] == "pending"
    before = snapshot(view)
    actual = tools.molecular_mechanics.get_potential_energy()
    expected, _ = direct_openmm_energies(view.molsys, energy_engine)
    np.testing.assert_allclose(
        puw.get_value(actual, to_unit="kJ/mol"), expected, rtol=1e-7, atol=1e-5
    )
    assert not np.isclose(
        puw.get_value(actual, to_unit="kJ/mol"),
        puw.get_value(original, to_unit="kJ/mol"),
    )
    unchanged(view, before)


def test_cached_energy_uses_replacement_and_rejects_empty_closed_owners(
    view, energy_engine
):
    puw = msm.pyunitwizard
    method = view.addons.molsysmt.molecular_mechanics.get_potential_energy
    first = method()
    replacement = msm.convert(
        msm.systems["Trp-Cage"]["1l2y.h5msm"], structure_indices=0
    )
    view.load(replacement, mode="replace")
    before = snapshot(view)
    actual = method()
    expected, _ = direct_openmm_energies(view.molsys, energy_engine)
    np.testing.assert_allclose(
        puw.get_value(actual, to_unit="kJ/mol"), expected, rtol=1e-7, atol=1e-5
    )
    assert not np.isclose(
        puw.get_value(first, to_unit="kJ/mol"), puw.get_value(actual, to_unit="kJ/mol")
    )
    unchanged(view, before)
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method()
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty.addons.molsysmt.molecular_mechanics.get_potential_energy()


def test_multistructure_energy_keeps_native_rejection(energy_engine):
    with msv.demo["pentalanine"] as view:
        before = snapshot(view)
        with pytest.raises(Exception) as native:
            msm.molecular_mechanics.get_potential_energy(view.molsys)
        with pytest.raises(type(native.value)) as actual:
            view.addons.molsysmt.molecular_mechanics.get_potential_energy()
        assert str(actual.value) == str(native.value)
        unchanged(view, before)


@pytest.mark.parametrize("skip", [False, True])
def test_degrees_match_independent_openmm_particle_constraint_count(view, engine, skip):
    from openmm import app

    before = snapshot(view)
    topology = msm.convert(view.molsys, to_form="openmm.Topology")
    system = app.ForceField("amber14-all.xml").createSystem(
        topology, nonbondedMethod=app.NoCutoff, constraints=app.HBonds
    )
    assert system.getNumParticles() == 62
    assert system.getNumConstraints() == 32
    expected = 3 * system.getNumParticles() - system.getNumConstraints()
    value = view.addons.molsysmt.molecular_mechanics.get_degrees_of_freedom(
        skip_digestion=skip
    )
    assert type(value) is int
    assert value == expected == 154
    # Match the native mechanical definition, without inventing a thermal/COM
    # degree correction or adopting the independent OpenMM system.
    assert value == msm.molecular_mechanics.get_degrees_of_freedom(
        view.molsys, skip_digestion=skip
    )
    unchanged(view, before)


@pytest.mark.parametrize(
    "parameters",
    [
        {},
        {"water_model": "TIP3P"},
        {"implicit_solvent": "OBC1"},
        {"forcefield": "AMBER99SB"},
    ],
)
def test_degrees_forward_explicit_native_model_choices(view, engine, parameters):
    before = snapshot(view)
    assert view.addons.molsysmt.molecular_mechanics.get_degrees_of_freedom(
        **parameters
    ) == msm.molecular_mechanics.get_degrees_of_freedom(view.molsys, **parameters)
    unchanged(view, before)


@pytest.mark.parametrize(
    "parameters",
    [
        {"forcefield": "not-a-forcefield"},
        {"forcefield": None},
        {"water_model": "not-a-water-model"},
        {"implicit_solvent": "not-a-solvent"},
    ],
)
def test_bound_model_errors_remain_native_without_preparation(view, engine, parameters):
    before = snapshot(view)
    with pytest.raises(Exception) as native:
        msm.molecular_mechanics.get_degrees_of_freedom(view.molsys, **parameters)
    with pytest.raises(type(native.value)) as actual:
        view.addons.molsysmt.molecular_mechanics.get_degrees_of_freedom(**parameters)
    assert str(actual.value) == str(native.value)
    unchanged(view, before)


def test_empty_owner_rejects_bound_count_but_keeps_explicit_lookup():
    with msv.new_view() as view:
        tools = view.addons.molsysmt.molecular_mechanics
        with pytest.raises(ValueError, match="Load a molecular system"):
            tools.get_degrees_of_freedom()
        assert tools.get_engine_forcefield("AMBER14") == ["amber14-all.xml"]


def test_pending_edits_are_read_without_scene_synchronization(view, engine):
    tools = view.addons.molsysmt
    coordinates = msm.get(view.molsys, coordinates=True)
    tools.basic.set(coordinates=coordinates, update_view=False)
    assert tools.get_sync_status()["state"] == "pending"
    before = snapshot(view)
    assert tools.molecular_mechanics.get_degrees_of_freedom() == 154
    assert tools.molecular_mechanics.get_engine_forcefield("AMBER14") == [
        "amber14-all.xml"
    ]
    unchanged(view, before)


def test_multiple_structure_conversion_failure_is_native_and_not_silently_reduced(
    engine,
):
    with msv.demo["pentalanine"] as view:
        before = snapshot(view)
        with pytest.raises(Exception) as native:
            msm.molecular_mechanics.get_degrees_of_freedom(view.molsys)
        with pytest.raises(type(native.value)) as actual:
            view.addons.molsysmt.molecular_mechanics.get_degrees_of_freedom()
        assert str(actual.value) == str(native.value)
        unchanged(view, before)


def test_cached_methods_resolve_replacement_and_reject_closed_owner(view, engine):
    tools = view.addons.molsysmt.molecular_mechanics
    count = tools.get_degrees_of_freedom
    lookup = tools.get_engine_forcefield
    assert count() == 154
    replacement = msm.convert(
        msm.systems["Trp-Cage"]["1l2y.h5msm"], structure_indices=0
    )
    view.load(replacement, mode="replace")
    assert count() == 762
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        count(skip_digestion=True)
    with pytest.raises(RuntimeError, match="closed view"):
        lookup("AMBER14", skip_digestion=True)
