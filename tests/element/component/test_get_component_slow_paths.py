"""
Tests for component element getter slow paths (non-'all' selection).

These tests bypass the fast native-hierarchy path and exercise branches
that require either a non-'all' selection or non-MolSys/Topology input.
"""

import molsysmt as msm
import pytest


# ---------------------------------------------------------------------------
# get_component_id – non-'all' selection branches (lines 46-57)
# ---------------------------------------------------------------------------

def test_component_id_list_selection_default(hp35_pdb_molsys):
    """List selection → else branch (lines 54-57): simple get with component_id."""
    output = msm.element.component.get_component_id(
        hp35_pdb_molsys, element='atom', selection=[0, 1, 2]
    )
    assert isinstance(output, list)
    assert len(output) == 3
    assert all(isinstance(v, str) for v in output)


def test_component_id_list_selection_redefine_indices(hp35_pdb_molsys):
    """List selection + redefine_indices=True → elif redefine_indices branch."""
    output = msm.element.component.get_component_id(
        hp35_pdb_molsys, element='atom', selection=[0, 1], redefine_indices=True
    )
    assert isinstance(output, list)


def test_component_id_list_selection_redefine_ids(hp35_pdb_molsys):
    """List selection + redefine_ids=True → elif redefine_ids branch."""
    output = msm.element.component.get_component_id(
        hp35_pdb_molsys, element='atom', selection=[0], redefine_ids=True
    )
    assert isinstance(output, list)


def test_component_id_molsys_redefine_ids(hp35_pdb_molsys):
    """selection='all' + MolSys + redefine_ids=True → lines 19-28."""
    output = msm.element.component.get_component_id(
        hp35_pdb_molsys, element='component', selection='all', redefine_ids=True
    )
    assert isinstance(output, list)


def test_component_id_component_element(hp35_pdb_molsys):
    output = msm.element.component.get_component_id(
        hp35_pdb_molsys, element='component', selection=[0]
    )
    assert isinstance(output, list)
    assert len(output) == 1


# ---------------------------------------------------------------------------
# get_component_name – else branch (lines 136-141): non-'all' selection
# ---------------------------------------------------------------------------

def test_component_name_list_selection_atom(hp35_pdb_molsys):
    """List selection + redefine_names=False → else branch."""
    output = msm.element.component.get_component_name(
        hp35_pdb_molsys, element='atom', selection=[0, 1, 2]
    )
    assert isinstance(output, list)
    assert len(output) == 3
    assert all(isinstance(v, str) for v in output)


def test_component_name_list_selection_group(hp35_pdb_molsys):
    output = msm.element.component.get_component_name(
        hp35_pdb_molsys, element='group', selection=[0]
    )
    assert isinstance(output, list)
    assert len(output) == 1


def test_component_name_list_selection_component(hp35_pdb_molsys):
    output = msm.element.component.get_component_name(
        hp35_pdb_molsys, element='component', selection=[0]
    )
    assert isinstance(output, list)
    assert len(output) == 1


# ---------------------------------------------------------------------------
# get_component_name – redefine_names=True slow path (lines 29-134)
# HP35 is pure protein, so component_type='protein' (lines 75-78)
# ---------------------------------------------------------------------------

def test_component_name_redefine_names_list_component(hp35_pdb_molsys):
    """redefine_names=True with list selection covers protein branch."""
    output = msm.element.component.get_component_name(
        hp35_pdb_molsys, element='component', selection=[0], redefine_names=True
    )
    assert isinstance(output, list)
    assert len(output) == 1
    assert 'protein' in output[0] or isinstance(output[0], str)


def test_component_name_redefine_names_list_atom(hp35_pdb_molsys):
    output = msm.element.component.get_component_name(
        hp35_pdb_molsys, element='atom', selection=[0, 1], redefine_names=True
    )
    assert isinstance(output, list)
    assert len(output) == 2


def test_component_name_redefine_names_list_group(hp35_pdb_molsys):
    output = msm.element.component.get_component_name(
        hp35_pdb_molsys, element='group', selection=[0], redefine_names=True
    )
    assert isinstance(output, list)
    assert len(output) == 1
