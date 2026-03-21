"""
Tests for get_chain_index and get_chain_type slow paths (non-'all' selection).

The fast path (selection='all' + MolSys/Topology) is already covered by existing
tests.  These tests exercise the branches reached when selection is a list or a
non-'all' string, bypassing the early-return native hierarchy shortcut.
"""

import molsysmt as msm
import pytest


# ---------------------------------------------------------------------------
# get_chain_index – else branch (redefine_indices=False, non-'all' selection)
# ---------------------------------------------------------------------------

def test_chain_index_list_selection_atom(hp35_pdb_molsys):
    """Passing a list selection bypasses the fast path and hits the else branch."""
    output = msm.element.chain.get_chain_index(
        hp35_pdb_molsys, element='atom', selection=[0, 1, 2]
    )
    assert isinstance(output, list)
    assert len(output) == 3
    assert all(isinstance(v, int) for v in output)


def test_chain_index_list_selection_group(hp35_pdb_molsys):
    output = msm.element.chain.get_chain_index(
        hp35_pdb_molsys, element='group', selection=[0, 1]
    )
    assert isinstance(output, list)
    assert len(output) == 2


def test_chain_index_list_selection_molecule(hp35_pdb_molsys):
    output = msm.element.chain.get_chain_index(
        hp35_pdb_molsys, element='molecule', selection=[0]
    )
    assert isinstance(output, list)
    assert len(output) == 1


def test_chain_index_list_selection_chain(hp35_pdb_molsys):
    output = msm.element.chain.get_chain_index(
        hp35_pdb_molsys, element='chain', selection=[0]
    )
    assert isinstance(output, list)
    assert len(output) == 1
    assert output[0] == 0


# ---------------------------------------------------------------------------
# get_chain_index – redefine_indices=True, non-'all' selection (slow path)
# ---------------------------------------------------------------------------

def test_chain_index_redefine_true_list_selection_atom(hp35_pdb_molsys):
    """redefine_indices=True with list selection → returns n_atoms * [0]."""
    n_atoms = msm.get(hp35_pdb_molsys, element='system', n_atoms=True)
    output = msm.element.chain.get_chain_index(
        hp35_pdb_molsys, element='atom', selection=[0, 1], redefine_indices=True
    )
    assert isinstance(output, list)
    assert len(output) == n_atoms
    assert all(v == 0 for v in output)


def test_chain_index_redefine_true_list_selection_group(hp35_pdb_molsys):
    n_groups = msm.get(hp35_pdb_molsys, element='system', n_groups=True)
    output = msm.element.chain.get_chain_index(
        hp35_pdb_molsys, element='group', selection=[0], redefine_indices=True
    )
    assert isinstance(output, list)
    assert len(output) == n_groups


def test_chain_index_redefine_true_list_selection_molecule(hp35_pdb_molsys):
    n_molecules = msm.get(hp35_pdb_molsys, element='system', n_molecules=True)
    output = msm.element.chain.get_chain_index(
        hp35_pdb_molsys, element='molecule', selection=[0], redefine_indices=True
    )
    assert isinstance(output, list)
    assert len(output) == n_molecules


def test_chain_index_redefine_true_list_selection_chain(hp35_pdb_molsys):
    output = msm.element.chain.get_chain_index(
        hp35_pdb_molsys, element='chain', selection=[0], redefine_indices=True
    )
    assert output == [0]


def test_chain_index_redefine_true_list_selection_component(hp35_pdb_molsys):
    n_components = msm.get(hp35_pdb_molsys, element='system', n_components=True)
    output = msm.element.chain.get_chain_index(
        hp35_pdb_molsys, element='component', selection=[0], redefine_indices=True
    )
    assert isinstance(output, list)
    assert len(output) == n_components


def test_chain_index_redefine_true_list_selection_entity(hp35_pdb_molsys):
    n_entities = msm.get(hp35_pdb_molsys, element='system', n_entities=True)
    output = msm.element.chain.get_chain_index(
        hp35_pdb_molsys, element='entity', selection=[0], redefine_indices=True
    )
    assert isinstance(output, list)
    assert len(output) == n_entities


# ---------------------------------------------------------------------------
# get_chain_type – else branch (redefine_types=False, non-'all' selection)
# ---------------------------------------------------------------------------

def test_chain_type_list_selection_atom(hp35_pdb_molsys):
    """Passing a list selection bypasses fast path → else branch."""
    output = msm.element.chain.get_chain_type(
        hp35_pdb_molsys, element='atom', selection=[0, 1, 2]
    )
    assert isinstance(output, list)
    assert len(output) == 3
    assert all(isinstance(v, str) for v in output)


def test_chain_type_list_selection_chain(hp35_pdb_molsys):
    output = msm.element.chain.get_chain_type(
        hp35_pdb_molsys, element='chain', selection=[0]
    )
    assert isinstance(output, list)
    assert len(output) == 1


# ---------------------------------------------------------------------------
# get_chain_type – redefine_types=True, non-'all' selection (slow path)
# ---------------------------------------------------------------------------

def test_chain_type_redefine_true_list_chain(hp35_pdb_molsys):
    """redefine_types=True with list selection covers the slow path."""
    output = msm.element.chain.get_chain_type(
        hp35_pdb_molsys, element='chain', selection=[0], redefine_types=True
    )
    assert isinstance(output, list)
    assert len(output) == 1
    assert isinstance(output[0], str)


def test_chain_type_redefine_true_list_atom(hp35_pdb_molsys):
    output = msm.element.chain.get_chain_type(
        hp35_pdb_molsys, element='atom', selection=[0, 1], redefine_types=True
    )
    assert isinstance(output, list)


def test_chain_type_redefine_true_list_group(hp35_pdb_molsys):
    output = msm.element.chain.get_chain_type(
        hp35_pdb_molsys, element='group', selection=[0], redefine_types=True
    )
    assert isinstance(output, list)


def test_chain_type_redefine_true_list_molecule(hp35_pdb_molsys):
    output = msm.element.chain.get_chain_type(
        hp35_pdb_molsys, element='molecule', selection=[0], redefine_types=True
    )
    assert isinstance(output, list)


def test_chain_type_redefine_true_list_component(hp35_pdb_molsys):
    output = msm.element.chain.get_chain_type(
        hp35_pdb_molsys, element='component', selection=[0], redefine_types=True
    )
    assert isinstance(output, list)
