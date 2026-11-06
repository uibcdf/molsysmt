"""Check native minimization ownership and actual course-call continuation."""

import ast
import inspect
import json
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw

pytest.importorskip("openmm")

ROOT = Path(__file__).resolve().parents[3]
COURSE = ROOT / "docs/content/course"
LESSONS = [
    f"Path_{name}/43_Energy_Minimization.ipynb"
    for name in ["Alzheimer", "Enzyme", "Antiviral", "Biophysics"]
] + ["Path_Alzheimer/54_Final_Project.ipynb"]


@pytest.fixture
def existing_engine_input(alanine_molsys, request):
    import openmm
    from openmm import app, unit

    molsys = msm.extract(alanine_molsys, structure_indices=0)
    system = msm.convert(molsys, to_form="openmm.System")
    probe = openmm.CustomExternalForce("marker*x*x")
    probe.addGlobalParameter("marker", 0.1)
    probe.addParticle(0, [])
    system.addForce(probe)
    integrator = openmm.LangevinIntegrator(
        300 * unit.kelvin, 1 / unit.picosecond, 0.002 * unit.picosecond
    )
    integrator.setRandomNumberSeed(19)
    integrator.setConstraintTolerance(1e-6)
    platform = openmm.Platform.getPlatformByName("Reference")
    if request.param == "openmm.Simulation":
        topology = msm.convert(molsys, to_form="openmm.Topology")
        item = app.Simulation(topology, system, integrator, platform)
        item.reporters.append(object())
        context = item.context
    else:
        item = context = openmm.Context(system, integrator, platform)
    context.setPositions(
        puw.convert(
            molsys.get(coordinates=True)[0], to_form="openmm.unit", to_unit="nm"
        )
    )
    context.setVelocities(
        np.full((system.getNumParticles(), 3), 0.01) * unit.nanometer / unit.picosecond
    )
    context.setPeriodicBoxVectors(*np.eye(3) * 3.0 * unit.nanometer)
    context.setTime(4.0 * unit.picosecond)
    context.setStepCount(13)
    context.setParameter("marker", 0.3)
    return item, context, molsys


def _engine_snapshot(context):
    import openmm

    state = context.getState(
        getPositions=True,
        getVelocities=True,
        getParameters=True,
        getIntegratorParameters=True,
    )
    return {
        "state": openmm.XmlSerializer.serialize(state),
        "system": openmm.XmlSerializer.serialize(context.getSystem()),
        "integrator": openmm.XmlSerializer.serialize(context.getIntegrator()),
        # Same live context/platform only; this is not a portable-copy recipe.
        "checkpoint": context.createCheckpoint(),
        "platform": context.getPlatform().getName(),
    }


@pytest.mark.parametrize(
    "existing_engine_input", ["openmm.Context", "openmm.Simulation"], indirect=True
)
def test_existing_engine_default_failure_preserves_all_source_state(
    existing_engine_input, monkeypatch
):
    import openmm

    from molsysmt._private.smonitor import NotImplementedMethodError

    item, context, _ = existing_engine_input
    before = _engine_snapshot(context)
    reporters = list(item.reporters) if hasattr(item, "reporters") else None
    calls = []
    original = openmm.LocalEnergyMinimizer.minimize

    def observe(*args, **kwargs):
        calls.append(args[0])
        return original(*args, **kwargs)

    monkeypatch.setattr(openmm.LocalEnergyMinimizer, "minimize", staticmethod(observe))
    with pytest.raises(NotImplementedMethodError):
        msm.molecular_mechanics.potential_energy_minimization(item)
    assert _engine_snapshot(context) == before
    assert calls == [], "Unsupported independent copying must fail before optimization"
    if reporters is not None:
        assert item.reporters == reporters


@pytest.mark.parametrize(
    "existing_engine_input", ["openmm.Context", "openmm.Simulation"], indirect=True
)
@pytest.mark.parametrize(
    "to_form",
    ["molsysmt.Structures", "molsysmt.MolSys", "openmm.Context", "openmm.Simulation"],
)
def test_existing_engine_explicit_output_cannot_bypass_detachment(
    existing_engine_input, to_form, monkeypatch
):
    import openmm

    from molsysmt._private.smonitor import NotImplementedMethodError

    item, context, _ = existing_engine_input
    before = _engine_snapshot(context)

    def must_not_optimize(*args, **kwargs):
        pytest.fail("The output form must not bypass source ownership")

    monkeypatch.setattr(
        openmm.LocalEnergyMinimizer, "minimize", staticmethod(must_not_optimize)
    )
    with pytest.raises(NotImplementedMethodError, match="independent copy") as raised:
        msm.molecular_mechanics.potential_energy_minimization(item, to_form=to_form)
    assert raised.value.extra["arguments"]["form"] == msm.get_form(item)
    assert _engine_snapshot(context) == before


