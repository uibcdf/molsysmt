"""Check nonbonded partition orientation, scalar parity and source ownership."""

import copy

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw

openmm = pytest.importorskip("openmm")


@pytest.mark.parametrize(
    "nested_left,nested_right",
    [(False, False), (True, False), (False, True), (True, True)],
)
@pytest.mark.parametrize("syntax", ["MolSysMT", "MDTraj"])
def test_mixed_partition_shapes_match_independent_scalar_calls(
    alanine_molsys, nested_left, nested_right, syntax
):
    molsys = msm.extract(alanine_molsys, structure_indices=0)
    left = [[3, 4, 5], [0, 1, 2]] if nested_left else [3, 4, 5]
    right = [[19, 20, 21], [10, 11, 12], [13, 14, 15]] if nested_right else [10, 11, 12]
    before = copy.deepcopy((left, right))
    coordinates = puw.get_value(molsys.get(coordinates=True), to_unit="nm").copy()
    energy = msm.molecular_mechanics.get_non_bonded_potential_energy
    with puw.context(
        standard_units=["angstrom", "ps", "kcal/mol", "e", "K", "radians"]
    ):
        policy = {
            k: v for k, v in puw.configure.report().items() if k != "loaded_libraries"
        }
        result = energy(
            molsys,
            selection=left,
            selection_2=right,
            platform="Reference",
            syntax=syntax,
        )
        rows = left if nested_left else [left]
        columns = right if nested_right else [right]
        expected = np.array(
            [
                [
                    puw.get_value(
                        energy(
                            molsys, selection=a, selection_2=b, platform="Reference"
                        ),
                        to_unit="kJ/mol",
                    )
                    for b in columns
                ]
                for a in rows
            ]
        )
        actual = puw.get_value(result, to_unit="kJ/mol")
        assert np.shape(actual) == (
            (len(rows), len(columns)) if nested_left or nested_right else ()
        )
        np.testing.assert_allclose(
            actual,
            expected if nested_left or nested_right else expected[0, 0],
            atol=1e-8,
            rtol=1e-10,
        )
        assert puw.get_unit(result) == puw.unit("kcal/mol")
        assert {
            k: v for k, v in puw.configure.report().items() if k != "loaded_libraries"
        } == policy
    assert (left, right) == before
    np.testing.assert_array_equal(
        puw.get_value(molsys.get(coordinates=True), to_unit="nm"), coordinates
    )


def test_repeated_partitions_and_shared_atoms_within_one_axis(alanine_molsys):
    molsys = msm.extract(alanine_molsys, structure_indices=0)
    left = [[0, 1, 2, 2], [1, 2, 3], [0, 1, 2]]
    right = [[10, 11, 12], [10, 11, 12], [11, 12, 13]]
    before = copy.deepcopy((left, right))
    energy = msm.molecular_mechanics.get_non_bonded_potential_energy
    result = puw.get_value(
        energy(molsys, selection=left, selection_2=right, platform="Reference"),
        to_unit="kJ/mol",
    )
    assert result.shape == (3, 3)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            scalar = energy(
                molsys,
                selection=sorted(set(a)),
                selection_2=sorted(set(b)),
                platform="Reference",
            )
            np.testing.assert_allclose(
                result[i, j],
                puw.get_value(scalar, to_unit="kJ/mol"),
                atol=1e-8,
                rtol=1e-10,
            )
    assert (left, right) == before


@pytest.mark.parametrize(
    "left,right,shape",
    [
        ([], [10, 11], ()),
        ([0, 1], [], ()),
        ([[], [0, 1]], [10, 11], (2, 1)),
        ([[0, 1]], [[10, 11], []], (1, 2)),
        ([[], []], [[]], (2, 1)),
    ],
)
def test_empty_selections_are_typed_zero_entries(alanine_molsys, left, right, shape):
    result = msm.molecular_mechanics.get_non_bonded_potential_energy(
        msm.extract(alanine_molsys, structure_indices=0),
        selection=left,
        selection_2=right,
        platform="Reference",
    )
    values = puw.get_value(result, to_unit="kJ/mol")
    assert np.shape(values) == shape
    assert puw.get_unit(result) == puw.unit("kJ/mol")
    rows = left if shape and left and isinstance(left[0], list) else [left]
    columns = right if shape and right and isinstance(right[0], list) else [right]
    expected = np.zeros((len(rows), len(columns)))
    for i, a in enumerate(rows):
        for j, b in enumerate(columns):
            if a and b:
                scalar = msm.molecular_mechanics.get_non_bonded_potential_energy(
                    msm.extract(alanine_molsys, structure_indices=0),
                    selection=a,
                    selection_2=b,
                    platform="Reference",
                )
                expected[i, j] = puw.get_value(scalar, to_unit="kJ/mol")
    np.testing.assert_array_equal(values, expected if shape else expected[0, 0])


