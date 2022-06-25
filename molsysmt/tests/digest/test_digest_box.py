# Tests for digestion functions
from molsysmt._private.digestion.box import digest_box_vectors, digest_box_vectors_value
from molsysmt import puw
import pytest
import numpy as np


def test_digest_box_vectors_value_with_list_and_tuple():
    lengths_list = [1, 2, 3]
    lengths_expected = np.array([[1, 2, 3]])
    lengths_digested = digest_box_vectors_value(lengths_list)
    assert np.all(lengths_digested == lengths_expected)

    lengths_tuple = (1, 2, 3)
    lengths_digested = digest_box_vectors_value(lengths_tuple)
    assert np.all(lengths_digested == lengths_expected)


def test_digest_box_vectors_value_with_array():
    length_array_1 = np.array([1, 2, 3])
    lengths_expected = np.array([[1, 2, 3]])
    lengths_digested = digest_box_vectors_value(length_array_1)
    assert lengths_digested.shape == (1, 3)
    assert np.all(lengths_digested == lengths_expected)

    length_array_2 = np.array([[1, 2, 3],
                               [4, 5, 6]])
    lengths_digested = digest_box_vectors_value(length_array_2)
    assert lengths_digested.shape == (2, 3)
    assert np.all(lengths_digested == length_array_2)


def test_digest_box_vectors_value_incorrect_shape_raises_error():
    lengths_list = [1, 2, 3, 4]
    lengths_tuple = (1, 2, 3, 4)

    with pytest.raises(ValueError):
        digest_box_vectors_value(lengths_list)

    with pytest.raises(ValueError):
        digest_box_vectors_value(lengths_tuple)

    length_array_1 = np.array([1, 2, 3, 4])
    length_array_2 = np.array([[1],
                               [2],
                               [3], ])
    length_array_3 = np.array([[[1, 2, 3]]])

    with pytest.raises(ValueError):
        digest_box_vectors_value(length_array_1)
    with pytest.raises(ValueError):
        digest_box_vectors_value(length_array_2)
    with pytest.raises(ValueError):
        digest_box_vectors_value(length_array_3)


def test_digest_box_vectors():

    lengths = puw.quantity([1, 2, 3], "meters")
    lengths_digested = digest_box_vectors(lengths)
    assert puw.get_value(lengths_digested).shape == (1, 3)
    assert np.all(puw.get_value(lengths_digested) == np.array([[1, 2, 3]]))
    assert puw.get_unit(lengths_digested) == "meter"
