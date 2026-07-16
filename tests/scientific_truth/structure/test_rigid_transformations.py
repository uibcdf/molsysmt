"""Analytic scientific truth tests for explicit rigid transformations."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import Structures


def _structures(coordinates_nm):
    return Structures(coordinates=coordinates_nm * msm.pyunitwizard.unit("nm"))


def _values(system):
    return msm.pyunitwizard.get_value(system.coordinates, to_unit="nm")


def test_rotate_applies_distinct_matrices_per_frame(float64_kernel_atol):
    """Interpret `(n_frames, 3, 3)` as one rotation matrix per frame."""

    coordinates = np.array([[[1.0, 0.0, 0.0]], [[1.0, 0.0, 0.0]]])
    rotations = np.array(
        [
            np.eye(3),
            [[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]],
        ]
    )
    rotated = msm.structure.rotate(_structures(coordinates), rotation=rotations)

    np.testing.assert_allclose(
        _values(rotated),
        np.array([[[1.0, 0.0, 0.0]], [[0.0, 1.0, 0.0]]]),
        rtol=0.0,
        atol=float64_kernel_atol,
    )


def test_rotation_and_inverse_preserve_coordinates_and_distances(float64_kernel_atol):
    """Validate rigid invariance and an exact matrix-inverse round trip."""

    coordinates = np.array(
        [[[0.2, 0.3, 0.4], [1.1, -0.2, 0.7], [-0.3, 0.8, 1.4]]]
    )
    angle = np.deg2rad(31.0)
    rotation = np.array(
        [
            [np.cos(angle), 0.0, np.sin(angle)],
            [0.0, 1.0, 0.0],
            [-np.sin(angle), 0.0, np.cos(angle)],
        ]
    )
    system = _structures(coordinates)
    rotated = msm.structure.rotate(system, rotation=rotation)
    restored = msm.structure.rotate(rotated, rotation=rotation.T)

    original_distances = np.linalg.norm(coordinates[0, 1:] - coordinates[0, 0], axis=1)
    rotated_values = _values(rotated)
    rotated_distances = np.linalg.norm(
        rotated_values[0, 1:] - rotated_values[0, 0], axis=1
    )
    np.testing.assert_allclose(
        rotated_distances,
        original_distances,
        rtol=0.0,
        atol=float64_kernel_atol,
    )
    np.testing.assert_allclose(
        _values(restored), coordinates, rtol=0.0, atol=float64_kernel_atol
    )


def test_rotate_rejects_improper_or_nonorthogonal_matrices():
    """Reject reflections and scaling matrices at the public boundary."""

    system = _structures(np.zeros((1, 1, 3)))
    with pytest.raises(ArgumentError):
        msm.structure.rotate(system, rotation=np.diag([-1.0, 1.0, 1.0]))
    with pytest.raises(ArgumentError):
        msm.structure.rotate(system, rotation=np.diag([2.0, 1.0, 1.0]))


def test_rotate_rejects_nonbroadcastable_matrix_stacks():
    """Reject per-frame and per-atom stacks that do not match coordinates."""

    system = _structures(np.zeros((2, 3, 3)))
    with pytest.raises(StructuralInconsistencyError):
        msm.structure.rotate(system, rotation=np.repeat(np.eye(3)[None], 3, axis=0))
    with pytest.raises(StructuralInconsistencyError):
        msm.structure.rotate(
            system,
            rotation=np.repeat(np.eye(3)[None, None], 2, axis=1),
        )


@pytest.mark.parametrize(
    "fit_points",
    [
        np.array([[0.0, 0.0, 0.0]]),
        np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]),
        np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [2.0, 0.0, 0.0]]),
    ],
)
def test_least_rmsd_fit_rejects_underdetermined_rotations(fit_points):
    """Reject fit selections that cannot define a unique 3D rotation."""

    transformed = fit_points + np.array([2.0, -1.0, 0.5])
    system = _structures(np.stack([fit_points, transformed]))

    with pytest.raises(StructuralInconsistencyError):
        msm.structure.least_rmsd_fit(
            system,
            selection="all",
            selection_fit="all",
            reference_structure_index=0,
            use_gpu=False,
        )
