import numpy as np
import pytest

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.argdigest.argument.center import digest_center
from molsysmt._private.argdigest.argument.center_at_origin import digest_center_at_origin
from molsysmt._private.argdigest.argument.center_coordinates import digest_center_coordinates
from molsysmt._private.argdigest.argument.center_of_atoms import digest_center_of_atoms
from molsysmt._private.argdigest.argument.center_of_atoms_2 import digest_center_of_atoms_2
from molsysmt._private.argdigest.argument.center_of_selection import digest_center_of_selection


def test_center_accepts_convert_semantics_and_alignment_bool():
    caller = 'molsysmt.basic.convert.convert'
    np.testing.assert_array_equal(digest_center(3, caller=caller), np.array([3], dtype='int64'))
    np.testing.assert_array_equal(digest_center([0, 2], caller=caller), np.array([0, 2], dtype='int64'))
    assert digest_center('index < 3', caller=caller) == 'index < 3'
    assert digest_center(None, caller=caller) is None
    assert digest_center(True, caller='molsysmt.structure.align_principal_axes.align_principal_axes') is True
    with pytest.raises(ArgumentError):
        digest_center('index < 3')


def test_center_coordinate_and_selection_digesters_accept_valid_values():
    coords = puw.quantity(np.array([[[0.0, 0.0, 0.0]]], dtype=np.float64), 'nm')
    standardized = digest_center_coordinates(coords)
    np.testing.assert_allclose(puw.get_value(standardized), puw.get_value(coords))
    assert puw.get_unit(standardized) == puw.get_unit(coords)
    assert digest_center_coordinates(None) is None
    with pytest.raises(ArgumentError):
        digest_center_coordinates('bad')

    assert digest_center_of_atoms(True) is True
    assert digest_center_of_atoms_2(True) is True
    assert digest_center_of_atoms_2(None) is None
    with pytest.raises(ArgumentError):
        digest_center_of_atoms('bad')

    assert digest_center_of_selection('name == "CA"') == 'name == "CA"'
    assert digest_center_of_selection(4) == [4]


def test_center_at_origin_requires_boolean():
    assert digest_center_at_origin(False) is False
    with pytest.raises(ArgumentError):
        digest_center_at_origin('yes')
