"""Tests for molsysmt._private.argdigest.argument.value.digest_value.

The dispatcher routes `msm.set()` calls to the appropriate sub-digester based
on the `caller` string that ends with `set_<attribute>_to_<element>`.

Coverage strategy
-----------------
Each test exercises one branch of the `if caller.endswith(...)` tree in
value.py by calling digest_value directly with a representative caller string
and a valid value.  The caller strings used here mirror what the real set
infrastructure passes down (e.g. `molsysmt.form.molsysmt_MolSys.set.set_atom_name_to_atom`).

All seven element levels are covered:
  atom, group, component, molecule, chain, entity, system
"""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest.argument.value import digest_value


# Prefix used for realistic caller strings (matches the branch condition logic
# but the dispatcher only cares about the suffix of the caller string).
_PREFIX = "molsysmt.form.molsysmt_MolSys.set."


# ===========================================================================
# Helpers
# ===========================================================================


def _caller(suffix: str) -> str:
    return _PREFIX + suffix


# ===========================================================================
# Atom-level branches
# ===========================================================================


class TestAtomBranches:
    """digest_value with callers ending in _to_atom."""

    def test_atom_name_str(self):
        result = digest_value(["N", "CA", "C"], caller=_caller("set_atom_name_to_atom"))
        assert result == ["N", "CA", "C"]

    def test_atom_name_single_str(self):
        result = digest_value("CA", caller=_caller("set_atom_name_to_atom"))
        assert result == "CA"

    def test_atom_id_list(self):
        result = digest_value([1, 2, 3], caller=_caller("set_atom_id_to_atom"))
        assert result == [1, 2, 3]

    def test_atom_id_int(self):
        result = digest_value(5, caller=_caller("set_atom_id_to_atom"))
        assert result == [5]

    def test_atom_type_list(self):
        result = digest_value(["C", "N", "O"], caller=_caller("set_atom_type_to_atom"))
        assert result == ["C", "N", "O"]

    def test_atom_type_str(self):
        result = digest_value("C", caller=_caller("set_atom_type_to_atom"))
        assert result == "C"

    def test_group_index_to_atom_list(self):
        result = digest_value([0, 0, 1], caller=_caller("set_group_index_to_atom"))
        assert result == [0, 0, 1]

    def test_group_index_to_atom_int(self):
        result = digest_value(0, caller=_caller("set_group_index_to_atom"))
        assert result == [0]

    def test_group_name_to_atom_list(self):
        result = digest_value(["ALA", "ALA", "HOH"], caller=_caller("set_group_name_to_atom"))
        assert result == ["ALA", "ALA", "HOH"]

    def test_group_id_to_atom_list(self):
        result = digest_value(["10", "10", "11"], caller=_caller("set_group_id_to_atom"))
        assert result == ["10", "10", "11"]

    def test_group_type_to_atom_list(self):
        result = digest_value(["amino acid", "amino acid", "water"], caller=_caller("set_group_type_to_atom"))
        assert result == ["amino acid", "amino acid", "water"]

    def test_component_index_to_atom_list(self):
        result = digest_value([0, 0, 1], caller=_caller("set_component_index_to_atom"))
        assert result == [0, 0, 1]

    def test_component_name_to_atom_list(self):
        result = digest_value(["prot", "prot", "wat"], caller=_caller("set_component_name_to_atom"))
        assert result == ["prot", "prot", "wat"]

    def test_component_id_to_atom_list(self):
        result = digest_value([0, 0, 1], caller=_caller("set_component_id_to_atom"))
        assert result == [0, 0, 1]

    def test_component_type_to_atom_list(self):
        result = digest_value(["protein", "protein", "water"], caller=_caller("set_component_type_to_atom"))
        assert result == ["protein", "protein", "water"]

    def test_molecule_index_to_atom_list(self):
        result = digest_value([0, 0, 1], caller=_caller("set_molecule_index_to_atom"))
        assert result == [0, 0, 1]

    def test_molecule_name_to_atom_list(self):
        result = digest_value(["hp35", "hp35", "water"], caller=_caller("set_molecule_name_to_atom"))
        assert result == ["hp35", "hp35", "water"]

    def test_molecule_id_to_atom_list(self):
        result = digest_value([0, 0, 1], caller=_caller("set_molecule_id_to_atom"))
        assert result == [0, 0, 1]

    def test_molecule_type_to_atom_list(self):
        result = digest_value(["protein", "protein", "water"], caller=_caller("set_molecule_type_to_atom"))
        assert result == ["protein", "protein", "water"]

    def test_chain_index_to_atom_list(self):
        result = digest_value([0, 0, 0], caller=_caller("set_chain_index_to_atom"))
        assert result == [0, 0, 0]

    def test_chain_name_to_atom_list(self):
        result = digest_value(["A", "A", "A"], caller=_caller("set_chain_name_to_atom"))
        assert result == ["A", "A", "A"]

    def test_chain_id_to_atom_list(self):
        result = digest_value(["A", "A", "A"], caller=_caller("set_chain_id_to_atom"))
        assert result == ["A", "A", "A"]

    def test_chain_type_to_atom_list(self):
        result = digest_value(["protein", "protein", "water"], caller=_caller("set_chain_type_to_atom"))
        assert result == ["protein", "protein", "water"]

    def test_entity_index_to_atom_list(self):
        result = digest_value([0, 0, 1], caller=_caller("set_entity_index_to_atom"))
        assert result == [0, 0, 1]

    def test_entity_name_to_atom_list(self):
        result = digest_value(["hp35", "hp35", "water"], caller=_caller("set_entity_name_to_atom"))
        assert result == ["hp35", "hp35", "water"]

    def test_entity_id_to_atom_list(self):
        result = digest_value([0, 0, 1], caller=_caller("set_entity_id_to_atom"))
        assert result == [0, 0, 1]

    def test_entity_type_to_atom_list(self):
        result = digest_value(["protein", "protein", "water"], caller=_caller("set_entity_type_to_atom"))
        assert result == ["protein", "protein", "water"]

    def test_coordinates_to_atom(self):
        coords = puw.quantity(np.zeros((1, 3, 3)), "nm")
        result = digest_value(coords, caller=_caller("set_coordinates_to_atom"))
        assert puw.is_quantity(result)


