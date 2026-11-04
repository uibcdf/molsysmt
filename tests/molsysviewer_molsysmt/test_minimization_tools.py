"""Receive real OpenMM minimization and retained-axis scene reconciliation."""

import inspect

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError
from molsysviewer.system_edits import SystemEditPendingError, SystemEditSyncError
from molsysviewer.widget import MolSysViewerWidget

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
    same,
    snapshot,
    unchanged,
)
from tests.molsysviewer_molsysmt.test_molecular_mechanics_tools import energy_units

puw = msm.pyunitwizard
NAME = "potential_energy_minimization"


def xyz(molsys):
    return puw.get_value(molsys.structures.coordinates, to_unit="nm")


@pytest.fixture
def engine(monkeypatch):
    engine = pytest.importorskip("openmm")
    monkeypatch.setenv("OPENMM_CPU_THREADS", "1")
    platform = engine.Platform.getPlatformByName("CPU")
    previous = platform.getPropertyDefaultValue("Threads")
    platform.setPropertyDefaultValue("Threads", "1")
    try:
        yield engine
    finally:
        platform.setPropertyDefaultValue("Threads", previous)


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0]) as view:
            result = msm.interactions.hbonds.get_buch_hbonds(
                view.molsys,
                structure_indices="all",
                pbc=False,
                output_type="molsysmt.Interactions",
            )
            view.interactions.attach(result, name="science", assume_aligned=True)
            view.interactions.add("science", tag="hb")
            yield view


def direct_openmm_minimum(molsys, engine):
    """Construct and minimize the qualified model without MolSysMT mechanics."""
    from openmm import app, unit

    topology = msm.convert(molsys, to_form="openmm.Topology")
    system = app.ForceField("amber14-all.xml", "amber14/tip3p.xml").createSystem(
        topology, nonbondedMethod=app.NoCutoff, constraints=app.HBonds
    )
    integrator = engine.VerletIntegrator(0.001)
    context = engine.Context(
        system, integrator, engine.Platform.getPlatformByName("CPU"), {"Threads": "1"}
    )
    try:
        context.setPositions(xyz(molsys)[0] * unit.nanometer)
        before = (
            context.getState(getEnergy=True)
            .getPotentialEnergy()
            .value_in_unit(unit.kilojoule_per_mole)
        )
        engine.LocalEnergyMinimizer.minimize(context)
        state = context.getState(getEnergy=True, getPositions=True, getForces=True)
        positions = state.getPositions(asNumpy=True).value_in_unit(unit.nanometer)
        after = state.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
        forces = state.getForces(asNumpy=True).value_in_unit(
            unit.kilojoule_per_mole / unit.nanometer
        )
        return before, after, positions, forces
    finally:
        del context
        del integrator


def same_noncoordinate_domains(actual, expected):
    for name in ("atoms", "groups", "molecules", "entities", "chains"):
        pd.testing.assert_frame_equal(
            getattr(actual.topology, name),
            getattr(expected.topology, name),
            check_frame_type=False,
        )
    assert actual.chemical_states._inventory_equals(expected.chemical_states)
    for name in (
        "forcefield",
        "water_model",
        "implicit_solvent",
        "partial_charge",
        "atom_ff_type",
    ):
        same(
            getattr(actual.molecular_mechanics, name),
            getattr(expected.molecular_mechanics, name),
        )
    same(actual.structures.time, expected.structures.time)
    same(actual.structures.box, expected.structures.box)


def unchanged_after_rejection(view, before, in_place):
    if in_place:
        # Managed attempts retain an audit identifier even after a clean native
        # rejection. Revisions, pending work and all scientific/scene data must
        # still match; do not confuse attempt metadata with a completed edit.
        status = view.addons.molsysmt.get_sync_status()
        operation_id = status["operation_id"]
        assert isinstance(operation_id, str)
        assert operation_id.startswith(f"molsysmt.molecular_mechanics.{NAME}:")
        assert operation_id != before[3]["operation_id"]
        before = list(before)
        before[3] = {**before[3], "operation_id": operation_id}
    unchanged(view, before)


def test_signature_local_controls_documentation_and_discovery(view):
    method = view.addons.molsysmt.molecular_mechanics.potential_energy_minimization
    native = inspect.signature(msm.molecular_mechanics.potential_energy_minimization)
    bound = inspect.signature(method)
    assert [
        p
        for n, p in bound.parameters.items()
        if n not in {"update_view", "skip_digestion"}
    ] == list(native.parameters.values())[1:]
    for name, default in (("update_view", True), ("skip_digestion", False)):
        parameter = bound.parameters[name]
        assert parameter.default is default
        assert parameter.kind is inspect.Parameter.KEYWORD_ONLY
    assert bound.parameters["in_place"].default is False
    assert method.digestion_plan is not None
    assert NAME in dir(view.addons.molsysmt.molecular_mechanics)
    assert not hasattr(view.addons.molsysmt, NAME)
    doc = inspect.getdoc(method)
    assert "View integration" in doc and "local minimum" in doc
    assert "native minimizer has no declared escape hatch" in doc
    for parameter in bound.parameters:
        assert f"{parameter} :" in doc
    for extra in ("molecular_system", "structure_indices", "selection", "tolerance"):
        with pytest.raises(UnknownArgumentError):
            method(**{extra: None})


