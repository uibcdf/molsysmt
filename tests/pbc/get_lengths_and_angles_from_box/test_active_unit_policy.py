"""Compare public box geometry to analytical truth under nondefault units."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.mark.parametrize(
    "length_unit, angle_unit", [("pm", "degrees"), ("nm", "radians")]
)
def test_box_geometry_follows_active_length_and_angle_policy(length_unit, angle_unit):
    box = puw.quantity(
        np.array([[[2.0, 0.0, 0.0], [0.0, 3.0, 0.0], [1.0, 0.0, np.sqrt(3.0)]]]),
        "angstrom",
    )
    original_units = puw.configure.get_standard_units()
    with puw.context(standard_units=[length_unit, "fs", angle_unit]):
        lengths, angles = msm.pbc.get_lengths_and_angles_from_box(box)
        assert lengths.shape == angles.shape == (1, 3)
        assert puw.get_unit(lengths) == puw.unit(length_unit)
        assert puw.get_unit(angles) == puw.unit(angle_unit)
        np.testing.assert_allclose(
            puw.get_value(lengths, to_unit="angstrom"), [[2.0, 3.0, 2.0]], atol=1e-6
        )
        np.testing.assert_allclose(
            puw.get_value(angles, to_unit="radians"),
            [[np.pi / 2, np.pi / 3, np.pi / 2]],
            atol=1e-6,
        )
    assert puw.configure.get_standard_units() == original_units
