"""
Tests for molsysmt.basic.is_a_molecular_system covering all branches.
"""
import molsysmt as msm
from molsysmt.basic.is_a_molecular_system import is_a_molecular_system
from molsysmt import systems
from molsysmt.native import MolSys, Topology, Structures
import pytest


def test_native_molsys_is_true(hp35_molsys):
    assert is_a_molecular_system(hp35_molsys) is True


def test_native_topology_is_true(hp35_molsys):
    top = msm.convert(hp35_molsys, to_form='molsysmt.Topology')
    assert is_a_molecular_system(top) is True


def test_native_structures_is_true(hp35_molsys):
    structs = msm.convert(hp35_molsys, to_form='molsysmt.Structures')
    assert is_a_molecular_system(structs) is True


def test_supported_string_is_true():
    assert is_a_molecular_system('AVLYAWPA') is True


def test_unsupported_string_is_false():
    assert is_a_molecular_system('some_string') is False


def test_invalid_object_is_false():
    assert is_a_molecular_system(12345) is False


def test_dict_valid_form_is_true(hp35_molsys):
    """A dict that encodes a valid MolSysDict returns True."""
    molsys_dict = msm.convert(hp35_molsys, to_form='molsysmt.MolSysDict')
    assert is_a_molecular_system(molsys_dict) is True


def test_dict_invalid_returns_false():
    """A plain dict that is not a valid form returns False."""
    assert is_a_molecular_system({'not': 'a_molsys'}) is False


def test_list_compatible_returns_true():
    """A list [topology, structures] with matching atoms returns True."""
    top_file = systems['pentalanine']['pentalanine.prmtop']
    crd_file = systems['pentalanine']['pentalanine.inpcrd']
    assert is_a_molecular_system([top_file, crd_file]) is True


def test_list_incompatible_returns_false():
    """A list with incompatible atom counts returns False."""
    top_file = systems['pentalanine']['pentalanine.prmtop']
    crd_file = systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.dcd']
    assert is_a_molecular_system([top_file, crd_file]) is False


def test_list_invalid_items_returns_false():
    """A list with non-molecular-system items returns False."""
    assert is_a_molecular_system([42, 'not_a_file.xyz']) is False
