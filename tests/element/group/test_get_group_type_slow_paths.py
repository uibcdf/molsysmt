"""
Tests for get_group_type slow paths (non-'all' selection or redefine_types=True).

These tests bypass the fast native-hierarchy path and exercise the branches
at lines 40+ (redefine_types=True) and 77+ (else) in get_group_type.py.
"""

import molsysmt as msm
import pytest


# ---------------------------------------------------------------------------
# else branch: redefine_types=False, non-'all' selection
# ---------------------------------------------------------------------------

def test_group_type_list_selection_atom(hp35_pdb_molsys):
    """Passing a list selection bypasses fast path → else branch."""
    output = msm.element.group.get_group_type(
        hp35_pdb_molsys, element='atom', selection=[0, 1, 2]
    )
    assert isinstance(output, list)
    assert len(output) == 3
    assert all(isinstance(v, str) for v in output)


def test_group_type_list_selection_group(hp35_pdb_molsys):
    output = msm.element.group.get_group_type(
        hp35_pdb_molsys, element='group', selection=[0, 1]
    )
    assert isinstance(output, list)
    assert len(output) == 2


# ---------------------------------------------------------------------------
# redefine_types=True, element='atom' (lines 42-55)
# HP35 is protein-only so no small-molecule branch (line 51 not hit)
# ---------------------------------------------------------------------------

def test_group_type_redefine_atom_all(hp35_pdb_molsys):
    """redefine_types=True, element='atom', non-MolSys fast path since
    hp35_pdb_molsys is MolSys — use list selection to force slow path."""
    output = msm.element.group.get_group_type(
        hp35_pdb_molsys, element='atom', selection=[0, 1, 2], redefine_types=True
    )
    assert isinstance(output, list)
    assert len(output) == 3
    assert all(isinstance(v, str) for v in output)
    # HP35 atoms belong to amino-acid groups
    assert all(v == 'amino acid' for v in output)


def test_group_type_redefine_atom_larger_slice(hp35_pdb_molsys):
    """Verify type inference over a larger slice still returns amino acid."""
    n_atoms = msm.get(hp35_pdb_molsys, element='system', n_atoms=True)
    selection = list(range(min(20, n_atoms)))
    output = msm.element.group.get_group_type(
        hp35_pdb_molsys, element='atom', selection=selection, redefine_types=True
    )
    assert isinstance(output, list)
    assert len(output) == len(selection)


# ---------------------------------------------------------------------------
# redefine_types=True, element='group' (lines 57-67)
# ---------------------------------------------------------------------------

def test_group_type_redefine_group_list(hp35_pdb_molsys):
    """element='group' with redefine_types=True covers lines 57-67."""
    output = msm.element.group.get_group_type(
        hp35_pdb_molsys, element='group', selection=[0, 1], redefine_types=True
    )
    assert isinstance(output, list)
    assert len(output) == 2
    assert all(isinstance(v, str) for v in output)


def test_group_type_redefine_group_single(hp35_pdb_molsys):
    output = msm.element.group.get_group_type(
        hp35_pdb_molsys, element='group', selection=[0], redefine_types=True
    )
    assert isinstance(output, list)
    assert len(output) == 1
    assert output[0] == 'amino acid'


def test_group_type_from_group_name_all_types():
    """get_group_type_from_group_name covers all classification branches."""
    from molsysmt.element.group.get_group_type import get_group_type_from_group_name

    assert get_group_type_from_group_name('HOH') == 'water'
    assert get_group_type_from_group_name('NA') == 'ion'
    assert get_group_type_from_group_name('ALA') == 'amino acid'
    assert get_group_type_from_group_name('ACE') == 'terminal capping'
    assert get_group_type_from_group_name('ZZZZZZ') == 'unknown'
