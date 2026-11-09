"""Checking complete-environment forces, explicit axes and source ownership."""

import copy

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentChoiceError, ArgumentError

openmm = pytest.importorskip("openmm")
from openmm import app, unit  # noqa: E402

FORCE_UNIT = "kJ/(mol*nm)"


@pytest.fixture
def harmonic():
    topology = app.Topology()
    group = topology.addResidue("LIG", topology.addChain("A"))
    atoms = [topology.addAtom(name, app.element.carbon, group) for name in ("C1", "C2")]
    topology.addBond(*atoms)
    system = openmm.System()
    for _ in atoms:
        system.addParticle(12.0)
    bond = openmm.HarmonicBondForce()
    bond.addBond(0, 1, 0.1, 100.0)
    system.addForce(bond)
    return topology, system


@pytest.fixture
def context(harmonic):
    _, system = harmonic
    context = openmm.Context(
        system,
        openmm.VerletIntegrator(0.001),
        openmm.Platform.getPlatformByName("Reference"),
    )
    context.setPositions(np.array([[0.0, 0.0, 0.0], [0.2, 0.0, 0.0]]) * unit.nanometer)
    context.setVelocities(np.full((2, 3), 0.3) * unit.nanometer / unit.picosecond)
    context.setTime(7.0)
    return context


@pytest.mark.parametrize(
    "selection,indices", [("all", [0, 1]), ([1], [1]), ([1, 0, 1], [1, 0, 1]), ([], [])]
)
@pytest.mark.parametrize("magnitude", [False, True])
def test_context_selection_keeps_the_complete_harmonic_environment(
    context, selection, indices, magnitude
):
    system_before = openmm.XmlSerializer.serialize(context.getSystem())
    integrator_before = openmm.XmlSerializer.serialize(context.getIntegrator())
    before = context.getState(getPositions=True, getVelocities=True)
    result = msm.molecular_mechanics.get_forces(
        context, selection=selection, magnitude=magnitude
    )
    expected = np.array([[10.0, 0.0, 0.0], [-10.0, 0.0, 0.0]])[indices]
    if magnitude:
        expected = np.linalg.norm(expected, axis=-1)
    np.testing.assert_allclose(
        puw.get_value(result, to_unit=FORCE_UNIT), expected, atol=1e-12
    )
    assert puw.get_unit(result) == puw.unit(FORCE_UNIT)
    assert openmm.XmlSerializer.serialize(context.getSystem()) == system_before
    assert openmm.XmlSerializer.serialize(context.getIntegrator()) == integrator_before
    after = context.getState(getPositions=True, getVelocities=True)
    assert after.getTime() == before.getTime()
    np.testing.assert_array_equal(
        after.getPositions(asNumpy=True), before.getPositions(asNumpy=True)
    )
    np.testing.assert_array_equal(
        after.getVelocities(asNumpy=True), before.getVelocities(asNumpy=True)
    )
    assert context.getPlatform().getName() == "Reference"


def test_simulation_selection_uses_its_existing_model(harmonic):
    topology, system = harmonic
    simulation = app.Simulation(
        topology,
        system,
        openmm.VerletIntegrator(0.001),
        openmm.Platform.getPlatformByName("Reference"),
    )
    simulation.context.setPositions([[0.0, 0.0, 0.0], [0.2, 0.0, 0.0]] * unit.nanometer)
    result = msm.molecular_mechanics.get_forces(
        simulation, selection='atom_name == "C2"'
    )
    np.testing.assert_allclose(
        puw.get_value(result, to_unit=FORCE_UNIT), [[-10.0, 0.0, 0.0]], atol=1e-12
    )


@pytest.mark.parametrize(
    "structures,shape",
    [([0], (1, 2, 3)), ([0, 0], (2, 2, 3)), ([], (0, 2, 3)), ("all", (1, 2, 3))],
)
def test_explicit_context_structure_axes_preserve_order_and_empty_shape(
    context, structures, shape
):
    result = msm.molecular_mechanics.get_forces(context, structure_indices=structures)
    assert result.shape == shape
    expected = np.broadcast_to([[10.0, 0.0, 0.0], [-10.0, 0.0, 0.0]], shape)
    np.testing.assert_allclose(
        puw.get_value(result, to_unit=FORCE_UNIT), expected, atol=1e-12
    )


