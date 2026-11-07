"""Use signed analytic matrices and rigid invariants to qualify axis-angle rotations."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw

QUARTER_TURNS = np.array(
    [
        [[1, 0, 0], [0, 0, -1], [0, 1, 0]],
        [[0, 0, 1], [0, 1, 0], [-1, 0, 0]],
        [[0, -1, 0], [1, 0, 0], [0, 0, 1]],
    ],
    dtype=float,
)


@pytest.mark.parametrize("axis_index", [0, 1, 2])
@pytest.mark.parametrize("sign", [-1, 1])
def test_signed_cartesian_quarter_turns_match_literal_matrices(
    axis_index, sign, float64_kernel_atol
):
    axis = np.eye(3)[axis_index]
    expected = QUARTER_TURNS[axis_index]
    if sign < 0:
        expected = expected.T
    observed = msm.structure.get_rotation_matrix_from_axis_angle(
        axis, puw.quantity(sign * 90, "degree")
    )
    np.testing.assert_allclose(observed, expected, rtol=0, atol=float64_kernel_atol)


def test_positive_body_diagonal_turn_cycles_cartesian_axes(float64_kernel_atol):
    expected = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    observed = msm.structure.get_rotation_matrix_from_axis_angle(
        [1, 1, 1], "120 degrees"
    )
    np.testing.assert_allclose(observed, expected, rtol=0, atol=float64_kernel_atol)
    np.testing.assert_allclose(
        np.eye(3) @ observed.T, expected.T, rtol=0, atol=float64_kernel_atol
    )


@pytest.mark.parametrize("scale", [1e-300, 1e300, -1e-300, -1e300])
def test_axis_rescaling_preserves_direction_and_negative_scale_reverses_angle(
    scale, float64_kernel_atol
):
    base = np.array([2.0, -3.0, 1.0])
    expected = msm.structure.get_rotation_matrix_from_axis_angle(base, "37 degrees")
    if scale < 0:
        expected = expected.T
    axis = base * scale
    before = axis.copy()
    observed = msm.structure.get_rotation_matrix_from_axis_angle(axis, "37 degrees")
    np.testing.assert_allclose(observed, expected, rtol=0, atol=float64_kernel_atol)
    np.testing.assert_array_equal(axis, before)


@pytest.mark.parametrize(
    "component", [np.nextafter(0.0, 1.0), np.finfo(np.float64).max]
)
def test_extreme_finite_axis_still_produces_the_analytic_rotation(
    component, float64_kernel_atol
):
    observed = msm.structure.get_rotation_matrix_from_axis_angle(
        [0, 0, component], "90 degrees"
    )
    np.testing.assert_allclose(
        observed, QUARTER_TURNS[2], rtol=0, atol=float64_kernel_atol
    )


def test_rotation_is_proper_fixed_axis_and_composes_with_its_inverse(
    float64_kernel_atol,
):
    axis = np.array([2.0, -3.0, 1.0])
    first = msm.structure.get_rotation_matrix_from_axis_angle(axis, "37 degrees")
    second = msm.structure.get_rotation_matrix_from_axis_angle(axis, "-11 degrees")
    total = msm.structure.get_rotation_matrix_from_axis_angle(axis, "26 degrees")
    inverse = msm.structure.get_rotation_matrix_from_axis_angle(axis, "-37 degrees")
    periodic = msm.structure.get_rotation_matrix_from_axis_angle(axis, "397 degrees")
    np.testing.assert_allclose(
        first @ first.T, np.eye(3), rtol=0, atol=float64_kernel_atol
    )
    assert abs(np.linalg.det(first) - 1) <= float64_kernel_atol
    np.testing.assert_allclose(first @ axis, axis, rtol=0, atol=float64_kernel_atol)
    np.testing.assert_allclose(second @ first, total, rtol=0, atol=float64_kernel_atol)
    np.testing.assert_allclose(inverse, first.T, rtol=0, atol=float64_kernel_atol)
    np.testing.assert_allclose(periodic, first, rtol=0, atol=float64_kernel_atol)


def test_constructed_matrix_drives_public_row_vector_rotation(float64_kernel_atol):
    coordinates = puw.quantity([[[1, 0, 0], [0, 1, 0], [0, 0, 1]]], "nm")
    before = np.asarray(puw.get_value(coordinates)).copy()
    rotation = msm.structure.get_rotation_matrix_from_axis_angle(
        [0, 0, 2], "90 degrees"
    )
    output = msm.structure.rotate(coordinates, rotation=rotation)
    expected = [[[0, 1, 0], [-1, 0, 0], [0, 0, 1]]]
    values = puw.get_value(output, to_unit="nm")
    np.testing.assert_allclose(values, expected, rtol=0, atol=float64_kernel_atol)
    np.testing.assert_array_equal(puw.get_value(coordinates), before)
    np.testing.assert_allclose(
        np.linalg.norm(values[0, 1:] - values[0, 0], axis=1),
        [np.sqrt(2), np.sqrt(2)],
        rtol=0,
        atol=float64_kernel_atol,
    )


def test_valid_zero_angle_is_identity_and_subnormal_angle_is_not_thresholded():
    identity = msm.structure.get_rotation_matrix_from_axis_angle(
        [2, -3, 1], "0 degrees"
    )
    np.testing.assert_array_equal(identity, np.eye(3))
    tiny = np.nextafter(0.0, 1.0)
    rotation = msm.structure.get_rotation_matrix_from_axis_angle(
        [0, 0, 1], puw.quantity(tiny, "radians")
    )
    assert rotation[1, 0] == tiny
    assert rotation[0, 1] == -tiny
