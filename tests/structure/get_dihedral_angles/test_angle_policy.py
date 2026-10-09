"""Protect the public angular-unit contract with an analytical torsion."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.mark.parametrize(
    "angle_unit, expected", [("radians", np.pi / 4), ("degrees", 45.0)]
)
def test_dihedral_angles_follow_active_angle_policy(angle_unit, expected):
    coordinates = puw.quantity(
        np.array(
            [[[0.0, 1.0, 0.0], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 1.0]]]
        ),
        "angstrom",
    )
    original_policy = puw.configure.get_standard_units()
    with puw.context(standard_units=["pm", "fs", "radians"]):
        with puw.context(standard_units=["pm", "fs", angle_unit]):
            angles = msm.structure.get_dihedral_angles(
                coordinates,
                dihedral_quartets=np.array([[0, 1, 2, 3]]),
                pbc=False,
                use_gpu=False,
            )
            assert angles.shape == (1, 1)
            assert puw.get_unit(angles) == puw.unit(angle_unit)
            np.testing.assert_allclose(puw.get_value(angles), [[expected]], atol=1e-12)
            np.testing.assert_allclose(
                puw.get_value(angles, to_unit="radians"), [[np.pi / 4]], atol=1e-12
            )
        assert puw.get_unit(puw.standardize(puw.quantity(1.0, "radians"))) == puw.unit(
            "radians"
        )
    assert puw.configure.get_standard_units() == original_policy