# ===========================================================================
# Group-level branches
# ===========================================================================


class TestGroupBranches:
    """digest_value with callers ending in _to_group."""

    def test_group_index_to_group_list(self):
        result = digest_value([0, 1], caller=_caller("set_group_index_to_group"))
        assert result == [0, 1]

    def test_group_name_to_group_list(self):
        result = digest_value(["ALA", "HOH"], caller=_caller("set_group_name_to_group"))
        assert result == ["ALA", "HOH"]

    def test_group_id_to_group_list(self):
        result = digest_value(["10", "11"], caller=_caller("set_group_id_to_group"))
        assert result == ["10", "11"]

    def test_group_type_to_group_list(self):
        result = digest_value(["amino acid", "water"], caller=_caller("set_group_type_to_group"))
        assert result == ["amino acid", "water"]

    def test_component_index_to_group_list(self):
        result = digest_value([0, 1], caller=_caller("set_component_index_to_group"))
        assert result == [0, 1]

    def test_component_name_to_group_list(self):
        result = digest_value(["prot", "wat"], caller=_caller("set_component_name_to_group"))
        assert result == ["prot", "wat"]

    def test_component_id_to_group_list(self):
        result = digest_value([0, 1], caller=_caller("set_component_id_to_group"))
        assert result == [0, 1]

    def test_component_type_to_group_list(self):
        result = digest_value(["protein", "water"], caller=_caller("set_component_type_to_group"))
        assert result == ["protein", "water"]

    def test_molecule_index_to_group_list(self):
        result = digest_value([0, 1], caller=_caller("set_molecule_index_to_group"))
        assert result == [0, 1]

    def test_molecule_name_to_group_list(self):
        result = digest_value(["hp35", "water"], caller=_caller("set_molecule_name_to_group"))
        assert result == ["hp35", "water"]

    def test_molecule_id_to_group_list(self):
        result = digest_value([0, 1], caller=_caller("set_molecule_id_to_group"))
        assert result == [0, 1]

    def test_molecule_type_to_group_list(self):
        result = digest_value(["protein", "water"], caller=_caller("set_molecule_type_to_group"))
        assert result == ["protein", "water"]

    def test_chain_index_to_group_list(self):
        result = digest_value([0, 0], caller=_caller("set_chain_index_to_group"))
        assert result == [0, 0]

    def test_chain_name_to_group_list(self):
        result = digest_value(["A", "A"], caller=_caller("set_chain_name_to_group"))
        assert result == ["A", "A"]

    def test_chain_id_to_group_list(self):
        result = digest_value(["A", "A"], caller=_caller("set_chain_id_to_group"))
        assert result == ["A", "A"]

    def test_chain_type_to_group_list(self):
        result = digest_value(["protein", "water"], caller=_caller("set_chain_type_to_group"))
        assert result == ["protein", "water"]

    def test_entity_index_to_group_list(self):
        result = digest_value([0, 1], caller=_caller("set_entity_index_to_group"))
        assert result == [0, 1]

    def test_entity_name_to_group_list(self):
        result = digest_value(["hp35", "water"], caller=_caller("set_entity_name_to_group"))
        assert result == ["hp35", "water"]

    def test_entity_id_to_group_list(self):
        result = digest_value([0, 1], caller=_caller("set_entity_id_to_group"))
        assert result == [0, 1]

    def test_entity_type_to_group_list(self):
        result = digest_value(["protein", "water"], caller=_caller("set_entity_type_to_group"))
        assert result == ["protein", "water"]


