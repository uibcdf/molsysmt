"""Receive explicit force-field metadata and qualified mechanical degree counts."""

import inspect
import os
import subprocess
import sys

import molsysviewer as msv
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from tests.molsysviewer_molsysmt.test_build_assignment_tools import snapshot, unchanged

NAMES = ("get_engine_forcefield", "get_degrees_of_freedom")


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0]) as owner:
            yield owner


@pytest.fixture
def engine():
    return pytest.importorskip("openmm")


@pytest.mark.parametrize("name", NAMES)
def test_explicit_namespace_signatures_help_and_validation(name):
    with msv.new_view() as view:
        namespace = view.addons.molsysmt.molecular_mechanics
        method = getattr(namespace, name)
        native = inspect.signature(getattr(msm.molecular_mechanics, name))
        parameters = list(native.parameters.values())
        if name == "get_degrees_of_freedom":
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
        inputs = {"forcefield": "AMBER14"}
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