@pytest.mark.parametrize("energy_unit", ["kJ/mol", "kcal/mol"])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("update_view", [False, True])
def test_minimum_matches_direct_openmm_and_preserves_noncoordinate_domains(
    view, engine, energy_unit, in_place, update_view
):
    energy_before, expected_energy, expected_xyz, forces = direct_openmm_minimum(
        view.molsys, engine
    )
    before = snapshot(view)
    target = view.molsys
    analysis = target.interactions["science"]
    with puw.context(standard_units=energy_units(energy_unit)):
        policy = dict(puw.configure.get_standard_units())
        result = view.addons.molsysmt.molecular_mechanics.potential_energy_minimization(
            in_place=in_place, update_view=update_view
        )
        output = target if in_place else result
        actual_energy = msm.molecular_mechanics.get_potential_energy(output)
        assert puw.is_quantity(actual_energy)
        assert dict(puw.configure.get_standard_units()) == policy
        np.testing.assert_allclose(
            puw.get_value(actual_energy, to_unit="kJ/mol"),
            expected_energy,
            rtol=1e-7,
            atol=1e-5,
        )
    assert np.isfinite(forces).all()
    assert expected_energy < energy_before - 100
    assert xyz(output).shape == (1, 62, 3)
    np.testing.assert_allclose(xyz(output)[0], expected_xyz, rtol=0, atol=5e-6)
    assert not np.allclose(xyz(output), xyz(before[1]))
    same_noncoordinate_domains(output, before[1])
    assert view.molsys is target
    assert output.interactions["science"].evaluated_structure_indices.size == 0
    if in_place:
        assert result is None
        assert view.addons.molsysmt.get_sync_status()["state"] == (
            "synchronized" if update_view else "pending"
        )
        if not update_view:
            storage = target.structures._coordinates
            view.addons.molsysmt.sync_view()
            assert target.structures._coordinates is storage
        assert view.addons.molsysmt.get_sync_status()["target_revision"] == 1
    else:
        assert output is not target
        np.testing.assert_array_equal(analysis.evaluated_structure_indices, [0])
        unchanged(view, before)


@pytest.mark.parametrize("in_place", [False, True])
def test_skip_is_local_and_never_bypasses_native_method_validation(
    view, engine, in_place
):
    before = snapshot(view)
    with pytest.raises(Exception) as native:
        msm.molecular_mechanics.potential_energy_minimization(
            view.molsys, method="unsupported-minimizer", in_place=in_place
        )
    with pytest.raises(type(native.value)) as actual:
        view.addons.molsysmt.molecular_mechanics.potential_energy_minimization(
            method="unsupported-minimizer", in_place=in_place, skip_digestion=True
        )
    assert str(actual.value) == str(native.value)
    unchanged_after_rejection(view, before, in_place)


@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("skip", [False, True])
def test_local_skip_keeps_real_native_minimization(view, engine, in_place, skip):
    result = view.addons.molsysmt.molecular_mechanics.potential_energy_minimization(
        in_place=in_place, skip_digestion=skip
    )
    output = view.molsys if in_place else result
    energy = msm.molecular_mechanics.get_potential_energy(output)
    assert float(puw.get_value(energy, to_unit="kJ/mol")) < 27


@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize(
    "parameters",
    [
        {"engine": "not-an-engine"},
        {"platform": "not-a-platform"},
        {"platform": "Reference"},
        {"to_form": "not-a-form"},
    ],
)
def test_native_rejection_preserves_science_and_scene(
    view, engine, in_place, parameters
):
    before = snapshot(view)
    with pytest.raises(Exception) as native:
        msm.molecular_mechanics.potential_energy_minimization(
            view.molsys, in_place=in_place, **parameters
        )
    with pytest.raises(type(native.value)) as actual:
        view.addons.molsysmt.molecular_mechanics.potential_energy_minimization(
            in_place=in_place, **parameters
        )
    assert str(actual.value) == str(native.value)
    unchanged_after_rejection(view, before, in_place)


@pytest.mark.parametrize("in_place", [False, True])
def test_multiple_structure_rejection_remains_native(engine, in_place):
    with msv.demo["pentalanine"] as view:
        before = snapshot(view)
        with pytest.raises(Exception) as native:
            msm.molecular_mechanics.potential_energy_minimization(
                view.molsys, in_place=in_place
            )
        with pytest.raises(type(native.value)) as actual:
            view.addons.molsysmt.molecular_mechanics.potential_energy_minimization(
                in_place=in_place
            )
        assert str(actual.value) == str(native.value)
        unchanged_after_rejection(view, before, in_place)


