import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.argdigest.argument.b_factor import digest_b_factor
from molsysmt._private.argdigest.argument.box import digest_box
from molsysmt._private.argdigest.argument.box_lengths import digest_box_lengths
from molsysmt._private.argdigest.argument.box_angles import digest_box_angles
from molsysmt._private.argdigest.argument.box_center import digest_box_center
from molsysmt._private.argdigest.argument.box_origin import digest_box_origin
from molsysmt._private.argdigest.argument.coordinates import digest_coordinates
from molsysmt._private.argdigest.argument.time import digest_time
from molsysmt._private.argdigest.argument.structure_id import digest_structure_id


GET_CALLER = "molsysmt.basic.get.get"


def test_b_factor_supports_boolean_none_and_valid_shapes():
    assert digest_b_factor(True, caller=GET_CALLER) is True
    assert digest_b_factor(None) is None

    quantity_1d = msm.pyunitwizard.quantity(np.array([1.0, 2.0]), "angstroms**2")
    digested_1d = digest_b_factor(quantity_1d)
    assert digested_1d.shape == (1, 2)

    quantity_2d = msm.pyunitwizard.quantity(np.array([[1.0, 2.0], [3.0, 4.0]]), "angstroms**2")
    digested_2d = digest_b_factor(quantity_2d)
    assert digested_2d.shape == (2, 2)

    with pytest.raises(ArgumentError):
        digest_b_factor(msm.pyunitwizard.quantity(np.array([1.0]), "nanometers"))


def test_box_digesters_normalize_valid_shapes_and_units():
    box = msm.pyunitwizard.quantity(np.eye(3), "nanometers")
    digested_box = digest_box(box)
    assert digested_box.shape == (1, 3, 3)

    box_lengths = digest_box_lengths(msm.pyunitwizard.quantity([1.0, 2.0, 3.0], "nanometers"))
    assert box_lengths.shape == (1, 3)

    box_angles = digest_box_angles(msm.pyunitwizard.quantity([90.0, 90.0, 120.0], "degrees"))
    assert box_angles.shape == (1, 3)

    box_center = digest_box_center(msm.pyunitwizard.quantity([0.0, 0.0, 0.0], "nanometers"))
    assert box_center.shape == (3,)

    box_origin = digest_box_origin(msm.pyunitwizard.quantity([[1.0, 2.0, 3.0]], "nanometers"))
    assert box_origin.shape == (3,)


def test_box_digesters_reject_invalid_inputs():
    with pytest.raises(ArgumentError):
        digest_box(msm.pyunitwizard.quantity(np.ones((2, 2)), "nanometers"))

    with pytest.raises(ArgumentError):
        digest_box_lengths(msm.pyunitwizard.quantity([1.0, 2.0], "nanometers"))

    with pytest.raises(ArgumentError):
        digest_box_angles(msm.pyunitwizard.quantity([90.0, 120.0], "degrees"))

    with pytest.raises(ArgumentError):
        digest_box_center(msm.pyunitwizard.quantity([0.0, 0.0], "nanometers"))

    with pytest.raises(ArgumentError):
        digest_box_origin(msm.pyunitwizard.quantity(np.ones((2, 2, 2)), "nanometers"))


def test_coordinates_digesters_normalize_supported_shapes():
    assert digest_coordinates(True, caller=GET_CALLER) is True
    assert digest_coordinates(None) is None

    c1 = digest_coordinates(msm.pyunitwizard.quantity([1.0, 2.0, 3.0], "nanometers"))
    assert c1.shape == (1, 1, 3)

    c2 = digest_coordinates(msm.pyunitwizard.quantity([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], "nanometers"))
    assert c2.shape == (1, 2, 3)

    c3 = digest_coordinates(
        msm.pyunitwizard.quantity(np.arange(12.0).reshape(2, 2, 3), "nanometers")
    )
    assert c3.shape == (2, 2, 3)

    with pytest.raises(ArgumentError):
        digest_coordinates(msm.pyunitwizard.quantity([1.0, 2.0], "nanometers"))


def test_time_and_structure_id_digesters_normalize_valid_values():
    assert digest_time(True, caller=GET_CALLER) is True
    assert digest_time(None) is None

    parsed = digest_time("1 ps")
    assert msm.pyunitwizard.get_value(parsed) == 1.0

    sequence = digest_time(
        [
            msm.pyunitwizard.quantity(1.0, "picoseconds"),
            msm.pyunitwizard.quantity(2.0, "picoseconds"),
        ]
    )
    assert msm.pyunitwizard.get_value(sequence).tolist() == [1.0, 2.0]

    assert digest_structure_id(None) is None
    assert digest_structure_id(3).tolist() == [3]
    assert digest_structure_id([1, 2]).tolist() == [1, 2]
    assert digest_structure_id(np.array([4, 5])).tolist() == [4, 5]

    with pytest.raises(ArgumentError):
        digest_time(msm.pyunitwizard.quantity(1.0, "nanometers"))

    with pytest.raises(ArgumentError):
        digest_structure_id("frame-1")
