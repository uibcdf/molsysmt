import numpy as np
import pytest

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.argdigest.argument.coordinates import digest_coordinates
from molsysmt._private.argdigest.argument.center_coordinates import digest_center_coordinates
from molsysmt._private.argdigest.argument.coordinates_minimum import digest_coordinates_minimum
from molsysmt._private.argdigest.argument.time import digest_time
from molsysmt._private.argdigest.argument.structure_id import digest_structure_id
from molsysmt._private.argdigest.argument.box_volume import digest_box_volume
from molsysmt._private.argdigest.argument.box_shape import digest_box_shape
from molsysmt._private.argdigest.argument.b_factor import digest_b_factor
from molsysmt._private.argdigest.argument.occupancy import digest_occupancy
from molsysmt._private.argdigest.argument.velocities import digest_velocities
from molsysmt._private.argdigest.argument.n_structures import digest_n_structures


def test_coordinate_family_digesters_accept_valid_shapes():
    coords_1 = puw.quantity(np.array([0.0, 0.0, 0.0]), 'nm')
    coords_2 = puw.quantity(np.array([[0.0, 0.0, 0.0], [0.1, 0.2, 0.3]]), 'nm')
    coords_3 = puw.quantity(np.array([[[0.0, 0.0, 0.0], [0.1, 0.2, 0.3]]]), 'nm')
    assert puw.get_value(digest_coordinates(coords_1)).shape == (1, 1, 3)
    assert puw.get_value(digest_coordinates(coords_2)).shape == (1, 2, 3)
    assert puw.get_value(digest_coordinates(coords_3)).shape == (1, 2, 3)
    assert puw.get_value(digest_center_coordinates(coords_3)).shape == (1, 2, 3)
    assert puw.get_value(digest_coordinates_minimum(coords_1)).shape == (1, 3)
    assert puw.get_value(digest_coordinates_minimum(coords_2)).shape == (2, 3)
    with pytest.raises(ArgumentError):
        digest_coordinates(puw.quantity(np.array([1.0, 2.0]), 'nm'))


def test_time_structure_id_and_box_flags_are_digested():
    time = puw.quantity(np.array([1.0, 2.0]), 'ps')
    digested = digest_time(time)
    np.testing.assert_allclose(puw.get_value(digested), [1.0, 2.0])
    assert digest_time(True, caller='molsysmt.basic.get.get') is True
    with pytest.raises(ArgumentError):
        digest_time(3)

    np.testing.assert_array_equal(digest_structure_id(4), np.array([4]))
    np.testing.assert_array_equal(digest_structure_id([4, 5]), np.array([4, 5]))
    assert digest_structure_id(None) is None

    assert digest_box_volume(True, caller='molsysmt.basic.get.get') is True
    assert digest_box_shape('Cubic') == 'cubic'
    with pytest.raises(ArgumentError):
        digest_box_shape('hexagonal')


def test_b_factor_occupancy_velocities_and_n_structures_digesters():
    b_factor = puw.quantity(np.array([1.0, 2.0]), 'angstrom**2')
    assert puw.get_value(digest_b_factor(b_factor)).shape == (1, 2)
    assert digest_b_factor(True, caller='molsysmt.basic.get.get') is True

    np.testing.assert_array_equal(digest_occupancy([0.5, 1.0]), np.array([[0.5, 1.0]]))
    assert digest_occupancy(True, caller='molsysmt.basic.get.get') is True

    vel = puw.quantity(np.array([[1.0, 0.0, 0.0]]), 'nm/ps')
    assert puw.get_value(digest_velocities(vel)).shape == (1, 1, 3)
    assert digest_velocities(True, caller='molsysmt.basic.get.get') is True

    assert digest_n_structures(True, caller='molsysmt.basic.get.get') is True
    assert digest_n_structures(5, caller='molsysmt.basic.contains.contains') == 5
    assert digest_n_structures(4, caller='molsysmt.pbc.get_box_with_shape') == 4
    with pytest.raises(ArgumentError):
        digest_n_structures(4)