def test_existing_context_system_and_energy_are_preserved(alanine_molsys):
    context = msm.convert(
        msm.extract(alanine_molsys, structure_indices=0),
        to_form="openmm.Context",
        platform="Reference",
    )
    system = context.getSystem()
    before = openmm.XmlSerializer.serialize(system)
    initial = context.getState(getEnergy=True).getPotentialEnergy()
    energy = msm.molecular_mechanics.get_non_bonded_potential_energy
    energy(context, selection=[[0, 1, 2], [3, 4, 5]], selection_2=[10, 11, 12])
    assert openmm.XmlSerializer.serialize(system) == before
    assert context.getState(getEnergy=True).getPotentialEnergy() == initial
    assert context.getPlatform().getName() == "Reference"


@pytest.mark.parametrize(
    "left,right",
    [
        ([0, 1], [1, 2]),
        ([[0, 1], [3, 4]], [1, 2]),
        ([0, 1], [[1, 2], [3, 4]]),
        ([[0, 1]], [[1, 2]]),
    ],
)
def test_atoms_shared_between_axes_are_rejected(alanine_molsys, left, right):
    from molsysmt._private.smonitor import ArgumentConflictError

    with pytest.raises(ArgumentConflictError, match="disjoint"):
        msm.molecular_mechanics.get_non_bonded_potential_energy(
            alanine_molsys, selection=left, selection_2=right, platform="Reference"
        )


@pytest.mark.parametrize(
    "selection", [None, [-1], [10000], [0.5], [[[0, 1]]], "not a valid selection"]
)
def test_invalid_selections_keep_native_diagnostics(alanine_molsys, selection):
    from molsysmt._private.smonitor import ArgumentError

    with pytest.raises(ArgumentError, match="selection"):
        msm.molecular_mechanics.get_non_bonded_potential_energy(
            alanine_molsys,
            selection=selection,
            selection_2=[10, 11],
            platform="Reference",
        )


def test_partitioned_internal_request_requires_a_second_selection(alanine_molsys):
    from molsysmt._private.smonitor import ArgumentConflictError

    with pytest.raises(ArgumentConflictError, match="explicit second selection"):
        msm.molecular_mechanics.get_non_bonded_potential_energy(
            alanine_molsys, selection=[[0, 1], [3, 4]], platform="Reference"
        )


def test_flat_internal_selection_deduplicates_and_empty_is_zero(alanine_molsys):
    molsys = msm.extract(alanine_molsys, structure_indices=0)
    energy = msm.molecular_mechanics.get_non_bonded_potential_energy
    unique = energy(molsys, selection=[0, 1, 2, 3], platform="Reference")
    repeated = energy(molsys, selection=[0, 1, 2, 3, 3], platform="Reference")
    np.testing.assert_allclose(
        puw.get_value(unique, to_unit="kJ/mol"),
        puw.get_value(repeated, to_unit="kJ/mol"),
        atol=1e-8,
        rtol=1e-10,
    )
    empty = energy(molsys, selection=[], platform="Reference")
    assert puw.get_value(empty, to_unit="kJ/mol") == 0.0


@pytest.mark.parametrize("platform", ["CPU", "Reference"])
def test_molsysmt_group_partitions_and_selection_strings(alanine_molsys, platform):
    molsys = msm.extract(alanine_molsys, structure_indices=0)
    energy = msm.molecular_mechanics.get_non_bonded_potential_energy
    result = energy(
        molsys,
        selection="all in groups of group_index in [0, 1]",
        selection_2="group_index == 2",
        platform=platform,
    )
    assert result.shape == (2, 1)
    for i in range(2):
        scalar = energy(
            molsys,
            selection=f"group_index == {i}",
            selection_2="group_index == 2",
            platform=platform,
        )
        np.testing.assert_allclose(
            puw.get_value(result[i, 0], to_unit="kJ/mol"),
            puw.get_value(scalar, to_unit="kJ/mol"),
            atol=1e-5,
            rtol=1e-6,
        )
    explicit = energy(
        molsys,
        selection=["group_index == 0", "group_index == 1"],
        selection_2="group_index == 2",
        platform=platform,
    )
    np.testing.assert_allclose(
        puw.get_value(result, to_unit="kJ/mol"),
        puw.get_value(explicit, to_unit="kJ/mol"),
        atol=1e-5,
        rtol=1e-6,
    )


def test_tuple_and_numpy_single_partitions_keep_matrix_axes(alanine_molsys):
    molsys = msm.extract(alanine_molsys, structure_indices=0)
    energy = msm.molecular_mechanics.get_non_bonded_potential_energy
    left = np.array([[0, 1, 2]], dtype=np.int64)
    right = ((10, 11, 12),)
    result = energy(molsys, selection=left, selection_2=right, platform="Reference")
    scalar = energy(
        molsys, selection=left[0], selection_2=right[0], platform="Reference"
    )
    assert result.shape == (1, 1)
    np.testing.assert_allclose(
        puw.get_value(result[0, 0], to_unit="kJ/mol"),
        puw.get_value(scalar, to_unit="kJ/mol"),
        atol=1e-8,
        rtol=1e-10,
    )
    np.testing.assert_array_equal(left, [[0, 1, 2]])
    assert right == ((10, 11, 12),)


