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
from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
    same,
    snapshot,
    unchanged,
)

NAMES = (
    "get_engine_forcefield",
    "get_degrees_of_freedom",
    "get_potential_energy",
    "get_forces",
)


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


def direct_openmm_energies(molsys, engine, platform="CPU"):
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
        system,
        integrator,
        engine.Platform.getPlatformByName(platform),
        {"Threads": "1"} if platform == "CPU" else {},
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
        assert set(dir(namespace)) == set(NAMES) | {
            "potential_energy_minimization",
            "get_non_bonded_potential_energy",
        }
        text = inspect.getdoc(method)
        assert "View integration" in text
        assert "\nmolecular_system :" not in text
        for parameter in parameters:
            assert f"{parameter.name} :" in text
        inputs = (
            {}
            if name in {"get_potential_energy", "get_forces"}
            else {"forcefield": "AMBER14"}
        )
        for extra in (
            {"molecular_system": None},
            {"update_view": True},
            {"to_form": "molsysmt.MolSys"}
            if name == "get_forces"
            else {"structure_indices": [0]},
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
            ["amber99sb.xml", "implicit/obc1.xml"],
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
        # Resource contents and ownership belong to the native registry.
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
        {"platform": ""},
        {"platform": None},
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


@pytest.mark.parametrize("loaded", [False, True])
@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("model", ["OBC1", "OBC2"])
def test_received_resource_results_are_independent(loaded, skip, model):
    with msv.demo["pentalanine"] if loaded else msv.new_view() as owner:
        before = snapshot(owner)
        call = owner.addons.molsysmt.molecular_mechanics.get_engine_forcefield
        expected = ["amber14-all.xml", f"implicit/{model.lower()}.xml"]
        first = call("AMBER14", implicit_solvent=model, skip_digestion=skip)
        second = call("AMBER14", implicit_solvent=model, skip_digestion=skip)
        assert first == second == expected
        assert first is not second
        first[:] = ["caller-local.xml"]
        assert call("AMBER14", implicit_solvent=model, skip_digestion=skip) == expected
        assert (
            msm.molecular_mechanics.get_engine_forcefield(
                "AMBER14", implicit_solvent=model
            )
            == expected
        )
        unchanged(owner, before)


@pytest.mark.parametrize("model", ["OBC1", "OBC2"])
@pytest.mark.parametrize(
    "constraints", [None, "none", "hbonds", "all bonds", "h angles"]
)
def test_received_implicit_energy_and_degrees_match_explicit_physical_recipe(
    energy_engine, model, constraints
):
    from pathlib import Path

    from openmm import app, unit

    data = Path(__file__).parents[1] / "form/openmm_Topology/data/obc1_alanine.pdb"
    pdb = app.PDBFile(str(data))
    source = msm.convert(pdb)
    settings = dict(
        forcefield="AMBER14", implicit_solvent=model, non_bonded_method="no cutoff"
    )
    # An absent stored setting uses the native HBonds default. The explicit
    # string "none" requests no constraints; converter-level None is tested
    # separately by the native owner and is not a setter contract here.
    if constraints is not None:
        settings["constraints"] = constraints
    msm.set(source, **settings)
    policy = {
        None: app.HBonds,
        "none": None,
        "hbonds": app.HBonds,
        "all bonds": app.AllBonds,
        "h angles": app.HAngles,
    }[constraints]
    system = app.ForceField(
        "amber14-all.xml", f"implicit/{model.lower()}.xml"
    ).createSystem(pdb.topology, nonbondedMethod=app.NoCutoff, constraints=policy)
    integrator = energy_engine.VerletIntegrator(0.001 * unit.picoseconds)
    context = energy_engine.Context(
        system,
        integrator,
        energy_engine.Platform.getPlatformByName("CPU"),
        {"Threads": "1"},
    )
    try:
        context.setPositions(pdb.positions)
        expected = (
            context.getState(getEnergy=True)
            .getPotentialEnergy()
            .value_in_unit(unit.kilojoules_per_mole)
        )
    finally:
        del context, integrator
    with msv.new_view(source) as owner:
        before = snapshot(owner)
        tools = owner.addons.molsysmt.molecular_mechanics
        observed = tools.get_potential_energy()
        # Explicit small-fixture CPU tolerance; finite-precision context
        # differences are not an implicit-model or arbitrary-system accuracy claim.
        assert msm.pyunitwizard.get_value(observed, to_unit="kJ/mol") == pytest.approx(
            expected, rel=1e-6, abs=1e-4
        )
        assert tools.get_degrees_of_freedom() == (
            3 * system.getNumParticles() - system.getNumConstraints()
        )
        unchanged(owner, before)


@pytest.mark.parametrize("platform", ["CPU", "Reference"])
def test_explicit_execution_platform_matches_its_independent_model(
    view, energy_engine, platform
):
    before = snapshot(view)
    expected, _ = direct_openmm_energies(view.molsys, energy_engine, platform=platform)
    observed = view.addons.molsysmt.molecular_mechanics.get_potential_energy(
        platform=platform
    )
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(observed, to_unit="kJ/mol"),
        expected,
        rtol=1e-7,
        atol=1e-5,
    )
    unchanged(view, before)


