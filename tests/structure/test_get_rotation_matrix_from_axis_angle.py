"""Protect explicit angle units, singleton inputs and constructor ownership."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest.argument.angle import digest_angle
from molsysmt._private.argdigest.argument.axis import digest_axis
from molsysmt._private.smonitor import ArgumentError

EXPECTED_Z_QUARTER = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=float)
CONSTRUCTOR_CALLER = (
    "molsysmt.structure.get_rotation_matrix_from_axis_angle."
    "get_rotation_matrix_from_axis_angle"
)


@pytest.mark.parametrize("standards", [["angstrom", "ps", "degrees"], ["nm", "ps"]])
@pytest.mark.parametrize(
    "form", ["degree_string", "radian_string", "degree_quantity", "radian_quantity"]
)
def test_explicit_angle_units_ignore_display_policy_and_preserve_it(standards, form):
    with puw.context(standard_units=standards):
        inputs = {
            "degree_string": "90 degree",
            "radian_string": f"{np.pi / 2} radians",
            "degree_quantity": puw.quantity(np.array(90.0), "degree"),
            "radian_quantity": puw.quantity(np.pi / 2, "radians"),
        }
        angle = inputs[form]
        before = puw.configure.report()
        rotation = msm.structure.get_rotation_matrix_from_axis_angle([0, 0, 7], angle)
        after = puw.configure.report()
    np.testing.assert_allclose(rotation, EXPECTED_Z_QUARTER, rtol=0, atol=1e-12)
    for key in ("default_form", "default_parser", "standard_units", "provenance"):
        assert after[key] == before[key]


def test_readonly_noncontiguous_axis_and_angle_are_preserved_and_result_is_independent():
    storage = np.array([2.0, 99.0, -3.0, 99.0, 1.0, 99.0])
    axis = storage[::2]
    axis.setflags(write=False)
    magnitude = np.array(37.0)
    magnitude.setflags(write=False)
    angle = puw.quantity(magnitude, "degrees")
    before_axis = storage.copy()
    before_angle = np.asarray(puw.get_value(angle)).copy()
    before_unit = puw.get_unit(angle)

    first = msm.structure.get_rotation_matrix_from_axis_angle(axis, angle)
    second = msm.structure.get_rotation_matrix_from_axis_angle(axis, angle)

    assert first.shape == (3, 3)
    assert first.dtype == np.float64
    assert not puw.is_quantity(first)
    assert not np.shares_memory(first, storage)
    assert not np.shares_memory(first, second)
    first[:] = 0
    np.testing.assert_allclose(second @ second.T, np.eye(3), rtol=0, atol=1e-12)
    np.testing.assert_array_equal(storage, before_axis)
    np.testing.assert_array_equal(puw.get_value(angle), before_angle)
    assert puw.get_unit(angle) == before_unit


@pytest.mark.parametrize(
    "axis",
    [
        None,
        [],
        [0, 0, 0],
        [0, 0],
        [[0, 0, 1]],
        [[0], [0], [1]],
        [[0, 0, 1], [1, 0, 0]],
        [np.nan, 0, 1],
        [np.inf, 0, 1],
        [0, 0, 1 + 0j],
        [False, False, True],
        [True, 0, 0],
        ["0", "0", "1"],
        np.array([0.0, 0.0, 1.0], dtype=object),
        "0 0 1",
        {0: 0, 1: 0, 2: 1},
        {0, 1, 2},
    ],
)
def test_undefined_or_malformed_axes_reject_even_with_zero_angle(axis):
    with pytest.raises(ArgumentError) as error:
        msm.structure.get_rotation_matrix_from_axis_angle(axis, "0 degrees")
    assert "axis" in str(error.value)


@pytest.mark.parametrize("nested", [False, True])
def test_unit_bearing_axes_do_not_lose_units_during_normalization(nested):
    axis = (
        [
            puw.quantity(0, "radians"),
            puw.quantity(0, "radians"),
            puw.quantity(1, "radians"),
        ]
        if nested
        else puw.quantity([0, 0, 1], "nm")
    )
    with pytest.raises(ArgumentError):
        msm.structure.get_rotation_matrix_from_axis_angle(axis, "90 degrees")


@pytest.mark.parametrize(
    "angle",
    [
        None,
        0,
        90.0,
        True,
        "1",
        "1 dimensionless",
        "100 percent",
        "1 nm",
        "not an angle",
    ],
)
def test_bare_and_nonangular_values_are_not_interpreted_as_angles(angle):
    with pytest.raises(ArgumentError) as error:
        msm.structure.get_rotation_matrix_from_axis_angle([0, 0, 1], angle)
    assert "angle" in str(error.value)
    assert error.value.__cause__ is not None


@pytest.mark.parametrize(
    "value", [[90], [[90]], [90, 45], np.nan, np.inf, -np.inf, 90 + 0j, True]
)
def test_angle_magnitude_must_be_one_finite_real_scalar(value):
    angle = puw.quantity(np.asarray(value), "degrees")
    with pytest.raises(ArgumentError):
        msm.structure.get_rotation_matrix_from_axis_angle([0, 0, 1], angle)


def test_generic_dimensionless_quantity_and_unit_without_magnitude_reject():
    for angle in (puw.quantity(1.0, "dimensionless"), puw.unit("degree")):
        with pytest.raises(ArgumentError):
            msm.structure.get_rotation_matrix_from_axis_angle([0, 0, 1], angle)


def test_trusted_delegation_uses_once_normalized_axis_and_radians():
    axis = digest_axis([0, 0, 1e-300], caller=CONSTRUCTOR_CALLER)
    angle = digest_angle("90 degrees", caller=CONSTRUCTOR_CALLER)
    assert axis.dtype == np.float64
    assert isinstance(angle, float)
    assert angle == np.pi / 2
    np.testing.assert_allclose(
        msm.structure.get_rotation_matrix_from_axis_angle(
            axis, angle, skip_digestion=True
        ),
        EXPECTED_Z_QUARTER,
        rtol=0,
        atol=1e-12,
    )
    with pytest.raises(ArgumentError):
        msm.structure.get_rotation_matrix_from_axis_angle(
            [0, 0, 1], "90 degrees", skip_digestion=1
        )


@pytest.mark.parametrize(
    "caller",
    [None, "molsysmt.lib.math.rodrigues_rotation", "molsysmt.structure.rotate.rotate"],
)
def test_shared_argument_names_do_not_impose_constructor_policy_on_other_callers(
    caller,
):
    with pytest.raises(ArgumentError):
        digest_axis([0, 0, 1], caller=caller)
    with pytest.raises(ArgumentError):
        digest_angle("90 degrees", caller=caller)
