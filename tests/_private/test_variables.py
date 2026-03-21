"""
Tests for molsysmt._private.variables module (75% coverage → improve).
"""

import numpy as np
import pytest


# ---------------------------------------------------------------------------
# is_all
# ---------------------------------------------------------------------------

def test_is_all_all():
    from molsysmt._private.variables import is_all
    assert is_all('all') is True
    assert is_all('All') is True
    assert is_all('ALL') is True


def test_is_all_false_cases():
    from molsysmt._private.variables import is_all
    assert is_all([0, 1]) is False
    assert is_all(None) is False
    assert is_all(0) is False


# ---------------------------------------------------------------------------
# is_iterable
# ---------------------------------------------------------------------------

def test_is_iterable_list():
    from molsysmt._private.variables import is_iterable
    assert is_iterable([1, 2, 3]) is True


def test_is_iterable_tuple():
    from molsysmt._private.variables import is_iterable
    assert is_iterable((1, 2)) is True


def test_is_iterable_ndarray():
    from molsysmt._private.variables import is_iterable
    assert is_iterable(np.array([1, 2])) is True


def test_is_iterable_string_false():
    from molsysmt._private.variables import is_iterable
    assert is_iterable('hello') is False


# ---------------------------------------------------------------------------
# is_iterable_of_iterables
# ---------------------------------------------------------------------------

def test_is_iterable_of_iterables_list_of_lists():
    from molsysmt._private.variables import is_iterable_of_iterables
    assert is_iterable_of_iterables([[1, 2], [3, 4]]) is True


def test_is_iterable_of_iterables_flat_list():
    from molsysmt._private.variables import is_iterable_of_iterables
    assert is_iterable_of_iterables([1, 2, 3]) is False


def test_is_iterable_of_iterables_not_iterable():
    from molsysmt._private.variables import is_iterable_of_iterables
    assert is_iterable_of_iterables('hello') is False


# ---------------------------------------------------------------------------
# is_iterable_of_iterables_of_iterables
# ---------------------------------------------------------------------------

def test_is_iterable_of_iterables_of_iterables_3level():
    from molsysmt._private.variables import is_iterable_of_iterables_of_iterables
    assert is_iterable_of_iterables_of_iterables([[[1, 2], [3]], [[4]]]) is True


def test_is_iterable_of_iterables_of_iterables_2level():
    from molsysmt._private.variables import is_iterable_of_iterables_of_iterables
    assert is_iterable_of_iterables_of_iterables([[1, 2], [3, 4]]) is False


def test_is_iterable_of_iterables_of_iterables_not_iterable():
    from molsysmt._private.variables import is_iterable_of_iterables_of_iterables
    assert is_iterable_of_iterables_of_iterables(42) is False


# ---------------------------------------------------------------------------
# is_next
# ---------------------------------------------------------------------------

def test_is_next_true():
    from molsysmt._private.variables import is_next
    assert is_next('next') is True
    assert is_next('Next') is True
    assert is_next('NEXT') is True


def test_is_next_false():
    from molsysmt._private.variables import is_next
    assert is_next('all') is False
    assert is_next([]) is False


# ---------------------------------------------------------------------------
# is_iterable_of_pairs
# ---------------------------------------------------------------------------

def test_is_iterable_of_pairs_ndarray():
    from molsysmt._private.variables import is_iterable_of_pairs
    arr = np.array([[0, 1], [2, 3]])
    assert is_iterable_of_pairs(arr) is True


def test_is_iterable_of_pairs_ndarray_wrong_shape():
    from molsysmt._private.variables import is_iterable_of_pairs
    arr = np.array([[0, 1, 2]])
    assert is_iterable_of_pairs(arr) is False


def test_is_iterable_of_pairs_list_of_pairs():
    from molsysmt._private.variables import is_iterable_of_pairs
    assert is_iterable_of_pairs([(0, 1), (2, 3)]) is True


def test_is_iterable_of_pairs_list_not_pairs():
    from molsysmt._private.variables import is_iterable_of_pairs
    assert is_iterable_of_pairs([(0, 1, 2)]) is False


def test_is_iterable_of_pairs_not_iterable():
    from molsysmt._private.variables import is_iterable_of_pairs
    assert is_iterable_of_pairs(42) is False


# ---------------------------------------------------------------------------
# is_iterable_of_integers
# ---------------------------------------------------------------------------

def test_is_iterable_of_integers_ndarray():
    from molsysmt._private.variables import is_iterable_of_integers
    assert is_iterable_of_integers(np.array([0, 1, 2], dtype=int)) is True


def test_is_iterable_of_integers_ndarray_float():
    from molsysmt._private.variables import is_iterable_of_integers
    assert is_iterable_of_integers(np.array([0.0, 1.0])) is False


def test_is_iterable_of_integers_list():
    from molsysmt._private.variables import is_iterable_of_integers
    assert is_iterable_of_integers([0, 1, 2]) is True


def test_is_iterable_of_integers_list_with_float():
    from molsysmt._private.variables import is_iterable_of_integers
    assert is_iterable_of_integers([0, 1.5]) is False


def test_is_iterable_of_integers_not_iterable():
    from molsysmt._private.variables import is_iterable_of_integers
    assert is_iterable_of_integers(42) is False
