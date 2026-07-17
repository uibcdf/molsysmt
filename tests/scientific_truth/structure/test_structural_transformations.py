"""Analytic truth tests for deterministic coordinate transformations."""

import numpy as np

import molsysmt as msm
from molsysmt.native import Structures


def _structures(coordinates):
    return Structures(coordinates=np.asarray(coordinates) * msm.pyunitwizard.unit("nm"))


def _values(system):
    return msm.pyunitwizard.get_value(system.coordinates, to_unit="nm")


def test_translate_applies_known_per_frame_displacements(float64_kernel_atol):
    """Apply distinct closed-form translations without changing internal geometry."""

    coordinates = np.array(
        [
            [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
            [[0.0, 1.0, 0.0], [0.0, 1.0, 1.0]],
        ]
    )
    translation = np.array([[[2.0, -1.0, 0.5]], [[-1.0, 3.0, 2.0]]])
    observed = msm.structure.translate(
        _structures(coordinates),
        translation=translation * msm.pyunitwizard.unit("nm"),
    )

    np.testing.assert_allclose(
        _values(observed),
        coordinates + translation,
        rtol=0.0,
        atol=float64_kernel_atol,
    )


def test_center_moves_a_known_centroid_to_the_target(float64_kernel_atol):
    """Translate an explicit two-point centroid to a prescribed coordinate."""

    coordinates = np.array([[[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]]])
    target = np.array([[[1.0, 2.0, -1.0]]])
    observed = msm.structure.center(
        _structures(coordinates),
        center_coordinates=target * msm.pyunitwizard.unit("nm"),
    )
    expected = np.array([[[0.0, 2.0, -1.0], [2.0, 2.0, -1.0]]])

    np.testing.assert_allclose(
        _values(observed), expected, rtol=0.0, atol=float64_kernel_atol
    )


def test_flip_reflects_points_across_an_explicit_plane(float64_kernel_atol):
    """Reflect x coordinates across the plane x=1 while preserving y and z."""

    coordinates = np.array([[[0.0, 2.0, -1.0], [3.0, -2.0, 4.0]]])
    observed = msm.structure.flip(
        _structures(coordinates),
        vector=[1.0, 0.0, 0.0],
        point="[1.0, 0.0, 0.0] nm",
    )
    expected = np.array([[[2.0, 2.0, -1.0], [-1.0, -2.0, 4.0]]])

    np.testing.assert_allclose(
        _values(observed), expected, rtol=0.0, atol=float64_kernel_atol
    )


def test_move_away_applies_the_requested_outward_displacement(float64_kernel_atol):
    """Move one atom two nanometers along the explicit center-to-center direction."""

    coordinates = np.array([[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]])
    observed = msm.structure.move_away(
        _structures(coordinates),
        selection=[1],
        center_of_selection=[1],
        reference_center_of_selection=[0],
        distance="2 nm",
    )
    expected = np.array([[[0.0, 0.0, 0.0], [3.0, 0.0, 0.0]]])

    np.testing.assert_allclose(
        _values(observed), expected, rtol=0.0, atol=float64_kernel_atol
    )
