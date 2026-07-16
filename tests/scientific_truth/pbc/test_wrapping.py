"""Analytic scientific truth tests for wrapping and temporal unwrapping."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.native import Structures


def _values(system):
    return msm.pyunitwizard.get_value(system.coordinates, to_unit="nm")


def _system(coordinates, box):
    unit = msm.pyunitwizard.unit("nm")
    return Structures(coordinates=coordinates * unit, box=box * unit)


def _bonded_system(coordinates, box):
    builder = msm.MolSysBuilder()
    atom_indices = [
        builder.add_atom(atom_name="C", atom_type="C") for _ in range(coordinates.shape[1])
    ]
    builder.add_group(atom_indices, group_name="MOL")
    for atom_1, atom_2 in zip(atom_indices[:-1], atom_indices[1:]):
        builder.add_bond(atom_1, atom_2)
    builder.set_coordinates(coordinates * msm.pyunitwizard.unit("nm"))
    builder.set_box(box * msm.pyunitwizard.unit("nm"))
    return builder.build()


def test_wrap_to_pbc_changes_only_requested_frames(float64_kernel_atol):
    """Apply primary-cell wrapping only to explicitly selected structures."""

    coordinates = np.array([[[2.2, 0.0, 0.0]], [[2.4, 0.0, 0.0]], [[2.6, 0.0, 0.0]]])
    box = np.repeat((2.0 * np.eye(3))[None, :, :], 3, axis=0)
    wrapped = msm.pbc.wrap_to_pbc(
        _system(coordinates, box), structure_indices=[1], in_place=False
    )

    expected = coordinates.copy()
    expected[1, 0, 0] = 0.4
    np.testing.assert_allclose(
        _values(wrapped), expected, rtol=0.0, atol=float64_kernel_atol
    )


def test_wrap_to_mic_changes_only_requested_frames(float64_kernel_atol):
    """Apply minimum-image wrapping only to explicitly selected structures."""

    coordinates = np.array([[[1.2, 0.0, 0.0]], [[1.4, 0.0, 0.0]], [[1.6, 0.0, 0.0]]])
    box = np.repeat((2.0 * np.eye(3))[None, :, :], 3, axis=0)
    wrapped = msm.pbc.wrap_to_mic(
        _system(coordinates, box), structure_indices=[1], in_place=False
    )

    expected = coordinates.copy()
    expected[1, 0, 0] = -0.6
    np.testing.assert_allclose(
        _values(wrapped), expected, rtol=0.0, atol=float64_kernel_atol
    )


def test_temporal_unwrap_recovers_continuous_orthorhombic_motion(float64_kernel_atol):
    """Recover a particle trajectory that crosses an orthorhombic boundary."""

    wrapped = np.array([[[0.8, 0.0, 0.0]], [[-0.8, 0.0, 0.0]], [[-0.4, 0.0, 0.0]]])
    box = np.repeat((2.0 * np.eye(3))[None, :, :], 3, axis=0)
    unwrapped = msm.pbc.unwrap(_system(wrapped, box), in_place=False)
    expected = np.array([[[0.8, 0.0, 0.0]], [[1.2, 0.0, 0.0]], [[1.6, 0.0, 0.0]]])

    np.testing.assert_allclose(
        _values(unwrapped), expected, rtol=0.0, atol=float64_kernel_atol
    )


def test_temporal_unwrap_changes_only_requested_frames(float64_kernel_atol):
    """Keep unselected frames untouched while unwrapping the selected subsequence."""

    wrapped = np.array([[[7.0, 0.0, 0.0]], [[0.8, 0.0, 0.0]], [[-0.8, 0.0, 0.0]]])
    box = np.repeat((2.0 * np.eye(3))[None, :, :], 3, axis=0)
    unwrapped = msm.pbc.unwrap(
        _system(wrapped, box), structure_indices=[1, 2], in_place=False
    )
    expected = wrapped.copy()
    expected[2, 0, 0] = 1.2

    np.testing.assert_allclose(
        _values(unwrapped), expected, rtol=0.0, atol=float64_kernel_atol
    )


def test_temporal_unwrap_recovers_continuous_triclinic_motion(float64_kernel_atol):
    """Recover continuous fractional motion across a triclinic cell boundary."""

    box_matrix = np.array(
        [[2.0, 0.0, 0.0], [1.0, np.sqrt(3.0), 0.0], [0.0, 0.0, 3.0]]
    )
    wrapped_fractional = np.array([[0.9, 0.9, 0.0], [0.1, 0.1, 0.0]])
    expected_fractional = np.array([[0.9, 0.9, 0.0], [1.1, 1.1, 0.0]])
    coordinates = (wrapped_fractional @ box_matrix)[:, None, :]
    expected = (expected_fractional @ box_matrix)[:, None, :]
    box = np.repeat(box_matrix[None, :, :], 2, axis=0)

    unwrapped = msm.pbc.unwrap(_system(coordinates, box), in_place=False)

    np.testing.assert_allclose(
        _values(unwrapped), expected, rtol=0.0, atol=float64_kernel_atol
    )


def test_wrap_to_pbc_reconstructs_a_boundary_spanning_covalent_block(float64_kernel_atol):
    """Preserve analytic bond lengths while wrapping a molecule as one unit."""

    coordinates = np.array([[[1.8, 0.0, 0.0], [0.1, 0.0, 0.0], [0.3, 0.0, 0.0]]])
    box = (2.0 * np.eye(3))[None, :, :]
    wrapped = msm.pbc.wrap_to_pbc(
        _bonded_system(coordinates, box),
        keep_covalent_bonds=True,
        in_place=False,
    )
    observed = msm.pyunitwizard.get_value(wrapped.structures.coordinates, to_unit="nm")
    bond_lengths = np.linalg.norm(np.diff(observed[0], axis=0), axis=1)

    np.testing.assert_allclose(
        bond_lengths,
        np.array([0.3, 0.2]),
        rtol=0.0,
        atol=float64_kernel_atol,
    )
    center_fractional = np.mean(observed[0], axis=0) @ np.linalg.inv(box[0])
    assert np.all(center_fractional >= 0.0)
    assert np.all(center_fractional < 1.0)


def test_wrap_to_mic_reconstructs_a_triclinic_covalent_block(float64_kernel_atol):
    """Preserve a bonded displacement across a triclinic boundary."""

    box_matrix = np.array(
        [[2.0, 0.0, 0.0], [1.0, np.sqrt(3.0), 0.0], [0.0, 0.0, 3.0]]
    )
    fractional = np.array([[0.9, 0.9, 0.0], [0.1, 0.1, 0.0]])
    coordinates = (fractional @ box_matrix)[None, :, :]
    wrapped = msm.pbc.wrap_to_mic(
        _bonded_system(coordinates, box_matrix[None, :, :]),
        keep_covalent_bonds=True,
        in_place=False,
    )
    observed = msm.pyunitwizard.get_value(wrapped.structures.coordinates, to_unit="nm")
    expected_displacement = np.array([0.2, 0.2, 0.0]) @ box_matrix

    np.testing.assert_allclose(
        observed[0, 1] - observed[0, 0],
        expected_displacement,
        rtol=0.0,
        atol=float64_kernel_atol,
    )


def test_periodic_transformations_reject_missing_and_singular_boxes():
    """Reject periodic operations whose cell geometry is undefined."""

    coordinates = np.zeros((2, 1, 3), dtype=np.float64)
    no_box = Structures(coordinates=coordinates * msm.pyunitwizard.unit("nm"))
    singular_box = np.zeros((1, 3, 3), dtype=np.float64)

    with pytest.raises(StructuralInconsistencyError):
        msm.pbc.unwrap(no_box)
    with pytest.raises(StructuralInconsistencyError):
        msm.pbc.wrap_to_pbc(_system(coordinates, singular_box))
