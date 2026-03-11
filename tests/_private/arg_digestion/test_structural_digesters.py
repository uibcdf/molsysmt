import numpy as np
import pytest

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.arg_digestion.argument.b_factor import digest_b_factor
from molsysmt._private.arg_digestion.argument.center import digest_center
from molsysmt._private.arg_digestion.argument.coordinates import digest_coordinates
from molsysmt._private.arg_digestion.argument.coordinates_minimum import digest_coordinates_minimum
from molsysmt._private.arg_digestion.argument.occupancy import digest_occupancy
from molsysmt._private.arg_digestion.argument.structure_id import digest_structure_id
from molsysmt._private.arg_digestion.argument.time import digest_time

GET_CALLER = 'molsysmt.basic.get.get'
COMPARE_CALLER = 'molsysmt.basic.compare.compare'
CONVERT_CALLER = 'molsysmt.basic.convert.convert'
ALIGN_AXES_CALLER = 'molsysmt.structure.align_principal_axes.align_principal_axes'


def test_digest_coordinates_accepts_boolean_none_and_standardizes_shapes():
    assert digest_coordinates(True, caller=GET_CALLER) is True
    assert digest_coordinates(None) is None

    vector = puw.quantity(np.array([1.0, 2.0, 3.0]), 'angstrom')
    digested = digest_coordinates(vector)
    assert digested.shape == (1, 1, 3)
    np.testing.assert_allclose(puw.get_value(digested), np.array([[[0.1, 0.2, 0.3]]]))

    matrix = puw.quantity(np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]), 'angstrom')
    digested = digest_coordinates(matrix)
    assert digested.shape == (1, 2, 3)

    tensor = puw.quantity(np.ones((2, 3, 3)), 'nanometer')
    digested = digest_coordinates(tensor)
    assert digested.shape == (2, 3, 3)

    with pytest.raises(ArgumentError):
        digest_coordinates(puw.quantity(np.ones((2, 2)), 'nanometer'))


def test_digest_b_factor_accepts_boolean_none_and_1d_2d_quantities():
    assert digest_b_factor(False, caller=COMPARE_CALLER) is False
    assert digest_b_factor(None) is None

    one_d = puw.quantity(np.array([1.0, 2.0]), 'angstrom**2')
    digested = digest_b_factor(one_d)
    assert digested.shape == (1, 2)

    two_d = puw.quantity(np.ones((2, 3)), 'angstrom**2')
    digested = digest_b_factor(two_d)
    assert digested.shape == (2, 3)

    with pytest.raises(ArgumentError):
        digest_b_factor(puw.quantity(np.array([1.0, 2.0]), 'picosecond'))


def test_digest_occupancy_accepts_boolean_none_and_arrays():
    assert digest_occupancy(True, caller=GET_CALLER) is True
    assert digest_occupancy(None) is None

    one_d = digest_occupancy([0.5, 1.0])
    assert one_d.shape == (1, 2)

    two_d = digest_occupancy(np.ones((2, 3)))
    assert two_d.shape == (2, 3)

    with pytest.raises(ArgumentError):
        digest_occupancy('1.0')


def test_digest_time_accepts_boolean_none_strings_and_quantity_sequences():
    assert digest_time(True, caller=GET_CALLER) is True
    assert digest_time(None) is None

    parsed = digest_time('1.0 ps')
    np.testing.assert_allclose(puw.get_value(parsed), np.array(1.0))

    seq = [puw.quantity(1.0, 'ps'), puw.quantity(2.0, 'ps')]
    digested = digest_time(seq)
    np.testing.assert_allclose(puw.get_value(digested), np.array([1.0, 2.0]))

    with pytest.raises(ArgumentError):
        digest_time([1.0, 2.0])


def test_digest_structure_id_and_coordinates_minimum_normalize_inputs():
    assert digest_structure_id(None) is None
    np.testing.assert_array_equal(digest_structure_id(4), np.array([4]))
    np.testing.assert_array_equal(digest_structure_id([1, 2]), np.array([1, 2]))

    vec = puw.quantity(np.array([1.0, 2.0, 3.0]), 'angstrom')
    digested = digest_coordinates_minimum(vec)
    assert digested.shape == (1, 3)
    np.testing.assert_allclose(puw.get_value(digested), np.array([[0.1, 0.2, 0.3]]))

    mat = puw.quantity(np.ones((2, 3)), 'nanometer')
    assert digest_coordinates_minimum(mat).shape == (2, 3)

    with pytest.raises(ArgumentError):
        digest_coordinates_minimum(puw.quantity(np.ones((2, 2)), 'nanometer'))


def test_digest_center_supports_convert_and_align_principal_axes_contracts():
    assert digest_center(True, caller=ALIGN_AXES_CALLER) is True
    assert digest_center(None, caller=CONVERT_CALLER) is None
    assert digest_center('chain_name=="A"', caller=CONVERT_CALLER) == 'chain_name=="A"'
    np.testing.assert_array_equal(digest_center(3, caller=CONVERT_CALLER), np.array([3], dtype='int64'))
    np.testing.assert_array_equal(digest_center([1, 2], caller=CONVERT_CALLER), np.array([1, 2], dtype='int64'))

    with pytest.raises(ArgumentError):
        digest_center('A', caller='molsysmt.other.caller')