@pytest.mark.parametrize(
    "existing_engine_input", ["openmm.Context", "openmm.Simulation"], indirect=True
)
def test_existing_engine_rejects_before_creating_output_file(
    existing_engine_input, tmp_path
):
    from molsysmt._private.smonitor import NotImplementedMethodError

    item, context, _ = existing_engine_input
    before = _engine_snapshot(context)
    filename = tmp_path / "independent.h5msm"
    with pytest.raises(NotImplementedMethodError, match="independent copy"):
        msm.molecular_mechanics.potential_energy_minimization(
            item, to_form=str(filename)
        )
    assert not filename.exists()
    assert _engine_snapshot(context) == before


@pytest.mark.parametrize(
    "existing_engine_input", ["openmm.Context", "openmm.Simulation"], indirect=True
)
@pytest.mark.parametrize("engine_first", [True, False])
def test_composite_engine_input_keeps_the_same_source_ownership(
    existing_engine_input, engine_first, monkeypatch
):
    import openmm

    from molsysmt._private.smonitor import NotImplementedMethodError

    item, context, molsys = existing_engine_input
    items = [item, molsys.topology] if engine_first else [molsys.topology, item]
    source_ids = [id(member) for member in items]
    before = _engine_snapshot(context)

    def must_not_optimize(*args, **kwargs):
        pytest.fail("A composite input must not bypass source ownership")

    monkeypatch.setattr(
        openmm.LocalEnergyMinimizer, "minimize", staticmethod(must_not_optimize)
    )
    with pytest.raises(NotImplementedMethodError, match="independent copy"):
        msm.molecular_mechanics.potential_energy_minimization(
            items, to_form="molsysmt.Structures"
        )
    assert [id(member) for member in items] == source_ids
    assert _engine_snapshot(context) == before


@pytest.mark.parametrize(
    "existing_engine_input", ["openmm.Context", "openmm.Simulation"], indirect=True
)
def test_existing_engine_explicit_in_place_preserves_other_state(existing_engine_input):
    item, context, _ = existing_engine_input
    before = _engine_snapshot(context)
    initial = context.getState(getPositions=True, getVelocities=True, getEnergy=True)
    positions = puw.get_value(initial.getPositions(asNumpy=True), to_unit="nm").copy()
    velocities = puw.get_value(
        initial.getVelocities(asNumpy=True), to_unit="nm/ps"
    ).copy()
    reporters = list(item.reporters) if hasattr(item, "reporters") else None
    with puw.context(
        standard_units=["angstrom", "ps", "kcal/mol", "e", "K", "radians"]
    ):
        policy = {
            k: v for k, v in puw.configure.report().items() if k != "loaded_libraries"
        }
        result = msm.molecular_mechanics.potential_energy_minimization(
            item, in_place=True
        )
        final = context.getState(getPositions=True, getVelocities=True, getEnergy=True)
        assert result is None
        assert (
            np.max(
                np.abs(
                    puw.get_value(final.getPositions(asNumpy=True), to_unit="nm")
                    - positions
                )
            )
            > 1e-5
        )
        assert puw.get_value(
            final.getPotentialEnergy(), to_unit="kJ/mol"
        ) < puw.get_value(initial.getPotentialEnergy(), to_unit="kJ/mol")
        assert {
            k: v for k, v in puw.configure.report().items() if k != "loaded_libraries"
        } == policy
    after = _engine_snapshot(context)
    assert after["system"] == before["system"]
    assert after["integrator"] == before["integrator"]
    assert after["platform"] == before["platform"]
    np.testing.assert_array_equal(
        puw.get_value(final.getVelocities(asNumpy=True), to_unit="nm/ps"), velocities
    )
    assert final.getTime() == initial.getTime()
    assert context.getStepCount() == 13
    assert context.getParameter("marker") == 0.3
    np.testing.assert_array_equal(
        puw.get_value(final.getPeriodicBoxVectors(), to_unit="nm"), np.eye(3) * 3.0
    )
    if reporters is not None:
        assert item.reporters == reporters


@pytest.mark.parametrize("existing_engine_input", ["openmm.Context"], indirect=True)
@pytest.mark.parametrize("positions", [True, False])
def test_state_copy_remains_an_explicit_snapshot_capability(
    existing_engine_input, positions
):
    import openmm

    _, context, _ = existing_engine_input
    state = context.getState(getPositions=positions, getEnergy=True)
    before = openmm.XmlSerializer.serialize(state)
    with pytest.raises(
        msm.NotImplementedMethodError, match="independent copy of openmm.State"
    ):
        msm.copy(state)
    assert openmm.XmlSerializer.serialize(state) == before