# Native #572 supplies the scientific implementation. These receive the bound
# current-primary/scene contract and compare against a separately built model.
FORCE_UNIT = "kJ/(mol*nm)"


@pytest.fixture
def force_view():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as owner:
            owner.regions.add(selection=[0, 5], tag="force-source")
            owner.measurements.add_distance(0, 5, tag="preserve-distance")
            owner.interactions.attach(
                msm.Interactions.from_records(
                    [],
                    n_atoms=owner.molsys.get_n_atoms(),
                    n_structures=3,
                    evaluated_structure_indices=[0, 1, 2],
                    method="receiving.force-read",
                ),
                name="preserve-coverage",
                assume_aligned=True,
            )
            owner.player.go_to_structure(1)
            yield owner


def independent_force_context(
    source, engine, *, platform="Reference", periodic=False, structure_index=0
):
    from openmm import app

    topology = msm.convert(
        source, to_form="openmm.Topology", structure_indices=[structure_index]
    )
    system = app.ForceField("amber14-all.xml", "amber14/tip3p.xml").createSystem(
        topology,
        nonbondedMethod=app.PME if periodic else app.NoCutoff,
        constraints=app.HBonds,
    )
    return engine.Context(
        system,
        engine.VerletIntegrator(0.001),
        engine.Platform.getPlatformByName(platform),
        {"Threads": "1"} if platform == "CPU" else {},
    )


def independent_force_rows(
    source, engine, structures, *, platform="Reference", periodic=False
):
    from openmm import unit

    context = independent_force_context(
        source,
        engine,
        platform=platform,
        periodic=periodic,
        structure_index=structures[0] if structures else 0,
    )
    xyz = msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm")
    boxes = (
        msm.pyunitwizard.get_value(source.structures.box, to_unit="nm")
        if periodic
        else None
    )
    try:
        rows = []
        for index in structures:
            if boxes is not None:
                context.setPeriodicBoxVectors(*(boxes[index] * unit.nanometer))
            context.setPositions(xyz[index] * unit.nanometer)
            rows.append(
                context.getState(getForces=True)
                .getForces(asNumpy=True)
                .value_in_unit(unit.kilojoule_per_mole / unit.nanometer)
            )
        return np.asarray(rows).reshape(len(structures), source.get_n_atoms(), 3)
    finally:
        del context


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("platform", ["CPU", "Reference"])
def test_force_vectors_read_full_environment_without_adopting_or_seeking(
    force_view, energy_engine, skip, platform
):
    before = snapshot(force_view)
    expected = independent_force_rows(
        force_view.molsys, energy_engine, [0], platform=platform
    )[0]
    result = force_view.addons.molsysmt.molecular_mechanics.get_forces(
        selection=[5, 0, 5], platform=platform, skip_digestion=skip
    )
    assert result.shape == (3, 3)
    assert msm.pyunitwizard.get_unit(result) == msm.pyunitwizard.unit(FORCE_UNIT)
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result, to_unit=FORCE_UNIT),
        expected[[5, 0, 5]],
        rtol=1e-7,
        atol=1e-5,
    )
    assert force_view.player.index == 1
    unchanged(force_view, before)


