# Tests for digestion functions
from molsysmt._private.exceptions import IncorrectShapeError, WrongEngineError, WrongElementError
from molsysmt._private.exceptions import WrongFormError, WrongIndicesError
from molsysmt._private.digestion.box import digest_box_vectors, digest_box_vectors_value
from molsysmt._private.digestion import digest_element, digest_engine, digest_form
from molsysmt._private.digestion import digest_indices
from molsysmt import puw
import pytest
import numpy as np


# Tests for digest box #

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

    with pytest.raises(IncorrectShapeError):
        digest_box_vectors_value(lengths_list)

    with pytest.raises(IncorrectShapeError):
        digest_box_vectors_value(lengths_tuple)

    length_array_1 = np.array([1, 2, 3, 4])
    length_array_2 = np.array([[1],
                               [2],
                               [3], ])
    length_array_3 = np.array([[[1, 2, 3]]])

    with pytest.raises(IncorrectShapeError):
        digest_box_vectors_value(length_array_1)
    with pytest.raises(IncorrectShapeError):
        digest_box_vectors_value(length_array_2)
    with pytest.raises(IncorrectShapeError):
        digest_box_vectors_value(length_array_3)


def test_digest_box_vectors():

    lengths = puw.quantity([1, 2, 3], "meters")
    lengths_digested = digest_box_vectors(lengths)
    assert puw.get_value(lengths_digested).shape == (1, 3)
    assert np.all(puw.get_value(lengths_digested) == np.array([[1, 2, 3]]))
    assert puw.get_unit(lengths_digested) == "meter"

# Tests for digest element #


def test_digest_element():
    element = "ATOM"
    assert digest_element(element) == "atom"

    element = "residues"
    assert digest_element(element) == "group"


def test_digest_element_raises_error():

    element = "cow"
    with pytest.raises(WrongElementError):
        digest_element(element)

    element = 20
    with pytest.raises(WrongElementError):
        digest_element(element)

# Tests for digest engine #


def test_digest_engine_invalid_name_raises_error():
    engine = "cow"
    with pytest.raises(WrongEngineError):
        digest_engine(engine)


def test_digest_engine_incorrect_type_raises_error():
    engine = [20, 10]
    with pytest.raises(WrongEngineError):
        digest_engine(engine)


def test_digest_engine():
    engine = "openmm"
    assert digest_engine(engine) == "OpenMM"


# Tests for digest form
def test_digest_form():

    form = "biopython.seq"
    assert digest_form(form) == "biopython.Seq"

    forms = ["file:pdb", "openmm.system"]
    assert digest_form(forms) == ["file:pdb", "openmm.System"]


def test_digest_form_invalid_form_name():

    form = "cow"
    with pytest.raises(WrongFormError):
        digest_form(form)


# Tests for digest indices


def test_digest_indices_all():
    indices = "ALL"
    assert digest_indices(indices) == "all"


def test_digest_indices_single_number():
    indices = 5
    assert np.all(digest_indices(indices) == np.array([5]))


def test_digest_indices_iterable():

    indices = [1, 2, 3]
    assert np.all(indices == np.array([1, 2, 3]))

    indices = (1, 2, 3)
    assert np.all(indices == np.array([1, 2, 3]))

    indices = np.array([1, 2, 3])
    assert np.all(indices == np.array([1, 2, 3]))


def test_indices_incorrect_value():

    indices = "everything"
    with pytest.raises(WrongIndicesError):
        digest_indices(indices)

    indices = 5.5
    with pytest.raises(WrongIndicesError):
        digest_indices(indices)

    indices = puw.quantity([2, 3], "meter")
    with pytest.raises(WrongIndicesError):
        digest_indices(indices)

# Test for digest item


def test_digest_item():
    pass

