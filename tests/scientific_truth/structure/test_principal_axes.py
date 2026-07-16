"""Analytic scientific truth tests for principal structural axes."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.native import Structures


def _structures(coordinates_nm):
    return Structures(coordinates=coordinates_nm * msm.pyunitwizard.unit("nm"))


def _anisotropic_points():
    return np.array(
        [
            [3.0, 0.0, 0.0],
            [-3.0, 0.0, 0.0],
            [0.0, 2.0, 0.0],
            [0.0, -2.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 0.0, -1.0],
        ]
    )


def _axis_projectors(axes):
    return np.einsum("...ik,...il->...ikl", axes, axes)


def test_geometric_axes_match_closed_form_and_rotate_covariantly(float64_kernel_atol):
    """Validate covariance eigenpairs and their rigid-rotation covariance."""

    reference = _anisotropic_points()
    rotation = np.array(
        [[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    )
    transformed = reference @ rotation.T + np.array([4.0, -3.0, 2.0])
    axes, variances = msm.structure.get_principal_axes(
        _structures(np.stack([reference, transformed])),
        principal_axes_type="geometric",
        use_gpu=False,
    )

    expected_variances = np.array([1.0 / 3.0, 4.0 / 3.0, 3.0])
    expected_reference_axes = np.array(
        [[0.0, 0.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]]
    )
    expected_transformed_axes = expected_reference_axes @ rotation.T

    np.testing.assert_allclose(
        variances,
        np.repeat(expected_variances[None, :], 2, axis=0),
        rtol=0.0,
        atol=float64_kernel_atol,
    )
    np.testing.assert_allclose(
        _axis_projectors(axes),
        _axis_projectors(np.stack([expected_reference_axes, expected_transformed_axes])),
        rtol=0.0,
        atol=float64_kernel_atol,
    )
    np.testing.assert_allclose(
        axes @ np.swapaxes(axes, -1, -2),
        np.repeat(np.eye(3)[None, :, :], 2, axis=0),
        rtol=0.0,
        atol=float64_kernel_atol,
    )
    np.testing.assert_allclose(
        np.linalg.det(axes), 1.0, rtol=0.0, atol=float64_kernel_atol
    )


def test_inertia_axes_and_moments_match_closed_form(float64_kernel_atol):
    """Validate a diagonal point-mass inertia tensor exactly."""

    axes, moments = msm.structure.get_principal_axes(
        _structures(_anisotropic_points()[None, :, :]),
        principal_axes_type="inertia",
        use_gpu=False,
    )

    np.testing.assert_allclose(
        moments,
        np.array([[10.0, 20.0, 26.0]]),
        rtol=0.0,
        atol=float64_kernel_atol,
    )
    np.testing.assert_allclose(
        _axis_projectors(axes),
        _axis_projectors(np.eye(3)[None, :, :]),
        rtol=0.0,
        atol=float64_kernel_atol,
    )


def test_mass_keyword_matches_explicit_atomic_masses(float64_kernel_atol):
    """Validate the physical-mass shortcut against explicitly retrieved masses."""

    molecular_system = msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']
    masses = msm.physchem.get_mass(molecular_system, element='atom')
    axes_keyword, moments_keyword = msm.structure.get_principal_axes(
        molecular_system,
        structure_indices=0,
        weights='masses',
        use_gpu=False,
    )
    axes_explicit, moments_explicit = msm.structure.get_principal_axes(
        molecular_system,
        structure_indices=0,
        weights=masses,
        use_gpu=False,
    )

    np.testing.assert_allclose(
        _axis_projectors(axes_keyword),
        _axis_projectors(axes_explicit),
        rtol=0.0,
        atol=float64_kernel_atol,
    )
    np.testing.assert_allclose(
        moments_keyword,
        moments_explicit,
        rtol=0.0,
        atol=float64_kernel_atol,
    )


def test_align_principal_axes_maps_unique_axes_to_target(float64_kernel_atol):
    """Align a rotated anisotropic body to the Cartesian target basis."""

    angle = np.deg2rad(37.0)
    rotation = np.array(
        [
            [np.cos(angle), -np.sin(angle), 0.0],
            [np.sin(angle), np.cos(angle), 0.0],
            [0.0, 0.0, 1.0],
        ]
    )
    coordinates = _anisotropic_points() @ rotation.T + np.array([3.0, 2.0, -1.0])
    aligned = msm.structure.align_principal_axes(
        _structures(coordinates[None, :, :]),
        principal_axes_type="inertia",
        axes=np.eye(3),
        center=True,
    )
    axes, moments = msm.structure.get_principal_axes(
        aligned, principal_axes_type="inertia", use_gpu=False
    )

    np.testing.assert_allclose(
        _axis_projectors(axes),
        _axis_projectors(np.eye(3)[None, :, :]),
        rtol=0.0,
        atol=float64_kernel_atol,
    )
    np.testing.assert_allclose(
        moments,
        np.array([[10.0, 20.0, 26.0]]),
        rtol=0.0,
        atol=float64_kernel_atol,
    )
    center = msm.structure.get_center(aligned, heavy_mode="off")
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(center, to_unit="nm"),
        0.0,
        rtol=0.0,
        atol=float64_kernel_atol,
    )


def test_align_principal_axes_uses_relative_degeneracy_tolerance(
    float64_kernel_atol,
):
    """Preserve distinct axes when the complete geometry is uniformly tiny."""

    coordinates = _anisotropic_points() * 1.0e-6
    aligned = msm.structure.align_principal_axes(
        _structures(coordinates[None, :, :]),
        principal_axes_type="inertia",
        axes=np.eye(3),
    )
    axes, _ = msm.structure.get_principal_axes(
        aligned, principal_axes_type="inertia", use_gpu=False
    )

    np.testing.assert_allclose(
        _axis_projectors(axes),
        _axis_projectors(np.eye(3)[None, :, :]),
        rtol=0.0,
        atol=float64_kernel_atol,
    )


def test_align_principal_axes_rejects_degenerate_axes():
    """Reject an isotropic body whose individual principal axes are undefined."""

    coordinates = np.array(
        [
            [1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 0.0, -1.0],
        ]
    )

    with pytest.raises(StructuralInconsistencyError):
        msm.structure.align_principal_axes(_structures(coordinates[None, :, :]))


def test_align_principal_axes_rejects_invalid_target_basis():
    """Reject target axes that contain scaling instead of a proper rotation."""

    with pytest.raises(StructuralInconsistencyError):
        msm.structure.align_principal_axes(
            _structures(_anisotropic_points()[None, :, :]),
            axes=np.diag([2.0, 1.0, 1.0]),
        )