@pytest.mark.parametrize("structures", [None, [2, 0, 2], [], "all"])
@pytest.mark.parametrize("magnitude", [False, True])
@pytest.mark.parametrize(
    "population", ["all", "repeated", "mask", "empty", "native", "mdtraj"]
)
def test_force_axes_units_and_selection_order_are_native(
    force_view, energy_engine, structures, magnitude, population
):
    size = force_view.molsys.get_n_atoms()
    syntax = "MolSysMT"
    if population == "all":
        selection, atoms = "all", np.arange(size)
    elif population == "repeated":
        selection, atoms = [5, 0, 5], np.array([5, 0, 5])
    elif population == "mask":
        selection = np.isin(np.arange(size), [0, 5])
        atoms = np.array([0, 5])
    elif population == "empty":
        selection, atoms = [], np.array([], dtype=int)
    else:
        atoms = np.flatnonzero(
            force_view.molsys.topology.atoms["atom_name"].to_numpy() == "CA"
        )
        selection = "atom_name=='CA'" if population == "native" else "name CA"
        syntax = "MolSysMT" if population == "native" else "MDTraj"
    indices = (
        [0]
        if structures is None
        else list(range(3))
        if structures == "all"
        else structures
    )
    before = snapshot(force_view)
    result = force_view.addons.molsysmt.molecular_mechanics.get_forces(
        selection=selection,
        structure_indices=structures,
        magnitude=magnitude,
        syntax=syntax,
        platform="Reference",
    )
    expected = independent_force_rows(force_view.molsys, energy_engine, indices)[
        :, atoms
    ]
    if magnitude:
        expected = np.linalg.norm(expected, axis=-1)
    if structures is None:
        expected = expected[0]
    assert result.shape == expected.shape
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result, to_unit=FORCE_UNIT),
        expected,
        rtol=1e-10,
        atol=1e-8,
    )
    unchanged(force_view, before)


def test_force_gradient_has_the_correct_sign_and_complete_model(
    force_view, energy_engine
):
    from openmm import unit

    context = independent_force_context(force_view.molsys, energy_engine)
    xyz = msm.pyunitwizard.get_value(
        force_view.molsys.structures.coordinates, to_unit="nm"
    )[0].copy()
    step = 1e-6
    try:
        energies = []
        for sign in (-1, 1):
            displaced = xyz.copy()
            displaced[5, 0] += sign * step
            context.setPositions(displaced * unit.nanometer)
            energies.append(
                context.getState(getEnergy=True)
                .getPotentialEnergy()
                .value_in_unit(unit.kilojoule_per_mole)
            )
        expected = -(energies[1] - energies[0]) / (2 * step)
    finally:
        del context
    before = snapshot(force_view)
    result = force_view.addons.molsysmt.molecular_mechanics.get_forces(
        selection=[5], platform="Reference"
    )
    assert msm.pyunitwizard.get_value(result, to_unit=FORCE_UNIT)[
        0, 0
    ] == pytest.approx(expected, rel=1e-6, abs=2e-4)
    unchanged(force_view, before)


