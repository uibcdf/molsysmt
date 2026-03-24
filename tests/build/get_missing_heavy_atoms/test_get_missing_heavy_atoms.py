"""
Unit and regression tests for get_missing_heavy_atoms on molsysmt.MolSys systems.

Tests cover both engine='MolSysMT' (native, default) and engine='PDBFixer'.
"""

import pytest
import molsysmt as msm


# Ground-truth for Barnase-Barstar 1brs: residues with genuinely missing
# sidechain/backbone heavy atoms (25 residues).  Stored as sets to be
# insensitive to atom ordering within each residue's list.
_EXPECTED_1BRS = {
    234: {'CG', 'CD', 'CE', 'NZ'},
    237: {'CG', 'OD1', 'OD2'},
    244: {'CD', 'OE1', 'OE2'},
    246: {'CG', 'CD', 'OE1', 'NE2'},
    254: {'CD', 'CE', 'NZ'},
    260: {'CG1', 'CG2'},
    264: {'CG', 'CD', 'CE', 'NZ'},
    282: {'OG'},
    325: {'O'},
    383: {'OE1', 'NE2'},
    385: {'NZ'},
    386: {'CG', 'CD', 'OE1', 'NE2'},
    422: {'NE', 'CZ', 'NH1', 'NH2'},
    429: {'CG', 'CD', 'OE1', 'NE2'},
    465: {'NE', 'CZ', 'NH1', 'NH2'},
    469: {'CG', 'CD', 'OE1', 'NE2'},
    471: {'CG', 'CD', 'CE', 'NZ'},
    472: {'CG', 'CD', 'OE1', 'NE2'},
    473: {'CG', 'CD1', 'CD2'},
    520: {'CD', 'CE', 'NZ'},
    526: {'CG', 'CD', 'OE1', 'OE2'},
    544: {'CG', 'CD', 'OE1', 'OE2'},
    562: {'CG', 'CD', 'OE1', 'OE2'},
    563: {'CG', 'OD1', 'ND2'},
    587: {'O'},
}


@pytest.fixture(scope='module')
def barnase_barstar():
    return msm.convert(msm.systems['Barnase-Barstar']['1brs.bcif.gz'])


def test_get_missing_heavy_atoms_native_barnase_count(barnase_barstar):
    """MolSysMT engine finds the same 25 residues with missing atoms as PDBFixer."""
    result = msm.build.get_missing_heavy_atoms(barnase_barstar, engine='MolSysMT')
    assert set(result.keys()) == set(_EXPECTED_1BRS.keys())


def test_get_missing_heavy_atoms_native_barnase_atoms(barnase_barstar):
    """MolSysMT engine finds the correct missing atom sets per residue."""
    result = msm.build.get_missing_heavy_atoms(barnase_barstar, engine='MolSysMT')
    for group_idx, expected_atoms in _EXPECTED_1BRS.items():
        assert set(result[group_idx]) == expected_atoms, \
            f"group {group_idx}: expected {expected_atoms}, got {set(result[group_idx])}"


def test_get_missing_heavy_atoms_pdbfixer_barnase(barnase_barstar):
    """PDBFixer engine finds the same missing atoms (regression test)."""
    result = msm.build.get_missing_heavy_atoms(barnase_barstar, engine='PDBFixer')
    assert set(result.keys()) == set(_EXPECTED_1BRS.keys())
    for group_idx, expected_atoms in _EXPECTED_1BRS.items():
        assert set(result[group_idx]) == expected_atoms, \
            f"group {group_idx}: expected {expected_atoms}, got {set(result[group_idx])}"


def test_get_missing_heavy_atoms_native_returns_dict(barnase_barstar):
    """Return value is always a dict."""
    result = msm.build.get_missing_heavy_atoms(barnase_barstar)
    assert isinstance(result, dict)


def test_get_missing_heavy_atoms_native_values_are_sorted_lists(barnase_barstar):
    """MolSysMT engine returns sorted lists of atom names."""
    result = msm.build.get_missing_heavy_atoms(barnase_barstar)
    for atom_list in result.values():
        assert isinstance(atom_list, list)
        assert atom_list == sorted(atom_list)


def test_get_missing_heavy_atoms_complete_structure():
    """Complete structures (built peptide) return empty dict."""
    molsys = msm.build.build_peptide('AceAlaTrpLysNme')
    result = msm.build.get_missing_heavy_atoms(molsys)
    assert result == {}


def test_get_missing_heavy_atoms_native_complete_t4(barnase_barstar):
    """181l (T4 lysozyme, complete) returns empty dict with native engine."""
    t4 = msm.systems['T4 lysozyme L99A']['181l.h5msm']
    result = msm.build.get_missing_heavy_atoms(t4)
    assert result == {}