# ===========================================================================
# Component-level branches
# ===========================================================================


class TestComponentBranches:
    """digest_value with callers ending in _to_component."""

    def test_component_index_to_component_list(self):
        result = digest_value([0, 1], caller=_caller("set_component_index_to_component"))
        assert result == [0, 1]

    def test_component_name_to_component_list(self):
        result = digest_value(["prot", "wat"], caller=_caller("set_component_name_to_component"))
        assert result == ["prot", "wat"]

    def test_component_id_to_component_list(self):
        result = digest_value([0, 1], caller=_caller("set_component_id_to_component"))
        assert result == [0, 1]

    def test_component_type_to_component_list(self):
        result = digest_value(["protein", "water"], caller=_caller("set_component_type_to_component"))
        assert result == ["protein", "water"]

    def test_molecule_index_to_component_list(self):
        result = digest_value([0, 1], caller=_caller("set_molecule_index_to_component"))
        assert result == [0, 1]

    def test_molecule_name_to_component_list(self):
        result = digest_value(["hp35", "water"], caller=_caller("set_molecule_name_to_component"))
        assert result == ["hp35", "water"]

    def test_molecule_id_to_component_list(self):
        result = digest_value([0, 1], caller=_caller("set_molecule_id_to_component"))
        assert result == [0, 1]

    def test_molecule_type_to_component_list(self):
        result = digest_value(["protein", "water"], caller=_caller("set_molecule_type_to_component"))
        assert result == ["protein", "water"]

    def test_chain_index_to_component_list(self):
        result = digest_value([0, 0], caller=_caller("set_chain_index_to_component"))
        assert result == [0, 0]

    def test_chain_name_to_component_list(self):
        result = digest_value(["A", "A"], caller=_caller("set_chain_name_to_component"))
        assert result == ["A", "A"]

    def test_chain_id_to_component_list(self):
        result = digest_value(["A", "A"], caller=_caller("set_chain_id_to_component"))
        assert result == ["A", "A"]

    def test_chain_type_to_component_list(self):
        result = digest_value(["protein", "water"], caller=_caller("set_chain_type_to_component"))
        assert result == ["protein", "water"]

    def test_entity_index_to_component_list(self):
        result = digest_value([0, 1], caller=_caller("set_entity_index_to_component"))
        assert result == [0, 1]

    def test_entity_name_to_component_list(self):
        result = digest_value(["hp35", "water"], caller=_caller("set_entity_name_to_component"))
        assert result == ["hp35", "water"]

    def test_entity_id_to_component_list(self):
        result = digest_value([0, 1], caller=_caller("set_entity_id_to_component"))
        assert result == [0, 1]

    def test_entity_type_to_component_list(self):
        result = digest_value(["protein", "water"], caller=_caller("set_entity_type_to_component"))
        assert result == ["protein", "water"]