@pytest.mark.parametrize("parameters", [{"update_view": 1}, {"in_place": "yes"}])
def test_integration_flags_still_validate_with_local_skip(view, parameters):
    before = snapshot(view)
    with pytest.raises(Exception):
        view.addons.molsysmt.molecular_mechanics.potential_energy_minimization(
            skip_digestion=True, **parameters
        )
    unchanged(view, before)


def test_explicit_native_form_and_verbose_output(view, engine, capsys):
    before = snapshot(view)
    result = view.addons.molsysmt.molecular_mechanics.potential_energy_minimization(
        to_form="molsysmt.MolSys", verbose=True
    )
    assert msm.get_form(result) == "molsysmt.MolSys"
    text = capsys.readouterr().out
    assert "Potential Energy before minimization:" in text
    assert "Potential Energy after minimization:" in text
    unchanged(view, before)


def test_deferred_minimization_preserves_scene_identity_and_composes(view, engine):
    region = view.regions.add(selection=[2, 4], tag="kept")
    saved = view.selections.add("saved", atom_indices=[2, 4])
    sphere = view.shapes.add_sphere(atom_indices=[4], tag="anchor")
    view.active_selection.set([2, 4])
    source_id = view.load_blocks[0]["source_id"]
    tools = view.addons.molsysmt
    assert (
        tools.molecular_mechanics.potential_energy_minimization(
            in_place=True, update_view=False
        )
        is None
    )
    minimized = xyz(view.molsys).copy()
    with pytest.raises(SystemEditPendingError):
        region.hide(skip_digestion=True)
    before = snapshot(view)
    independent = tools.molecular_mechanics.potential_energy_minimization()
    assert independent is not view.molsys
    unchanged(view, before)
    tools.structure.translate(
        translation="[0,0,1] nm", in_place=True, update_view=False
    )
    expected = minimized + [0, 0, 1]
    storage = view.molsys.structures._coordinates
    tools.sync_view()
    np.testing.assert_allclose(xyz(view.molsys), expected, rtol=0, atol=1e-12)
    assert view.molsys.structures._coordinates is storage
    assert view.regions["kept"] is region and region.atom_indices == (2, 4)
    assert view.selections["saved"] is saved
    assert view.shapes["anchor"] is sphere
    assert view.active_selection.atom_indices == [2, 4]
    assert view.load_blocks[0]["source_id"] == source_id
    assert tools.get_sync_status()["target_revision"] == 2
    assert not view.history.can_undo()


class InterruptedMinimizationWidget(MolSysViewerWidget):
    interrupted = False

    def send(self, content, buffers=None):
        if self.interrupted and content.get("op") == "add_sphere":
            self.interrupted = False
            raise OSError("minimization receiving transport interruption")
        return super().send(content, buffers=buffers)


def test_sync_retry_keeps_completed_native_minimum_and_coordinate_storage(engine):
    with msv.demo["pentalanine"] as source:
        with msv.MolSysView(transport=InterruptedMinimizationWidget()) as view:
            view.load(source.molsys, structure_indices=[0])
            view.shapes.add_sphere(atom_indices=[0], tag="anchor")
            view._ready = True
            view.widget.interrupted = True
            with pytest.raises(SystemEditSyncError) as error:
                view.addons.molsysmt.molecular_mechanics.potential_energy_minimization(
                    in_place=True
                )
            assert error.value.science_completed is True
            assert error.value.scientific_result is None
            assert isinstance(error.value.__cause__, OSError)
            assert view.addons.molsysmt.get_sync_status()["state"] == "sync_failed"
            completed = xyz(view.molsys).copy()
            storage = view.molsys.structures._coordinates
            view.addons.molsysmt.sync_view()
            np.testing.assert_array_equal(xyz(view.molsys), completed)
            assert view.molsys.structures._coordinates is storage
            assert view.addons.molsysmt.get_sync_status()["target_revision"] == 1


def test_cached_minimizer_rebinds_and_rejects_closed_empty_owners(view, engine):
    method = view.addons.molsysmt.molecular_mechanics.potential_energy_minimization
    replacement = msm.convert(
        msm.systems["Trp-Cage"]["1l2y.h5msm"], structure_indices=0
    )
    view.load(replacement, mode="replace")
    before = snapshot(view)
    result = method()
    assert result.get_n_atoms() == 304
    assert not np.allclose(xyz(result), xyz(view.molsys))
    unchanged(view, before)
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method(in_place=True)
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty.addons.molsysmt.molecular_mechanics.potential_energy_minimization()
