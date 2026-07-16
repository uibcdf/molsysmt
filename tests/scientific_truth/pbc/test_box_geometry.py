"""Analytic truth tests for periodic-box geometry."""

import numpy as np

import molsysmt as msm


def _values(quantity, unit):
    return msm.pyunitwizard.get_value(quantity, to_unit=unit)


def test_orthorhombic_box_has_exact_geometry(
    public_six_decimal_atol,
    float64_kernel_atol,
):
    """Validate the 2 x 3 x 4 nm orthorhombic box against closed-form truth."""

    box = np.diag([2.0, 3.0, 4.0])[None, :, :] * msm.pyunitwizard.unit("nm")

    lengths, angles = msm.pbc.get_lengths_and_angles_from_box(box)
    volume = msm.pbc.get_volume_from_box(box)

    np.testing.assert_allclose(
        _values(lengths, "nm"),
        [[2.0, 3.0, 4.0]],
        rtol=0.0,
        atol=public_six_decimal_atol,
    )
    np.testing.assert_allclose(
        _values(angles, "degrees"),
        [[90.0, 90.0, 90.0]],
        rtol=0.0,
        atol=public_six_decimal_atol * 180.0 / np.pi,
    )
    np.testing.assert_allclose(
        _values(volume, "nm**3"),
        [24.0],
        rtol=0.0,
        atol=float64_kernel_atol,
    )


def test_triclinic_box_has_exact_lengths_angles_and_volume(
    public_six_decimal_atol,
    float64_kernel_atol,
):
    """Validate a 60-degree triclinic cell with volume 6 sqrt(3) nm^3."""

    sqrt_three = np.sqrt(3.0)
    box_values = np.array(
        [[[2.0, 0.0, 0.0], [1.0, sqrt_three, 0.0], [0.0, 0.0, 3.0]]]
    )
    box = box_values * msm.pyunitwizard.unit("nm")

    lengths, angles = msm.pbc.get_lengths_and_angles_from_box(box)
    volume = msm.pbc.get_volume_from_box(box)

    np.testing.assert_allclose(
        _values(lengths, "nm"),
        [[2.0, 2.0, 3.0]],
        rtol=0.0,
        atol=public_six_decimal_atol,
    )
    np.testing.assert_allclose(
        _values(angles, "radians"),
        [[np.pi / 2.0, np.pi / 2.0, np.pi / 3.0]],
        rtol=0.0,
        atol=public_six_decimal_atol,
    )
    np.testing.assert_allclose(
        _values(volume, "nm**3"),
        [6.0 * sqrt_three],
        rtol=0.0,
        atol=float64_kernel_atol,
    )


def test_box_constructor_matches_the_canonical_triclinic_matrix(public_six_decimal_atol):
    """Validate the canonical row-vector matrix for alpha=beta=90, gamma=60 degrees."""

    lengths = [[2.0, 2.0, 3.0]] * msm.pyunitwizard.unit("nm")
    angles = [[90.0, 90.0, 60.0]] * msm.pyunitwizard.unit("degrees")
    expected = np.array(
        [[[2.0, 0.0, 0.0], [1.0, np.sqrt(3.0), 0.0], [0.0, 0.0, 3.0]]]
    )

    observed = msm.pbc.get_box_from_lengths_and_angles(lengths, angles)

    np.testing.assert_allclose(
        _values(observed, "nm"),
        expected,
        rtol=0.0,
        atol=public_six_decimal_atol,
    )


def test_triclinic_volume_from_lengths_and_angles_matches_closed_form(float64_kernel_atol):
    """Validate V=abc*sqrt(1+2cos(a)cos(b)cos(g)-sum(cos^2))."""

    lengths = [[2.0, 2.0, 3.0]] * msm.pyunitwizard.unit("nm")
    angles = [[90.0, 90.0, 60.0]] * msm.pyunitwizard.unit("degrees")

    observed = msm.pbc.get_volume_from_lengths_and_angles(lengths, angles)

    np.testing.assert_allclose(
        _values(observed, "nm**3"),
        [6.0 * np.sqrt(3.0)],
        rtol=0.0,
        atol=float64_kernel_atol,
    )