# ===========================================================================
# Molecule-level branches
# ===========================================================================


class TestMoleculeBranches:
    """digest_value with callers ending in _to_molecule."""

    def test_molecule_index_to_molecule_list(self):
        result = digest_value([0, 1], caller=_caller("set_molecule_index_to_molecule"))
        assert result == [0, 1]

    def test_molecule_name_to_molecule_list(self):
        result = digest_value(["hp35", "water"], caller=_caller("set_molecule_name_to_molecule"))
        assert result == ["hp35", "water"]

    def test_molecule_id_to_molecule_list(self):
        result = digest_value([0, 1], caller=_caller("set_molecule_id_to_molecule"))
        assert result == [0, 1]

    def test_molecule_type_to_molecule_list(self):
        result = digest_value(["protein", "water"], caller=_caller("set_molecule_type_to_molecule"))
        assert result == ["protein", "water"]

    def test_chain_index_to_molecule_list(self):
        result = digest_value([0, 0], caller=_caller("set_chain_index_to_molecule"))
        assert result == [0, 0]

    def test_chain_name_to_molecule_list(self):
        result = digest_value(["A", "A"], caller=_caller("set_chain_name_to_molecule"))
        assert result == ["A", "A"]

    def test_chain_id_to_molecule_list(self):
        result = digest_value(["A", "A"], caller=_caller("set_chain_id_to_molecule"))
        assert result == ["A", "A"]

    def test_chain_type_to_molecule_list(self):
        result = digest_value(["protein", "water"], caller=_caller("set_chain_type_to_molecule"))
        assert result == ["protein", "water"]

    def test_entity_index_to_molecule_list(self):
        result = digest_value([0, 1], caller=_caller("set_entity_index_to_molecule"))
        assert result == [0, 1]

    def test_entity_name_to_molecule_list(self):
        result = digest_value(["hp35", "water"], caller=_caller("set_entity_name_to_molecule"))
        assert result == ["hp35", "water"]

    def test_entity_id_to_molecule_list(self):
        result = digest_value([0, 1], caller=_caller("set_entity_id_to_molecule"))
        assert result == [0, 1]

    def test_entity_type_to_molecule_list(self):
        result = digest_value(["protein", "water"], caller=_caller("set_entity_type_to_molecule"))
        assert result == ["protein", "water"]


# ===========================================================================
# Chain-level branches
# ===========================================================================


class TestChainBranches:
    """digest_value with callers ending in _to_chain."""

    def test_chain_index_to_chain_list(self):
        result = digest_value([0, 1], caller=_caller("set_chain_index_to_chain"))
        assert result == [0, 1]

    def test_chain_name_to_chain_list(self):
        result = digest_value(["A", "B"], caller=_caller("set_chain_name_to_chain"))
        assert result == ["A", "B"]

    def test_chain_id_to_chain_list(self):
        result = digest_value(["A", "B"], caller=_caller("set_chain_id_to_chain"))
        assert result == ["A", "B"]

    def test_chain_type_to_chain_list(self):
        result = digest_value(["protein", "water"], caller=_caller("set_chain_type_to_chain"))
        assert result == ["protein", "water"]

    def test_entity_index_to_chain_list(self):
        result = digest_value([0, 1], caller=_caller("set_entity_index_to_chain"))
        assert result == [0, 1]

    def test_entity_name_to_chain_list(self):
        result = digest_value(["hp35", "water"], caller=_caller("set_entity_name_to_chain"))
        assert result == ["hp35", "water"]

    def test_entity_id_to_chain_list(self):
        result = digest_value([0, 1], caller=_caller("set_entity_id_to_chain"))
        assert result == [0, 1]

    def test_entity_type_to_chain_list(self):
        result = digest_value(["protein", "water"], caller=_caller("set_entity_type_to_chain"))
        assert result == ["protein", "water"]


# ===========================================================================
# Entity-level branches
# ===========================================================================


