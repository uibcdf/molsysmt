"""Receive independent native solvent construction without scene adoption."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_build_assignment_tools import snapshot, unchanged
from tests.molsysviewer_molsysmt.test_molecular_mechanics_tools import energy_units

puw = msm.pyunitwizard
PARAMETERS = dict(engine="OpenMM", box_shape="cubic", clearance="0.35 nm")


def source():
    # Preparation is explicit fixture construction, never part of the facade.
    molsys = msm.build.add_missing_terminal_cappings(
        msm.build.build_peptide("AlaValPro")
    )
    molsys.interactions = {
        "saved": msm.Interactions.from_records(
            [],
            n_atoms=molsys.get_n_atoms(),
            n_structures=1,
            evaluated_structure_indices=[0],
            method="test.solvation",
        )
    }
    return molsys


@pytest.fixture
def view():
    with msv.new_view(source()) as owner:
        owner.regions.add(selection=[0, 2], tag="keep")
        owner.shapes.add_sphere(atom_indices=[1], tag="anchor")
        yield owner


@pytest.fixture
def engine(monkeypatch):
    monkeypatch.setenv("OPENMM_CPU_THREADS", "1")
    return pytest.importorskip("openmm")


def direct_modeller(molsys):
    """Build an independent, neutral TIP3P cube using public OpenMM tools."""
    from openmm import app, unit

    topology = msm.convert(molsys, to_form="openmm.Topology")
    xyz = puw.get_value(molsys.structures.coordinates, to_unit="nm")[0]
    modeller = app.Modeller(topology, xyz * unit.nanometer)
    field = app.ForceField("amber14-all.xml", "amber14/tip3p.xml")
    modeller.addSolvent(
        field,
        model="tip3p",
        padding=0.35 * unit.nanometer,
        ionicStrength=0 * unit.molar,
        positiveIon="Na+",
        negativeIon="Cl-",
    )
    return modeller


def assert_water_geometry(result):
    water_atoms = msm.select(result, selection="group_type=='water'")
    n_waters = int(msm.get(result, n_waters=True))
    assert n_waters > 0 and len(water_atoms) == 3 * n_waters
    types = np.asarray(
        msm.get(result, selection=water_atoms, element="atom", atom_type=True)
    )
    np.testing.assert_array_equal(
        types.reshape(-1, 3), np.tile(["O", "H", "H"], (n_waters, 1))
    )
    water = puw.get_value(result.structures.coordinates, to_unit="nm")[
        0, water_atoms
    ].reshape(-1, 3, 3)
    # Each PDB coordinate is rounded to 0.001 angstrom. Subtracting two
    # independently rounded 3D positions bounds vector error by sqrt(3)*step.
    # The corresponding two-vector angular bound follows from arcsin(e/r).
    vector_rounding_bound = np.sqrt(3) * 1e-4  # nm
    vectors = water[:, 1:] - water[:, :1]
    lengths = np.linalg.norm(vectors, axis=-1)
    np.testing.assert_allclose(lengths, 0.09572, rtol=0, atol=vector_rounding_bound)
    angles = np.degrees(
        np.arccos(
            np.clip(
                np.sum(vectors[:, 0] * vectors[:, 1], axis=1)
                / np.prod(lengths, axis=1),
                -1,
                1,
            )
        )
    )
    angle_bound = np.degrees(2 * np.arcsin(vector_rounding_bound / 0.09572))
    np.testing.assert_allclose(angles, 104.52, rtol=0, atol=angle_bound)


def test_native_signature_help_discovery_and_local_control(view):
    call = view.addons.molsysmt.build.solvate
    native = inspect.signature(msm.build.solvate)
    assert inspect.signature(call) == native.replace(
        parameters=[
            *list(native.parameters.values())[1:],
            inspect.Parameter(
                "skip_digestion", inspect.Parameter.KEYWORD_ONLY, default=False
            ),
        ]
    )
    assert call.digestion_plan is not None and "solvate" in dir(
        view.addons.molsysmt.build
    )
    assert not hasattr(view.addons.molsysmt, "solvate")
    assert "not forwarded" in inspect.getdoc(call)
    assert "no update_view control" in inspect.getdoc(call)
    assert "\nmolecular_system :" not in inspect.getdoc(call)
    for name in inspect.signature(call).parameters:
        assert f"{name} :" in inspect.getdoc(call)
    for flag in ("molecular_system", "update_view", "in_place", "structure_indices"):
        with pytest.raises(UnknownArgumentError):
            call(**{flag: None})
    with pytest.raises(Exception):
        call(skip_digestion="yes")


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("clearance", ["0.35 nm", "3.5 angstroms"])
@pytest.mark.parametrize("length_unit", ["nm", "angstrom"])
def test_cube_matches_direct_openmm_geometry_units_and_independent_ownership(
    view, engine, skip, clearance, length_unit
):
    from openmm import unit

    expected = direct_modeller(view.molsys)
    expected_xyz = np.asarray(expected.positions.value_in_unit(unit.nanometer))
    expected_box = np.asarray(
        expected.topology.getPeriodicBoxVectors().value_in_unit(unit.nanometer)
    )
    with puw.context(standard_units=[length_unit, *energy_units("kJ/mol")[1:]]):
        before = snapshot(view)
        policy = dict(puw.configure.get_standard_units())
        result = view.addons.molsysmt.build.solvate(
            **{**PARAMETERS, "clearance": clearance}, skip_digestion=skip
        )
        assert result is not view.molsys
        actual_xyz = puw.get_value(result.structures.coordinates, to_unit="nm")[0]
        actual_box = puw.get_value(result.structures.box, to_unit="nm")[0]
        np.testing.assert_allclose(actual_box, expected_box, rtol=0, atol=1e-12)
        # Native origin placement may translate the whole engine output once.
        delta = actual_xyz - expected_xyz
        np.testing.assert_allclose(
            delta, np.broadcast_to(delta[0], delta.shape), rtol=0, atol=1e-10
        )
        np.testing.assert_allclose(
            (actual_xyz.min(axis=0) + actual_xyz.max(axis=0)) / 2,
            actual_box.sum(axis=0) / 2,
            rtol=0,
            atol=1e-10,
        )
        assert result.get_n_atoms() == len(expected_xyz)
        assert msm.get(result, n_structures=True) == 1
        assert msm.get(result, n_ions=True) == 0
        assert_water_geometry(result)
        assert not result.interactions
        assert dict(puw.configure.get_standard_units()) == policy
        unchanged(view, before)
        # Editing the independent result cannot change the current system/scene.
        msm.set(result, coordinates=puw.quantity(actual_xyz[None] + 1, "nm"))
        unchanged(view, before)


@pytest.mark.parametrize("shape", ["truncated octahedral", "rhombic dodecahedral"])
def test_declared_triclinic_geometry_keeps_solute_distances_and_water_geometry(
    view, engine, shape
):
    original = puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[0]
    before = snapshot(view)
    result = view.addons.molsysmt.build.solvate(**{**PARAMETERS, "box_shape": shape})
    box = puw.get_value(result.structures.box, to_unit="nm")[0]
    gram = box @ box.T
    length_squared = gram[0, 0]
    normalized = gram / length_squared
    expected = (
        np.array([[1, 1 / 3, -1 / 3], [1 / 3, 1, 1 / 3], [-1 / 3, 1 / 3, 1]])
        if shape == "truncated octahedral"
        else np.array([[1, 0, 0.5], [0, 1, 0.5], [0.5, 0.5, 1]])
    )
    np.testing.assert_allclose(normalized, expected, rtol=0, atol=1e-12)
    assert np.linalg.det(box) > 0
    actual = puw.get_value(result.structures.coordinates, to_unit="nm")[
        0, : len(original)
    ]
    np.testing.assert_allclose(
        actual - actual[0], original - original[0], rtol=0, atol=1e-12
    )
    assert_water_geometry(result)
    unchanged(view, before)


@pytest.mark.parametrize(
    "parameters",
    [
        {"engine": "invalid"},
        {"water_model": "invalid"},
        {"to_form": "invalid"},
    ],
)
@pytest.mark.parametrize("skip", [False, True])
def test_native_failures_keep_diagnostics_and_source(view, engine, parameters, skip):
    args = {**PARAMETERS, **parameters}
    before = snapshot(view)
    with pytest.raises(Exception) as native:
        msm.build.solvate(view.molsys, **args)
    with pytest.raises(type(native.value)) as actual:
        view.addons.molsysmt.build.solvate(**args, skip_digestion=skip)
    assert str(actual.value) == str(native.value)
    unchanged(view, before)


def test_multistructure_input_keeps_native_rejection_before_preparation(engine):
    with msv.demo["pentalanine"] as view:
        before = snapshot(view)
        with pytest.raises(Exception) as native:
            msm.build.solvate(view.molsys, **PARAMETERS)
        with pytest.raises(type(native.value)) as actual:
            view.addons.molsysmt.build.solvate(**PARAMETERS)
        assert str(actual.value) == str(native.value)
        unchanged(view, before)


def test_nonnumeric_identifier_rejection_is_native_and_source_is_preserved(
    view, engine
):
    msm.set(view.molsys, element="atom", selection=[0], atom_id="alpha")
    before = snapshot(view)
    with pytest.raises(ValueError) as native:
        msm.build.solvate(view.molsys, **PARAMETERS)
    with pytest.raises(type(native.value)) as actual:
        view.addons.molsysmt.build.solvate(**PARAMETERS)
    assert str(actual.value) == str(native.value)
    unchanged(view, before)


def test_explicit_openmm_counts_are_forwarded_without_hidden_compensation(view, engine):
    before = snapshot(view)
    args = {**PARAMETERS, "n_cations": 2, "n_anions": 2}
    native = msm.build.solvate(view.molsys, **args)
    result = view.addons.molsysmt.build.solvate(**args)
    # Known native limitation: these explicit counts are ignored by OpenMM.
    assert msm.get(native, n_ions=True) == msm.get(result, n_ions=True) == 0
    unchanged(view, before)


def test_pending_edits_are_used_without_synchronization_or_source_adoption(
    view, engine
):
    tools = view.addons.molsysmt
    tools.structure.translate(
        translation="[0.1,0,0] nm", in_place=True, update_view=False
    )
    before = snapshot(view)
    result = tools.build.solvate(**PARAMETERS)
    assert (
        result is not view.molsys and result.get_n_atoms() > view.molsys.get_n_atoms()
    )
    unchanged(view, before)


def test_cached_method_rebinds_and_rejects_closed_empty_views(view, engine):
    call = view.addons.molsysmt.build.solvate
    replacement = source()
    msm.set(replacement, element="atom", selection=[0], atom_id="replacement")
    view.load(replacement, mode="replace")
    before = snapshot(view)
    with pytest.raises(ValueError, match="replacement"):
        call(**PARAMETERS)
    unchanged(view, before)
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        call(**PARAMETERS)
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty.addons.molsysmt.build.solvate(**PARAMETERS)
