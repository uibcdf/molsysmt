"""
Tests for get_molecule_type slow paths (non-'all' selection).

These bypass the fast native-hierarchy path (selection='all' + MolSys/Topology)
and exercise the redefine_indices, redefine_types, and plain else branches.
"""

import molsysmt as msm
import pytest


# ---------------------------------------------------------------------------
# else branch (lines 127-131): redefine_types=False, non-'all' selection
# ---------------------------------------------------------------------------

def test_molecule_type_list_selection_molecule(hp35_pdb_molsys):
    """List selection bypasses fast path → else branch."""
    output = msm.element.molecule.get_molecule_type(
        hp35_pdb_molsys, element='molecule', selection=[0]
    )
    assert isinstance(output, list)
    assert len(output) == 1
    assert isinstance(output[0], str)


def test_molecule_type_list_selection_atom(hp35_pdb_molsys):
    output = msm.element.molecule.get_molecule_type(
        hp35_pdb_molsys, element='atom', selection=[0, 1, 2]
    )
    assert isinstance(output, list)
    assert len(output) == 3


def test_molecule_type_list_selection_group(hp35_pdb_molsys):
    output = msm.element.molecule.get_molecule_type(
        hp35_pdb_molsys, element='group', selection=[0]
    )
    assert isinstance(output, list)
    assert len(output) == 1


# ---------------------------------------------------------------------------
# redefine_types=True, non-'all' selection (lines 67-125)
# ---------------------------------------------------------------------------

def test_molecule_type_redefine_types_list_molecule(hp35_pdb_molsys):
    """redefine_types=True + list selection covers the slow redefine path."""
    output = msm.element.molecule.get_molecule_type(
        hp35_pdb_molsys, element='molecule', selection=[0], redefine_types=True
    )
    assert isinstance(output, list)
    assert len(output) == 1
    assert isinstance(output[0], str)


def test_molecule_type_redefine_types_list_atom(hp35_pdb_molsys):
    output = msm.element.molecule.get_molecule_type(
        hp35_pdb_molsys, element='atom', selection=[0, 1], redefine_types=True
    )
    assert isinstance(output, list)
    assert len(output) == 2


def test_molecule_type_redefine_types_list_group(hp35_pdb_molsys):
    output = msm.element.molecule.get_molecule_type(
        hp35_pdb_molsys, element='group', selection=[0], redefine_types=True
    )
    assert isinstance(output, list)
    assert len(output) == 1


def test_molecule_type_redefine_types_list_component(hp35_pdb_molsys):
    output = msm.element.molecule.get_molecule_type(
        hp35_pdb_molsys, element='component', selection=[0], redefine_types=True
    )
    assert isinstance(output, list)
    assert len(output) == 1



def test_molecule_type_redefine_types_chain_list(hp35_pdb_molsys):
    """element='chain' with redefine_types=True, list selection (lines 112-117)."""
    output = msm.element.molecule.get_molecule_type(
        hp35_pdb_molsys, element='chain', selection=[0], redefine_types=True
    )
    assert isinstance(output, list)
    assert len(output) == 1
    # Each entry for a chain is a list of molecule types in that chain
    assert isinstance(output[0], list)


def test_molecule_type_redefine_types_entity_list(hp35_pdb_molsys):
    """element='entity' with redefine_types=True, list selection (lines 118-123)."""
    output = msm.element.molecule.get_molecule_type(
        hp35_pdb_molsys, element='entity', selection=[0], redefine_types=True
    )
    assert isinstance(output, list)


# ---------------------------------------------------------------------------
# redefine_indices=True, non-'all' selection (lines 39-65)
# ---------------------------------------------------------------------------

def test_molecule_type_redefine_indices_list_molecule(hp35_pdb_molsys):
    """redefine_indices=True + list selection covers lines 39-59."""
    output = msm.element.molecule.get_molecule_type(
        hp35_pdb_molsys, element='molecule', selection=[0], redefine_indices=True
    )
    assert isinstance(output, list)



def test_molecule_type_redefine_indices_list_group(hp35_pdb_molsys):
    output = msm.element.molecule.get_molecule_type(
        hp35_pdb_molsys, element='group', selection=[0], redefine_indices=True
    )
    assert isinstance(output, list)


def test_molecule_type_redefine_indices_list_component(hp35_pdb_molsys):
    output = msm.element.molecule.get_molecule_type(
        hp35_pdb_molsys, element='component', selection=[0], redefine_indices=True
    )
    assert isinstance(output, list)