class TestEntityBranches:
    """digest_value with callers ending in _to_entity."""

    def test_entity_index_to_entity_list(self):
        result = digest_value([0, 1], caller=_caller("set_entity_index_to_entity"))
        assert result == [0, 1]

    def test_entity_name_to_entity_list(self):
        result = digest_value(["hp35", "water"], caller=_caller("set_entity_name_to_entity"))
        assert result == ["hp35", "water"]

    def test_entity_name_to_entity_str(self):
        result = digest_value("hp35", caller=_caller("set_entity_name_to_entity"))
        assert result == "hp35"

    def test_entity_id_to_entity_list(self):
        result = digest_value([0, 1], caller=_caller("set_entity_id_to_entity"))
        assert result == [0, 1]

    def test_entity_type_to_entity_list(self):
        result = digest_value(["protein", "water"], caller=_caller("set_entity_type_to_entity"))
        assert result == ["protein", "water"]


# ===========================================================================
# System-level branches
# ===========================================================================


class TestSystemBranches:
    """digest_value with callers ending in _to_system."""

    def test_structure_id_to_system_list(self):
        result = digest_value([0, 1, 2], caller=_caller("set_structure_id_to_system"))
        np.testing.assert_array_equal(result, np.array([0, 1, 2]))

    def test_structure_id_to_system_int(self):
        result = digest_value(0, caller=_caller("set_structure_id_to_system"))
        np.testing.assert_array_equal(result, np.array([0]))

    def test_time_to_system(self):
        t = puw.quantity(np.array([0.0, 1.0, 2.0]), "ps")
        result = digest_value(t, caller=_caller("set_time_to_system"))
        assert puw.is_quantity(result)

    def test_box_to_system(self):
        box = puw.quantity(np.eye(3)[np.newaxis, :, :], "nm")
        result = digest_value(box, caller=_caller("set_box_to_system"))
        assert puw.is_quantity(result)

    def test_coordinates_to_system(self):
        coords = puw.quantity(np.zeros((2, 5, 3)), "nm")
        result = digest_value(coords, caller=_caller("set_coordinates_to_system"))
        assert puw.is_quantity(result)


# ===========================================================================
# numpy array inputs (type-conversion paths)
# ===========================================================================


class TestNumpyArrayInputs:
    """Verify that numpy array inputs are correctly converted to lists."""

    def test_atom_name_ndarray(self):
        arr = np.array(["N", "CA", "C"])
        result = digest_value(arr, caller=_caller("set_atom_name_to_atom"))
        assert result == ["N", "CA", "C"]

    def test_group_name_ndarray(self):
        arr = np.array(["ALA", "HOH"])
        result = digest_value(arr, caller=_caller("set_group_name_to_group"))
        assert result == ["ALA", "HOH"]

    def test_chain_name_ndarray(self):
        arr = np.array(["A", "B"])
        result = digest_value(arr, caller=_caller("set_chain_name_to_chain"))
        assert result == ["A", "B"]

    def test_molecule_name_ndarray(self):
        arr = np.array(["hp35", "water"])
        result = digest_value(arr, caller=_caller("set_molecule_name_to_molecule"))
        assert result == ["hp35", "water"]

    def test_entity_name_ndarray(self):
        arr = np.array(["hp35", "water"])
        result = digest_value(arr, caller=_caller("set_entity_name_to_entity"))
        assert result == ["hp35", "water"]

    def test_group_index_ndarray(self):
        arr = np.array([0, 0, 1])
        result = digest_value(arr, caller=_caller("set_group_index_to_atom"))
        assert result == [0, 0, 1]

    def test_chain_index_ndarray(self):
        arr = np.array([0, 0])
        result = digest_value(arr, caller=_caller("set_chain_index_to_group"))
        assert result == [0, 0]

    def test_molecule_index_ndarray(self):
        arr = np.array([0, 1])
        result = digest_value(arr, caller=_caller("set_molecule_index_to_molecule"))
        assert result == [0, 1]

    def test_entity_index_ndarray(self):
        arr = np.array([0, 1])
        result = digest_value(arr, caller=_caller("set_entity_index_to_entity"))
        assert result == [0, 1]