def test_force_result_follows_nondefault_energy_and_length_policy(
    force_view, energy_engine
):
    puw = msm.pyunitwizard
    expected = independent_force_rows(force_view.molsys, energy_engine, [2, 0])
    before = snapshot(force_view)
    with puw.context(standard_units=energy_units("kcal/mol") + ["kcal/(mol*angstrom)"]):
        result = force_view.addons.molsysmt.molecular_mechanics.get_forces(
            structure_indices=[2, 0], platform="Reference"
        )
        assert puw.get_unit(result) == puw.unit("kcal/(mol*angstrom)")
        np.testing.assert_allclose(
            puw.get_value(result, to_unit=FORCE_UNIT), expected, atol=1e-8, rtol=1e-10
        )
    unchanged(force_view, before)


def test_force_reader_uses_pending_coordinates_without_scene_synchronization(
    force_view, energy_engine
):
    puw = msm.pyunitwizard
    tools = force_view.addons.molsysmt
    original = tools.molecular_mechanics.get_forces(selection=[0], platform="Reference")
    xyz = puw.get_value(force_view.molsys.structures.coordinates, to_unit="nm").copy()
    xyz[0, 0, 0] += 0.003
    tools.basic.set(coordinates=puw.quantity(xyz, "nm"), update_view=False)
    assert tools.get_sync_status()["state"] == "pending"
    before = snapshot(force_view)
    result = tools.molecular_mechanics.get_forces(selection=[0], platform="Reference")
    expected = independent_force_rows(force_view.molsys, energy_engine, [0])[0, [0]]
    np.testing.assert_allclose(
        puw.get_value(result, to_unit=FORCE_UNIT), expected, atol=1e-8, rtol=1e-10
    )
    assert not np.allclose(
        puw.get_value(result, to_unit=FORCE_UNIT),
        puw.get_value(original, to_unit=FORCE_UNIT),
    )
    unchanged(force_view, before)


@pytest.mark.parametrize(
    "parameters",
    [
        {"element": "group"},
        {"engine": "unknown"},
        {"platform": "unknown"},
        {"selection": [100000]},
        {"structure_indices": [3]},
        {"structure_indices": [-1]},
    ],
)
def test_force_native_validation_errors_leave_source_scene_and_history_intact(
    force_view, energy_engine, parameters
):
    before = snapshot(force_view)
    with pytest.raises(Exception) as native:
        msm.molecular_mechanics.get_forces(force_view.molsys, **parameters)
    with pytest.raises(type(native.value)) as actual:
        force_view.addons.molsysmt.molecular_mechanics.get_forces(**parameters)
    assert str(actual.value) == str(native.value)
    unchanged(force_view, before)


def test_force_result_is_detached_and_cached_reader_resolves_replacement(
    force_view, energy_engine
):
    puw = msm.pyunitwizard
    method = force_view.addons.molsysmt.molecular_mechanics.get_forces
    first = method(selection=[0], platform="Reference")
    expected_first = puw.get_value(first, to_unit=FORCE_UNIT).copy()
    puw.get_value(first)[:] = 0
    assert np.any(expected_first)
    np.testing.assert_allclose(
        puw.get_value(method(selection=[0], platform="Reference"), to_unit=FORCE_UNIT),
        expected_first,
        rtol=1e-10,
        atol=1e-8,
    )
    with msv.demo["dialanine"] as replacement:
        force_view.load(replacement.molsys, mode="replace")
    before = snapshot(force_view)
    result = method(platform="Reference")
    assert result.shape == (force_view.molsys.get_n_atoms(), 3)
    np.testing.assert_allclose(
        puw.get_value(result, to_unit=FORCE_UNIT),
        independent_force_rows(force_view.molsys, energy_engine, [0])[0],
        rtol=1e-10,
        atol=1e-8,
    )
    unchanged(force_view, before)
    expected_after_close = puw.get_value(result, to_unit=FORCE_UNIT).copy()
    force_view.close()
    assert result.shape[1] == 3
    np.testing.assert_array_equal(
        puw.get_value(result, to_unit=FORCE_UNIT), expected_after_close
    )
    for skip in (False, True):
        with pytest.raises(RuntimeError, match="closed view"):
            method(skip_digestion=skip)
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty.addons.molsysmt.molecular_mechanics.get_forces()


