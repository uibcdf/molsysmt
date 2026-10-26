"""
Unit and regression test for the get_box_from_lengths_and_angles module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError

# Distance between atoms in space and time


def test_get_box_from_lengths_and_angles_1():
    angles = [[60.0, 60.0, 90.0]] * msm.pyunitwizard.unit("degrees")
    lengths = [[2.0, 2.0, 2.0]] * msm.pyunitwizard.unit("nm")
    box = msm.pbc.get_box_from_lengths_and_angles(lengths, angles)
    true_box = np.array([[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [1.0, 1.0, 1.414214]]])
    check = np.allclose(true_box, msm.pyunitwizard.get_value(box, to_unit="nm"))
    assert check


puw = msm.pyunitwizard


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize(
    "lengths", [[2.0, 3.0, 4.0], [[2.0, 3.0, 4.0], [5.0, 6.0, 7.0]]]
)
@pytest.mark.parametrize("angle_mode", ["omitted", "none", "degrees", "radians"])
def test_orthogonal_defaults_match_independent_diagonals(unit, lengths, angle_mode):
    expected = np.array([np.diag(row) for row in np.asarray(lengths).reshape(-1, 3)])
    kwargs = {}
    if angle_mode == "none":
        kwargs["box_angles"] = None
    elif angle_mode == "degrees":
        kwargs["box_angles"] = puw.quantity([90.0, 90.0, 90.0], "degrees")
    elif angle_mode == "radians":
        kwargs["box_angles"] = puw.quantity([np.pi / 2] * 3, "radians")
    with puw.context(standard_units=[unit, "fs"]):
        supplied = puw.convert(puw.quantity(lengths, "nm"), to_unit="angstrom")
        before = puw.get_value(supplied).copy()
        observed = msm.pbc.get_box_from_lengths_and_angles(supplied, **kwargs)
        np.testing.assert_array_equal(puw.get_value(supplied), before)
        assert observed.shape == expected.shape
        np.testing.assert_allclose(
            puw.get_value(observed, to_unit="nm"), expected, atol=1e-12
        )
        np.testing.assert_allclose(
            puw.get_value(observed), expected * (1000 if unit == "pm" else 1), atol=1e-9
        )


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("shared", [True, False])
def test_shared_and_per_structure_triclinic_angles_follow_length_rows(unit, shared):
    lengths = puw.quantity([[2.0, 2.0, 3.0], [4.0, 4.0, 5.0]], "nm")
    angles = (
        [[90.0, 90.0, 60.0]] if shared else [[90.0, 90.0, 90.0], [90.0, 90.0, 60.0]]
    )
    expected = np.array(
        [
            [[2.0, 0, 0], [1.0, np.sqrt(3.0), 0], [0, 0, 3.0]],
            [[4.0, 0, 0], [2.0, 2 * np.sqrt(3.0), 0], [0, 0, 5.0]],
        ]
    )
    if not shared:
        expected[0] = np.diag([2.0, 2.0, 3.0])
    with puw.context(standard_units=[unit, "fs"]):
        observed = msm.pbc.get_box_from_lengths_and_angles(
            lengths, puw.quantity(angles, "degrees")
        )
        np.testing.assert_allclose(
            puw.get_value(observed, to_unit="nm"), expected, atol=5e-7
        )


def test_raw_nm_lengths_and_empty_structure_axis_keep_defined_output_shapes():
    box = msm.pbc.get_box_from_lengths_and_angles(np.array([2.0, 3.0, 4.0]))
    assert box.shape == (1, 3, 3)
    np.testing.assert_array_equal(
        puw.get_value(box, to_unit="nm"), [np.diag([2.0, 3.0, 4.0])]
    )
    empty = msm.pbc.get_box_from_lengths_and_angles(np.empty((0, 3)))
    assert empty.shape == (0, 3, 3)
    assert puw.are_compatible(empty, "nm")


@pytest.mark.parametrize(
    "lengths,angles",
    [
        (puw.quantity([1, 2], "nm"), None),
        (puw.quantity([1, 2, 3], "ps"), None),
        (puw.quantity([1, 2, 3], "nm"), puw.quantity([90, 90], "degrees")),
        (puw.quantity([1, 2, 3], "nm"), puw.quantity([1, 2, 3], "nm")),
        (
            puw.quantity([[1, 2, 3]] * 3, "nm"),
            puw.quantity([[90, 90, 90]] * 2, "degrees"),
        ),
    ],
)
def test_invalid_units_shapes_and_angle_structure_counts_fail_before_kernel(
    lengths, angles
):
    with pytest.raises(ArgumentError):
        msm.pbc.get_box_from_lengths_and_angles(lengths, angles)


def test_factory_default_does_not_make_angles_optional_for_other_public_contracts():
    with pytest.raises(ArgumentError):
        msm.pbc.get_volume_from_lengths_and_angles(puw.quantity([2, 3, 4], "nm"), None)