@pytest.mark.parametrize("platform", ["CPU", "Reference"])
@pytest.mark.parametrize("in_place", [False, True])
def test_native_minimization_ownership_coordinates_energy_and_units(
    alanine_molsys, platform, in_place
):
    molsys = msm.extract(alanine_molsys, structure_indices=0)
    original = puw.get_value(molsys.get(coordinates=True), to_unit="nm").copy()
    with puw.context(
        standard_units=["angstrom", "ps", "kcal/mol", "e", "K", "radians"]
    ):
        policy = {
            k: v for k, v in puw.configure.report().items() if k != "loaded_libraries"
        }
        before = msm.molecular_mechanics.get_potential_energy(molsys, platform=platform)
        result = msm.molecular_mechanics.potential_energy_minimization(
            molsys, platform=platform, in_place=in_place
        )
        if in_place:
            assert result is None
            minimized = molsys
        else:
            assert isinstance(result, type(molsys))
            assert result is not molsys
            minimized = result
            np.testing.assert_array_equal(
                puw.get_value(molsys.structures.coordinates, to_unit="nm"), original
            )
        coordinates = puw.get_value(minimized.get(coordinates=True), to_unit="nm")
        assert coordinates.shape == original.shape
        assert np.isfinite(coordinates).all()
        assert np.max(np.abs(coordinates - original)) > 1e-5
        after = msm.molecular_mechanics.get_potential_energy(
            minimized, platform=platform
        )
        assert puw.get_unit(before) == puw.unit("kcal/mol")
        assert puw.get_unit(after) == puw.unit("kcal/mol")
        before_value = puw.get_value(before, to_unit="kJ/mol")
        after_value = puw.get_value(after, to_unit="kJ/mol")
        assert np.isfinite([before_value, after_value]).all()
        assert after_value < before_value - 1e-4
        assert {
            k: v for k, v in puw.configure.report().items() if k != "loaded_libraries"
        } == policy


@pytest.mark.parametrize("lesson", LESSONS)
def test_course_minimization_keeps_the_minimized_system_for_later_steps(
    alanine_molsys, lesson
):
    notebook = json.loads((COURSE / lesson).read_text())
    code = "\n\n".join(
        "".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code"
    )
    tree = ast.parse(code)
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "potential_energy_minimization"
    ]
    assert len(calls) == 1
    call = calls[0]
    # Check the actual public keyword contract; no invented compatibility alias.
    assert all(keyword.arg is not None for keyword in call.keywords)
    inspect.signature(msm.molecular_mechanics.potential_energy_minimization).bind(
        *[object() for _ in call.args],
        **{keyword.arg: object() for keyword in call.keywords},
    )
    assert isinstance(call.args[0], ast.Name)
    system_name = call.args[0].id
    parents = {
        child: parent
        for parent in ast.walk(tree)
        for child in ast.iter_child_nodes(parent)
    }
    statement = parents[call]
    assert isinstance(statement, (ast.Expr, ast.Assign))
    assert statement.value is call
    molsys = msm.extract(alanine_molsys, structure_indices=0)
    original = puw.get_value(molsys.get(coordinates=True), to_unit="nm").copy()
    before = msm.molecular_mechanics.get_potential_energy(molsys, platform="CPU")
    namespace = {"msm": msm, system_name: molsys}
    # Execute the actual lesson call on a bounded bundled model, not its
    # network/download/ligand/membrane preparation or graphical scene.
    executable = ast.fix_missing_locations(
        ast.Module(body=[statement], type_ignores=[])
    )
    exec(compile(executable, str(COURSE / lesson), "exec"), namespace)
    minimized = namespace[system_name]
    coordinates = puw.get_value(minimized.get(coordinates=True), to_unit="nm")
    assert np.max(np.abs(coordinates - original)) > 1e-5, (
        "The lesson continues with unminimized coordinates"
    )
    explicit_in_place = any(
        k.arg == "in_place" and ast.literal_eval(k.value) is True for k in call.keywords
    )
    if not explicit_in_place:
        assert minimized is not molsys
        np.testing.assert_array_equal(
            puw.get_value(molsys.get(coordinates=True), to_unit="nm"), original
        )
    after = msm.molecular_mechanics.get_potential_energy(minimized, platform="CPU")
    assert (
        puw.get_value(after, to_unit="kJ/mol")
        < puw.get_value(before, to_unit="kJ/mol") - 1e-4
    )
    # Later energy/view calls must receive the system that was actually relaxed.
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in {"get_potential_energy", "view"}
            and node.lineno > call.lineno
        ):
            assert isinstance(node.args[0], ast.Name)
            assert namespace[node.args[0].id] is minimized