def test_force_group_names_and_other_forces_do_not_change_nonbonded_energy(
    alanine_molsys,
):
    context = msm.convert(
        msm.extract(alanine_molsys, structure_indices=0),
        to_form="openmm.Context",
        platform="Reference",
    )
    energy = msm.molecular_mechanics.get_non_bonded_potential_energy
    expected = energy(context, selection=[[0, 1, 2]], selection_2=[10, 11, 12])
    system = msm.copy(context.getSystem())
    for force in system.getForces():
        force.setForceGroup(7)
        if isinstance(force, openmm.NonbondedForce):
            force.setName("renamed standard force")
    external = openmm.CustomExternalForce("10")
    external.addParticle(0, [])
    external.setForceGroup(7)
    system.addForce(external)
    modified = openmm.Context(
        system,
        openmm.VerletIntegrator(0.001),
        openmm.Platform.getPlatformByName("Reference"),
    )
    modified.setPositions(context.getState(getPositions=True).getPositions())
    before = openmm.XmlSerializer.serialize(system)
    actual = energy(modified, selection=[[0, 1, 2]], selection_2=[10, 11, 12])
    np.testing.assert_allclose(
        puw.get_value(actual, to_unit="kJ/mol"),
        puw.get_value(expected, to_unit="kJ/mol"),
        atol=1e-8,
        rtol=1e-10,
    )
    assert openmm.XmlSerializer.serialize(system) == before


@pytest.mark.parametrize("count", [0, 2])
def test_unsupported_nonbonded_force_counts_are_explicit(count):
    from molsysmt._private.smonitor import NotImplementedMethodError

    system = openmm.System()
    for _ in range(2):
        system.addParticle(12)
    for _ in range(count):
        force = openmm.NonbondedForce()
        force.addParticle(0, 0.3, 0.1)
        force.addParticle(0, 0.3, 0.1)
        system.addForce(force)
    context = openmm.Context(
        system,
        openmm.VerletIntegrator(0.001),
        openmm.Platform.getPlatformByName("Reference"),
    )
    context.setPositions([[0, 0, 0], [1, 0, 0]])
    before = openmm.XmlSerializer.serialize(system)
    with pytest.raises(NotImplementedMethodError, match="exactly one"):
        msm.molecular_mechanics.get_non_bonded_potential_energy(
            context, selection=[0], selection_2=[1]
        )
    assert openmm.XmlSerializer.serialize(system) == before


def test_periodic_context_keeps_its_current_box_instead_of_system_defaults():
    system = openmm.System()
    force = openmm.NonbondedForce()
    force.setNonbondedMethod(force.CutoffPeriodic)
    force.setCutoffDistance(1.0 * openmm.unit.nanometer)
    force.setUseDispersionCorrection(False)
    for charge in [1.0, -1.0]:
        system.addParticle(12)
        force.addParticle(charge, 0.3, 0.0)
    system.addForce(force)
    system.setDefaultPeriodicBoxVectors(*np.eye(3) * 2.0 * openmm.unit.nanometer)
    context = openmm.Context(
        system,
        openmm.VerletIntegrator(0.001),
        openmm.Platform.getPlatformByName("Reference"),
    )
    current_box = np.eye(3) * 3.0 * openmm.unit.nanometer
    context.setPeriodicBoxVectors(*current_box)
    context.setPositions(np.array([[0, 0, 0], [1.3, 0, 0]]) * openmm.unit.nanometer)
    before = openmm.XmlSerializer.serialize(system)
    # In the current 3 nm cell, the separation exceeds the 1 nm cutoff.
    # The stored 2 nm defaults would wrap it to 0.7 nm and give a nonzero value.
    for left in [[0], [[0]]]:
        value = msm.molecular_mechanics.get_non_bonded_potential_energy(
            context, selection=left, selection_2=[1]
        )
        np.testing.assert_allclose(
            puw.get_value(value, to_unit="kJ/mol"), 0.0, atol=1e-12
        )
    np.testing.assert_array_equal(
        puw.get_value(context.getState().getPeriodicBoxVectors(), to_unit="nm"),
        np.eye(3) * 3.0,
    )
    assert openmm.XmlSerializer.serialize(system) == before


def test_get_non_bonded_potential_energy_1():

    import molsysmt as msm

    molecular_system = msm.convert(
        msm.systems["Barnase-Barstar"]["barnase_barstar.h5msm"]
    )

    U1nb2 = msm.molecular_mechanics.get_non_bonded_potential_energy(
        molecular_system,
        selection='molecule_name=="BARNASE"',
        selection_2='molecule_name=="BARSTAR"',
    )

    assert puw.get_unit(U1nb2) == puw.unit("kilojoule/mole")


def test_get_non_bonded_potential_energy_2():

    import molsysmt as msm

    molecular_system = msm.convert(
        msm.systems["Barnase-Barstar"]["barnase_barstar.h5msm"]
    )

    U12_groups = msm.molecular_mechanics.get_non_bonded_potential_energy(
        molecular_system,
        selection="all in groups of group_index in [0,1,2]",
        selection_2="all in groups of group_index in [100,101,102]",
    )

    assert U12_groups.shape == (3, 3)
    assert puw.get_unit(U12_groups) == puw.unit("kilojoule/mole")
