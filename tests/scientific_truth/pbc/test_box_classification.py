"""Analytic truth tests for public box decomposition and classification."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import Structures


def _values(quantity, unit):
    return msm.pyunitwizard.get_value(quantity, to_unit=unit)


def test_box_lengths_match_row_vector_norms(public_six_decimal_atol):
    """Recover three independently known row-vector norms."""

    box = np.array(
        [[[3.0, 0.0, 0.0], [1.0, 4.0, 0.0], [-2.0, 1.0, 5.0]]]
    ) * msm.pyunitwizard.unit("nm")
    observed = msm.pbc.get_lengths_from_box(box)
    expected = np.array([[3.0, np.sqrt(17.0), np.sqrt(30.0)]])

    np.testing.assert_allclose(
        _values(observed, "nm"),
        expected,
        rtol=0.0,
        atol=public_six_decimal_atol,
    )


def test_box_angles_match_closed_form_dot_products(public_six_decimal_atol):
    """Recover alpha=90, beta=90, and gamma=60 degrees from explicit vectors."""

    box = np.array(
        [[[2.0, 0.0, 0.0], [1.0, np.sqrt(3.0), 0.0], [0.0, 0.0, 3.0]]]
    ) * msm.pyunitwizard.unit("nm")
    observed = msm.pbc.get_angles_from_box(box)
    expected = np.deg2rad([[90.0, 90.0, 60.0]])

    np.testing.assert_allclose(
        _values(observed, "radians"),
        expected,
        rtol=0.0,
        atol=public_six_decimal_atol,
    )


@pytest.mark.parametrize(
    ("shape", "unit_box"),
    [
        ("cubic", np.eye(3)),
        (
            "truncated octahedral",
            np.array(
                [
                    [1.0, 0.0, 0.0],
                    [1.0 / 3.0, 2.0 * np.sqrt(2.0) / 3.0, 0.0],
                    [-1.0 / 3.0, np.sqrt(2.0) / 3.0, np.sqrt(6.0) / 3.0],
                ]
            ),
        ),
        (
            "rhombic dodecahedral",
            np.array(
                [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.5, 0.5, 1.0 / np.sqrt(2.0)]]
            ),
        ),
    ],
)
def test_box_shape_constructors_match_canonical_vectors(
    shape,
    unit_box,
    float64_kernel_atol,
):
    """Construct each supported canonical cell for two frames."""

    observed = msm.pbc.get_box_with_shape(
        shape=shape,
        length="2 nm",
        n_structures=2,
    )
    expected = np.repeat((2.0 * unit_box)[None, :, :], 2, axis=0)

    np.testing.assert_allclose(
        _values(observed, "nm"),
        expected,
        rtol=0.0,
        atol=float64_kernel_atol,
    )


@pytest.mark.parametrize(
    ("angles_degrees", "expected"),
    [
        ([90.0, 90.0, 90.0], "cubic"),
        ([70.52878, 109.471221, 70.52878], "truncated octahedral"),
        ([60.0, 60.0, 90.0], "rhombic dodecahedral"),
        ([70.0, 80.0, 90.0], "triclinic"),
    ],
)
def test_shape_classification_matches_exact_angle_signatures(angles_degrees, expected):
    """Classify canonical angle signatures and a generic triclinic cell."""

    angles = np.array([angles_degrees]) * msm.pyunitwizard.unit("degrees")

    assert msm.pbc.get_shape_from_angles(angles) == expected


@pytest.mark.parametrize(
    ("box", "expected"),
    [
        (np.eye(3), "cubic"),
        (
            np.array(
                [
                    [1.0, 0.0, 0.0],
                    [1.0 / 3.0, 2.0 * np.sqrt(2.0) / 3.0, 0.0],
                    [-1.0 / 3.0, np.sqrt(2.0) / 3.0, np.sqrt(6.0) / 3.0],
                ]
            ),
            "truncated octahedral",
        ),
        (
            np.array(
                [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.5, 0.5, 1.0 / np.sqrt(2.0)]]
            ),
            "rhombic dodecahedral",
        ),
    ],
)
def test_shape_classification_matches_explicit_box_vectors(box, expected):
    """Classify independently declared canonical row-vector boxes."""

    quantity = box[None, :, :] * msm.pyunitwizard.unit("nm")

    assert msm.pbc.get_shape_from_box(quantity) == expected


def test_has_pbc_reports_box_presence_exactly():
    """Distinguish coordinate-only structures from structures carrying a box."""

    coordinates = np.zeros((1, 2, 3)) * msm.pyunitwizard.unit("nm")
    without_box = Structures(coordinates=coordinates)
    with_box = Structures(
        coordinates=coordinates,
        box=np.eye(3)[None, :, :] * msm.pyunitwizard.unit("nm"),
    )

    assert msm.pbc.has_pbc(without_box) is False
    assert msm.pbc.has_pbc(with_box) is True