@pytest.fixture
def native(alanine_molsys):
    native = msm.extract(alanine_molsys, structure_indices=0)
    xyz = puw.get_value(native.get(coordinates=True), to_unit="nm").copy()
    second = xyz.copy()
    second[0, 0, 0] += 0.002
    third = xyz.copy()
    third[0, 3, 1] -= 0.003
    for xyz in (second, third):
        incoming = msm.extract(native, structure_indices=0)
        msm.set(incoming, coordinates=puw.quantity(xyz, "nm"), structure_indices=0)
        msm.append_structures(native, incoming)
    return native


def _independent_context(native, *, periodic=False, structure_index=0):
    topology = msm.convert(
        native, to_form="openmm.Topology", structure_indices=[structure_index]
    )
    forcefield = app.ForceField("amber14-all.xml", "amber14/tip3p.xml")
    system = forcefield.createSystem(
        topology,
        nonbondedMethod=app.PME if periodic else app.NoCutoff,
        constraints=app.HBonds,
    )
    return openmm.Context(
        system,
        openmm.VerletIntegrator(0.001),
        openmm.Platform.getPlatformByName("Reference"),
    )


def test_native_default_returns_the_first_structure_without_preparation(
    native, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Force reading must not repair, protonate or minimize the source")

    monkeypatch.setattr(msm.build, "add_missing_hydrogens", forbidden)
    monkeypatch.setattr(openmm.LocalEnergyMinimizer, "minimize", forbidden)
    before = copy.deepcopy(native)
    result = msm.molecular_mechanics.get_forces(native, platform="Reference")
    oracle = _independent_context(native)
    xyz = puw.get_value(native.get(coordinates=True), to_unit="nm")
    oracle.setPositions(xyz[0] * unit.nanometer)
    expected = (
        oracle.getState(getForces=True)
        .getForces(asNumpy=True)
        .value_in_unit(unit.kilojoule_per_mole / unit.nanometer)
    )
    assert result.shape == (native.topology.n_atoms, 3)
    np.testing.assert_allclose(
        puw.get_value(result, to_unit=FORCE_UNIT), expected, rtol=1e-10, atol=1e-8
    )
    np.testing.assert_array_equal(
        puw.get_value(native.get(coordinates=True), to_unit="nm"), xyz
    )
    for name in ("atoms", "groups", "chains", "molecules", "entities"):
        pd.testing.assert_frame_equal(
            getattr(native.topology, name), getattr(before.topology, name)
        )
    assert native.chemical_states._inventory_equals(before.chemical_states)
    np.testing.assert_equal(
        native.chemical_states.get_preparation_history(),
        before.chemical_states.get_preparation_history(),
    )
    assert native.molecular_mechanics.to_dict() == before.molecular_mechanics.to_dict()


@pytest.mark.parametrize("magnitude", [False, True])
def test_native_nonconsecutive_structures_and_repeated_atom_selection(
    native, magnitude, monkeypatch
):
    indices = [7, 0, 7]
    structures = [2, 0, 2]
    monkeypatch.setattr(msm.configure, "chunk_size", 1)
    output = msm.molecular_mechanics.get_forces(
        native,
        selection=indices,
        structure_indices=structures,
        magnitude=magnitude,
        platform="Reference",
    )
    oracle = _independent_context(native)
    xyz = puw.get_value(native.get(coordinates=True), to_unit="nm")
    rows = []
    for structure_index in structures:
        oracle.setPositions(xyz[structure_index] * unit.nanometer)
        values = (
            oracle.getState(getForces=True)
            .getForces(asNumpy=True)
            .value_in_unit(unit.kilojoule_per_mole / unit.nanometer)[indices]
        )
        rows.append(np.linalg.norm(values, axis=-1) if magnitude else values)
    np.testing.assert_allclose(
        puw.get_value(output, to_unit=FORCE_UNIT), rows, atol=1e-8, rtol=1e-10
    )


def test_native_forces_match_an_independent_central_energy_gradient(native):
    forces = msm.molecular_mechanics.get_forces(
        native, selection=[0], platform="Reference"
    )
    oracle = _independent_context(native)
    xyz = puw.get_value(native.get(coordinates=True), to_unit="nm")[0].copy()
    delta = 1e-6
    energies = []
    for sign in (-1, 1):
        moved = xyz.copy()
        moved[0, 0] += sign * delta
        oracle.setPositions(moved * unit.nanometer)
        energies.append(
            oracle.getState(getEnergy=True)
            .getPotentialEnergy()
            .value_in_unit(unit.kilojoule_per_mole)
        )
    expected = -(energies[1] - energies[0]) / (2 * delta)
    np.testing.assert_allclose(
        puw.get_value(forces, to_unit=FORCE_UNIT)[0, 0], expected, atol=2e-4, rtol=1e-6
    )


def test_force_units_follow_the_application_policy(context):
    with puw.context(
        standard_units=[
            "pm",
            "ps",
            "kcal/mol",
            "kcal/(mol*angstrom)",
            "K",
            "e",
            "radians",
        ]
    ):
        policy = {
            k: v for k, v in puw.configure.report().items() if k != "loaded_libraries"
        }
        result = msm.molecular_mechanics.get_forces(context, selection=[1])
        assert puw.get_unit(result) == puw.unit("kcal/(mol*angstrom)")
        np.testing.assert_allclose(
            puw.get_value(result, to_unit=FORCE_UNIT), [[-10.0, 0.0, 0.0]], atol=1e-12
        )
        assert {
            k: v for k, v in puw.configure.report().items() if k != "loaded_libraries"
        } == policy


@pytest.mark.parametrize("element", ["group", "molecule", "system"])
def test_nonatomic_levels_are_rejected_explicitly(context, element):
    with pytest.raises(ArgumentChoiceError, match="element"):
        msm.molecular_mechanics.get_forces(context, element=element)


@pytest.mark.parametrize("indices", [[-1], [1], [True], [[0]], [0.5]])
def test_invalid_context_structure_indices_are_not_silently_reinterpreted(
    context, indices
):
    with pytest.raises(ArgumentError, match="structure_indices"):
        msm.molecular_mechanics.get_forces(context, structure_indices=indices)


@pytest.mark.parametrize("selection", [[-1], [2], [[0]], [0.5], [True]])
def test_invalid_context_atom_populations_are_rejected(context, selection):
    with pytest.raises(ArgumentError, match="selection"):
        msm.molecular_mechanics.get_forces(context, selection=selection)


@pytest.mark.parametrize("selection", [np.array([False, True]), [False, True]])
def test_boolean_masks_retain_atomic_meaning(context, selection):
    values = msm.molecular_mechanics.get_forces(context, selection=selection)
    np.testing.assert_allclose(
        puw.get_value(values, to_unit=FORCE_UNIT), [[-10.0, 0.0, 0.0]], atol=1e-12
    )


@pytest.mark.parametrize(
    "setting,value", [("cutoff_distance", "1.1 nm"), ("rigid_water", False)]
)
def test_unsupported_stored_model_overrides_are_not_discarded(native, setting, value):
    from molsysmt._private.smonitor import NotImplementedMethodError

    setattr(native.molecular_mechanics, setting, value)
    with pytest.raises(NotImplementedMethodError, match="overrides"):
        msm.molecular_mechanics.get_forces(native, platform="Reference")
    assert getattr(native.molecular_mechanics, setting) == value


def test_native_selection_uses_one_complete_context(native, monkeypatch):
    from molsysmt._private.molecular_forces import _ForceReducer

    original = msm.convert
    original_consume = _ForceReducer.consume
    calls = []
    chunks = []

    def observed(*args, **kwargs):
        result = original(*args, **kwargs)
        if kwargs.get("to_form") == "openmm.Context":
            calls.append((kwargs.copy(), result.getSystem().getNumParticles()))
        return result

    monkeypatch.setattr(msm.basic, "convert", observed)

    def consume(reducer, chunk):
        chunks.append(chunk["coordinates"].shape)
        assert not chunk["coordinates"].flags.writeable
        return original_consume(reducer, chunk)

    monkeypatch.setattr(_ForceReducer, "consume", consume)
    monkeypatch.setattr(msm.configure, "chunk_size", 1)
    result = msm.molecular_mechanics.get_forces(
        native, selection=[7], structure_indices=[2, 0], platform="Reference"
    )
    assert result.shape == (2, 1, 3)
    assert len(calls) == 1
    assert calls[0][0]["selection"] == "all"
    assert calls[0][0]["structure_indices"] == [2]
    assert calls[0][1] == native.topology.n_atoms
    assert chunks == [(1, native.topology.n_atoms, 3)] * 2


def test_native_input_and_force_output_follow_nondefault_units(native):
    xyz = puw.get_value(native.get(coordinates=True), to_unit="nm").copy()
    with puw.context(
        standard_units=[
            "pm",
            "ps",
            "kcal/mol",
            "kcal/(mol*angstrom)",
            "K",
            "e",
            "radians",
        ]
    ):
        msm.set(native, coordinates=puw.quantity(xyz * 1000, "pm"))
        policy = {
            k: v for k, v in puw.configure.report().items() if k != "loaded_libraries"
        }
        result = msm.molecular_mechanics.get_forces(
            native, selection=[0], structure_indices=[2, 0], platform="Reference"
        )
        oracle = _independent_context(native)
        rows = []
        for index in (2, 0):
            oracle.setPositions(xyz[index] * unit.nanometer)
            rows.append(
                oracle.getState(getForces=True)
                .getForces(asNumpy=True)
                .value_in_unit(unit.kilojoule_per_mole / unit.nanometer)[[0]]
            )
        assert puw.get_unit(result) == puw.unit("kcal/(mol*angstrom)")
        np.testing.assert_allclose(
            puw.get_value(result, to_unit=FORCE_UNIT), rows, atol=1e-8, rtol=1e-10
        )
        assert {
            k: v for k, v in puw.configure.report().items() if k != "loaded_libraries"
        } == policy
    np.testing.assert_allclose(
        puw.get_value(native.get(coordinates=True), to_unit="nm"), xyz, atol=1e-14
    )


def test_numerical_budget_is_checked_before_context_construction(native, monkeypatch):
    from molsysmt._private.smonitor import MemoryBudgetExceededError

    def forbidden(*args, **kwargs):
        pytest.fail("A rejected output must not construct an engine context")

    monkeypatch.setattr(msm.basic, "convert", forbidden)
    monkeypatch.setattr(msm.configure, "max_ram_usage", 100)
    with pytest.raises(MemoryBudgetExceededError):
        msm.molecular_mechanics.get_forces(native, platform="Reference")


def test_native_periodic_forces_use_each_selected_row_box(native):
    boxes = np.array(
        [
            np.diag([3.0, 3.0, 3.0]),
            [[3.2, 0.0, 0.0], [0.3, 3.0, 0.0], [0.2, 0.1, 3.4]],
            np.diag([4.0, 4.0, 4.0]),
        ]
    )
    msm.set(native, box=puw.quantity(boxes, "nm"))
    native.molecular_mechanics.non_bonded_method = "PME"
    coordinates = puw.get_value(native.get(coordinates=True), to_unit="nm").copy()
    frames = [2, 1, 0]
    result = msm.molecular_mechanics.get_forces(
        native, structure_indices=frames, platform="Reference"
    )
    # Match the declared numerical PME initialization as well as the physical
    # model; changing the box does not rebuild a live Context's FFT grid.
    oracle = _independent_context(native, periodic=True, structure_index=frames[0])
    rows = []
    for index in frames:
        oracle.setPeriodicBoxVectors(*(boxes[index] * unit.nanometer))
        oracle.setPositions(coordinates[index] * unit.nanometer)
        rows.append(
            oracle.getState(getForces=True)
            .getForces(asNumpy=True)
            .value_in_unit(unit.kilojoule_per_mole / unit.nanometer)
        )
    np.testing.assert_allclose(
        puw.get_value(result, to_unit=FORCE_UNIT), rows, atol=1e-7, rtol=1e-10
    )
    np.testing.assert_array_equal(
        puw.get_value(native.get(box=True), to_unit="nm"), boxes
    )


@pytest.mark.parametrize("magnitude", [False, True])
@pytest.mark.parametrize("empty_axis", ["atom", "structure"])
def test_native_empty_axes_are_typed_without_model_evaluation(
    native, monkeypatch, magnitude, empty_axis
):
    def forbidden(*args, **kwargs):
        pytest.fail("An empty force population does not evaluate a physical model")

    monkeypatch.setattr(msm.basic, "convert", forbidden)
    result = msm.molecular_mechanics.get_forces(
        native,
        selection=[] if empty_axis == "atom" else "all",
        structure_indices=[] if empty_axis == "structure" else "all",
        magnitude=magnitude,
    )
    shape = (0, native.topology.n_atoms) if empty_axis == "structure" else (3, 0)
    assert result.shape == (shape if magnitude else (*shape, 3))
    assert puw.get_unit(result) == puw.unit(FORCE_UNIT)


@pytest.mark.parametrize("format_version", ["0.5", "0.6"])
def test_modular_h5msm_streaming_avoids_full_molsys_or_analysis_loading(
    native, tmp_path, monkeypatch, format_version
):
    import hashlib
    import importlib

    expected = msm.molecular_mechanics.get_forces(
        native, selection=[7, 0], structure_indices=[2, 0], platform="Reference"
    )
    path = tmp_path / "forces.h5msm"
    msm.h5msm.write(native, path, format_version=format_version)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    module = importlib.import_module("molsysmt.form._h5msm05_modular")

    def forbidden(*args, **kwargs):
        pytest.fail(
            "Forces need chemistry and coordinate blocks, not a complete saved MolSys"
        )

    monkeypatch.setattr(module, "read_molsys_file", forbidden)
    monkeypatch.setattr(module, "read_named_analyses", forbidden)
    current = importlib.import_module("molsysmt._private.h5msm_storage.modular")
    monkeypatch.setattr(current, "read_molsys_file", forbidden)
    monkeypatch.setattr(current, "read_named_analyses", forbidden)
    monkeypatch.setattr(msm.configure, "chunk_size", 1)
    result = msm.molecular_mechanics.get_forces(
        str(path), selection=[7, 0], structure_indices=[2, 0], platform="Reference"
    )
    np.testing.assert_allclose(
        puw.get_value(result, to_unit=FORCE_UNIT),
        puw.get_value(expected, to_unit=FORCE_UNIT),
        atol=1e-8,
        rtol=1e-10,
    )
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest


@pytest.mark.parametrize("association", [pd.NA, 1])
def test_native_force_model_refuses_unknown_or_nonreference_chemistry(
    native, association, monkeypatch
):
    from molsysmt._private.smonitor import ArgumentConflictError

    if association is not pd.NA:
        native.chemical_states.append_state()
    msm.set(native, structure_indices=[1], structure_chemical_state_index=association)
    before = native.get(structure_chemical_state_index=True)

    def forbidden(*args, **kwargs):
        pytest.fail("Incompatible chemistry must fail before context construction")

    monkeypatch.setattr(msm.basic, "convert", forbidden)
    with pytest.raises(ArgumentConflictError, match="chemical_states"):
        msm.molecular_mechanics.get_forces(
            native, structure_indices=[2, 1], platform="Reference"
        )
    pd.testing.assert_extension_array_equal(
        pd.array(native.get(structure_chemical_state_index=True), dtype="Int64"),
        pd.array(before, dtype="Int64"),
    )


def test_parameterized_system_with_native_structures_preserves_the_exact_model(
    harmonic,
):
    _, system = harmonic
    from molsysmt.native import Structures

    structures = Structures()
    structures.coordinates = puw.quantity(
        [[[0, 0, 0], [0.2, 0, 0]], [[0, 0, 0], [0.3, 0, 0]]], "nm"
    )
    before = openmm.XmlSerializer.serialize(system)
    result = msm.molecular_mechanics.get_forces(
        [structures, system],
        structure_indices=[1, 0],
        selection=[1],
        platform="Reference",
    )
    np.testing.assert_allclose(
        puw.get_value(result, to_unit=FORCE_UNIT),
        [[[-20, 0, 0]], [[-10, 0, 0]]],
        atol=1e-12,
    )
    assert openmm.XmlSerializer.serialize(system) == before


def test_supplied_system_needs_no_native_chemical_parameterization(
    harmonic, monkeypatch
):
    from molsysmt.native import MolSys

    _, system = harmonic
    source = MolSys(n_atoms=2)
    source.structures.coordinates = puw.quantity([[[0, 0, 0], [0.2, 0, 0]]], "nm")
    msm.set(source, structure_chemical_state_index=pd.NA)

    def forbidden(*args, **kwargs):
        pytest.fail("A supplied complete System must not be reparameterized")

    monkeypatch.setattr(app, "ForceField", forbidden)
    forces = msm.molecular_mechanics.get_forces(
        [source, system], selection=[1], platform="Reference"
    )
    np.testing.assert_allclose(
        puw.get_value(forces, to_unit=FORCE_UNIT), [[-10.0, 0, 0]], atol=1e-12
    )
    assert pd.isna(source.get(structure_chemical_state_index=True)[0])


def test_force_reader_does_not_require_optional_attribution(context, monkeypatch):
    from molsysmt import _ackredit

    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    result = msm.molecular_mechanics.get_forces(context)
    np.testing.assert_allclose(
        puw.get_value(result, to_unit=FORCE_UNIT), [[10, 0, 0], [-10, 0, 0]], atol=1e-12
    )


def test_absent_force_engine_retains_a_dependency_diagnostic(native, monkeypatch):
    from depdigest.core import checker

    from molsysmt._private.smonitor import LibraryNotFoundError

    original = checker.find_spec

    def missing(name, *args, **kwargs):
        return None if name == "openmm" else original(name, *args, **kwargs)

    try:
        monkeypatch.setattr(checker, "find_spec", missing)
        checker.is_installed.cache_clear()
        with pytest.raises(LibraryNotFoundError, match="openmm"):
            msm.molecular_mechanics.get_forces(native)
    finally:
        monkeypatch.setattr(checker, "find_spec", original)
        checker.is_installed.cache_clear()


def test_an_unimplemented_force_engine_does_not_fall_back(context):
    with pytest.raises(ArgumentChoiceError, match="engine"):
        msm.molecular_mechanics.get_forces(context, engine="MolSysMT")


@pytest.mark.parametrize("periodic", [False, True])
@pytest.mark.parametrize("format_version", ["0.5", "0.6"])
def test_structures_only_h5msm_can_supply_a_parameterized_model(
    harmonic, tmp_path, monkeypatch, periodic, format_version
):
    import importlib

    from molsysmt.native import Structures

    _, system = harmonic
    if periodic:
        system.getForce(0).setUsesPeriodicBoundaryConditions(True)
        system.setDefaultPeriodicBoxVectors(*np.eye(3))
    structures = Structures()
    structures.coordinates = puw.quantity(
        [[[0, 0, 0], [0.2, 0, 0]], [[0, 0, 0], [0.8 if periodic else 0.3, 0, 0]]], "nm"
    )
    path = tmp_path / "force_coordinates.h5msm"
    msm.h5msm.write_layers(path, structures=structures, format_version=format_version)
    module = importlib.import_module("molsysmt.form._h5msm05_modular")

    def forbidden(*args, **kwargs):
        pytest.fail(
            "A complete model and coordinate file need no reconstructed chemistry"
        )

    monkeypatch.setattr(module, "read_molsys_file", forbidden)
    result = msm.molecular_mechanics.get_forces(
        [str(path), system],
        selection=[1],
        structure_indices=[1, 0],
        platform="Reference",
    )
    np.testing.assert_allclose(
        puw.get_value(result, to_unit=FORCE_UNIT),
        [[[10 if periodic else -20, 0, 0]], [[-10, 0, 0]]],
        atol=1e-12,
    )


def test_completed_force_execution_records_the_actual_engine_version(context):
    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("potential forces"):
        with ackredit.capture("force reader") as capture:
            msm.molecular_mechanics.get_forces(context, selection=[1])
        attribution = capture.attribution.to_dict()
        items = attribution["items"]
        actual = [item for item in items if item["id"].startswith("software:openmm:")]
        assert len(actual) == 1
        assert actual[0]["id"] == f"software:openmm:{openmm.__version__}"
        assert actual[0]["version"] == openmm.__version__
        uses = [use for use in attribution["uses"] if use["item_id"] == actual[0]["id"]]
        assert len(uses) == 1
        assert uses[0]["roles"] == ["executed_software"]
        assert uses[0]["context"]["environment"] == "complete_model"
    with ackredit.session("no force evaluation"):
        msm.molecular_mechanics.get_forces(context, selection=[])
        assert not ackredit.get_used_items()


def test_missing_coordinate_form_has_a_scientific_prerequisite_diagnostic(harmonic):
    from molsysmt._private.smonitor import NotWithThisFormError

    topology, _ = harmonic
    with pytest.raises(NotWithThisFormError, match="coordinates"):
        msm.molecular_mechanics.get_forces(topology)


def test_failed_force_evaluation_preserves_native_coordinates(native):
    from molsysmt._private.smonitor import StructuralInconsistencyError

    xyz = puw.get_value(native.get(coordinates=True), to_unit="nm").copy()
    invalid = xyz.copy()
    invalid[1, 0, 0] = np.nan
    native.structures.coordinates = puw.quantity(invalid, "nm")
    with pytest.raises(StructuralInconsistencyError, match="finite"):
        msm.molecular_mechanics.get_forces(
            native, structure_indices=[0, 1], platform="Reference"
        )
    np.testing.assert_array_equal(
        puw.get_value(native.get(coordinates=True), to_unit="nm"), invalid
    )