@pytest.mark.parametrize("magnitude", [False, True])
def test_force_periodic_model_uses_each_ordered_structure_box(
    force_view, energy_engine, magnitude
):
    puw = msm.pyunitwizard
    boxes = np.array(
        [
            np.diag([3.0, 3.0, 3.0]),
            [[3.2, 0.0, 0.0], [0.3, 3.0, 0.0], [0.2, 0.1, 3.4]],
            np.diag([4.0, 4.0, 4.0]),
        ]
    )
    msm.set(force_view.molsys, non_bonded_method="PME")
    force_view.addons.molsysmt.basic.set(box=puw.quantity(boxes, "nm"))
    before = snapshot(force_view)
    structures = [2, 1, 0, 2]
    result = force_view.addons.molsysmt.molecular_mechanics.get_forces(
        selection=[5, 0, 5],
        structure_indices=structures,
        magnitude=magnitude,
        platform="Reference",
    )
    # An existing PME context retains its initial FFT grid. Build the oracle
    # against the first requested box, then update row-vector boxes in order.
    expected = independent_force_rows(
        force_view.molsys, energy_engine, structures, periodic=True
    )[:, [5, 0, 5]]
    if magnitude:
        expected = np.linalg.norm(expected, axis=-1)
    assert result.shape == expected.shape
    np.testing.assert_allclose(
        puw.get_value(result, to_unit=FORCE_UNIT), expected, rtol=1e-10, atol=1e-7
    )
    unchanged(force_view, before)


def test_force_numerical_budget_refusal_does_not_mutate_or_synchronize(
    force_view, energy_engine, monkeypatch
):
    from molsysmt._private.smonitor import MemoryBudgetExceededError

    monkeypatch.setattr(msm.configure, "max_ram_usage", 100)
    before = snapshot(force_view)
    with pytest.raises(MemoryBudgetExceededError):
        force_view.addons.molsysmt.molecular_mechanics.get_forces(
            structure_indices="all", platform="Reference"
        )
    unchanged(force_view, before)


def test_force_unavailable_model_override_is_not_silently_dropped(
    force_view, energy_engine
):
    from molsysmt._private.smonitor import NotImplementedMethodError

    force_view.molsys.molecular_mechanics.cutoff_distance = "1.1 nm"
    before = snapshot(force_view)
    with pytest.raises(NotImplementedMethodError, match="overrides") as native:
        msm.molecular_mechanics.get_forces(force_view.molsys, platform="Reference")
    with pytest.raises(NotImplementedMethodError, match="overrides") as actual:
        force_view.addons.molsysmt.molecular_mechanics.get_forces(platform="Reference")
    assert str(actual.value) == str(native.value)
    unchanged(force_view, before)


def test_force_read_preserves_all_native_domains_and_structural_observations(
    force_view, energy_engine
):
    source = force_view.molsys
    scientific = source.copy()
    before = snapshot(force_view)
    force_view.addons.molsysmt.molecular_mechanics.get_forces(
        structure_indices=[2, 0, 2], platform="Reference"
    )
    for name in ("atoms", "groups", "molecules", "chains", "entities"):
        same(getattr(source.topology, name), getattr(scientific.topology, name))
    assert source.chemical_states._inventory_equals(scientific.chemical_states)
    same(
        source.chemical_states.get_preparation_history(),
        scientific.chemical_states.get_preparation_history(),
    )
    same(source.molecular_mechanics.to_dict(), scientific.molecular_mechanics.to_dict())
    for attribute in (
        "coordinates",
        "box",
        "time",
        "b_factor",
        "occupancy",
        "structure_id",
    ):
        same(
            msm.get(source, **{attribute: True}),
            msm.get(scientific, **{attribute: True}),
        )
    unchanged(force_view, before)
