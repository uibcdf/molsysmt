# Tests for digestion functions
from molsysmt._private.exceptions import *
from molsysmt._private.digestion.box import digest_box_vectors_value
from molsysmt._private.digestion import *
from molsysmt import puw
from molsysmt.native import MolSys
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
    element_ = "ATOM"
    assert digest_element(element_) == "atom"

    element_ = "residues"
    assert digest_element(element_) == "group"


def test_digest_element_raises_error():

    element_ = "cow"
    with pytest.raises(WrongElementError):
        digest_element(element_)

    element_ = 20
    with pytest.raises(WrongElementError):
        digest_element(element_)

# Tests for digest engine #


def test_digest_engine_invalid_name_raises_error():
    engine_ = "cow"
    with pytest.raises(WrongEngineError):
        digest_engine(engine_)


def test_digest_engine_incorrect_type_raises_error():
    engine_ = [20, 10]
    with pytest.raises(WrongEngineError):
        digest_engine(engine_)


def test_digest_engine():
    engine_ = "openmm"
    assert digest_engine(engine_) == "OpenMM"


# Tests for digest form
def test_digest_form():

    form_ = "biopython.seq"
    assert digest_form(form_) == "biopython.Seq"

    forms = ["file:pdb", "openmm.system"]
    assert digest_form(forms) == ["file:pdb", "openmm.System"]


def test_digest_form_invalid_form_name():

    form_ = "cow"
    with pytest.raises(WrongFormError):
        digest_form(form_)


# Tests for digest indices


def test_digest_indices_all():
    indices_ = "ALL"
    assert digest_indices(indices_) == "all"


def test_digest_indices_single_number():
    indices_ = 5
    assert np.all(digest_indices(indices_) == np.array([5]))


def test_digest_indices_iterable():

    indices_ = [1, 2, 3]
    assert np.all(indices_ == np.array([1, 2, 3]))

    indices_ = (1, 2, 3)
    assert np.all(indices_ == np.array([1, 2, 3]))

    indices_ = np.array([1, 2, 3])
    assert np.all(indices_ == np.array([1, 2, 3]))


def test_indices_incorrect_value():

    indices_ = "everything"
    with pytest.raises(WrongIndicesError):
        digest_indices(indices_)

    indices_ = 5.5
    with pytest.raises(WrongIndicesError):
        digest_indices(indices_)

    indices_ = puw.quantity([2, 3], "meter")
    with pytest.raises(WrongIndicesError):
        digest_indices(indices_)

# Test for digest item


def test_digest_item():

    molecular_sys = MolSys()
    digest_item(molecular_sys, form="molsysmt.MolSys")


def test_digest_item_raises_error():

    item_ = [1, 2, 3]
    with pytest.raises(WrongFormError):
        digest_item(item_, form="list")


# Test for digest step

def test_digest_step_raise_error():

    with pytest.raises(WrongStepError):
        digest_step(20.0)

    with pytest.raises(WrongStepError):
        digest_step("10")


# Tests for digest syntaxis

def test_digest_syntaxis():

    syntax = "molsysmt"
    assert digest_syntaxis(syntax) == "MolSysMT"


# Tests for digest_viewer

def test_digest_viewer():

    viewer, viewer_form = digest_viewer("nglview")
    assert viewer == "NGLView"
    assert viewer_form == "nglview.NGLWidget"


def test_invalid_viewer_raises_error():

    with pytest.raises(BadCallError):
        digest_viewer("pymol")
