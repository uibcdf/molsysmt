"""
Parity tests for get_non_standard_residues: MolSysMT engine vs PDBFixer engine.

The MolSysMT engine uses a ~817-entry MDTraj-derived name-to-canonical-code
table, while PDBFixer uses a ~150-entry internal table.  On systems where both
engines know the residue, they should agree.

Synthetic test: a built peptide with one group renamed to a well-known
non-standard residue (MSE → MET, PTR → TYR) to verify that both engines
return the same replacement recommendation.
"""

import pytest
import molsysmt as msm


@pytest.fixture(scope='module')
def t4_lysozyme():
    return msm.systems['T4 lysozyme L99A']['181l.h5msm']


@pytest.fixture(scope='module')
def mol_with_mse():
    """A built peptide where one residue has been renamed to MSE (selenomethionine)."""
    mol = msm.build.build_peptide('ACDEFGHIKLMNPQRSTVWY', engine='MolSysMT',
                                   to_form='molsysmt.MolSys')
    # Rename group 10 (MET) → MSE so both engines can find it
    mol.topology.groups.at[10, 'group_name'] = 'MSE'
    mol.topology._groups_dirty = True
    return mol


@pytest.fixture(scope='module')
def mol_with_ptr():
    """A built peptide where one residue has been renamed to PTR (phosphotyrosine)."""
    mol = msm.build.build_peptide('ACDEFGHIKLMNPQRSTVWY', engine='MolSysMT',
                                   to_form='molsysmt.MolSys')
    # Rename group 19 (TYR) → PTR
    mol.topology.groups.at[19, 'group_name'] = 'PTR'
    mol.topology._groups_dirty = True
    return mol


# ── Standard-only structures: both engines agree on empty result ──────────────

def test_parity_t4_both_engines_empty(t4_lysozyme):
    """Both engines return {} for T4 lysozyme (no non-standard residues)."""
    r_native = msm.build.get_non_standard_residues(t4_lysozyme, engine='MolSysMT')
    r_pdb    = msm.build.get_non_standard_residues(t4_lysozyme, engine='PDBFixer')
    assert r_native == {}
    assert r_pdb    == {}


# ── MSE (selenomethionine → MET) ─────────────────────────────────────────────

def test_parity_mse_detected_native(mol_with_mse):
    """MolSysMT detects MSE and maps it to MET."""
    result = msm.build.get_non_standard_residues(mol_with_mse, engine='MolSysMT')
    assert 10 in result
    assert result[10].upper() == 'MET'


def test_parity_mse_detected_pdbfixer(mol_with_mse):
    """PDBFixer detects MSE and maps it to MET."""
    result = msm.build.get_non_standard_residues(mol_with_mse, engine='PDBFixer')
    assert 10 in result
    assert result[10].upper() == 'MET'


def test_parity_mse_engines_agree_keys(mol_with_mse):
    """Both engines identify the same set of non-standard group indices."""
    r_native = msm.build.get_non_standard_residues(mol_with_mse, engine='MolSysMT')
    r_pdb    = msm.build.get_non_standard_residues(mol_with_mse, engine='PDBFixer')
    assert set(r_native.keys()) == set(r_pdb.keys())


def test_parity_mse_engines_agree_replacement(mol_with_mse):
    """Both engines recommend the same replacement name for MSE."""
    r_native = msm.build.get_non_standard_residues(mol_with_mse, engine='MolSysMT')
    r_pdb    = msm.build.get_non_standard_residues(mol_with_mse, engine='PDBFixer')
    assert r_native[10].upper() == r_pdb[10].upper()


# ── PTR (phosphotyrosine → TYR) ──────────────────────────────────────────────

def test_parity_ptr_detected_native(mol_with_ptr):
    """MolSysMT detects PTR and maps it to TYR."""
    result = msm.build.get_non_standard_residues(mol_with_ptr, engine='MolSysMT')
    assert 19 in result
    assert result[19].upper() == 'TYR'


def test_parity_ptr_detected_pdbfixer(mol_with_ptr):
    """PDBFixer detects PTR and maps it to TYR."""
    result = msm.build.get_non_standard_residues(mol_with_ptr, engine='PDBFixer')
    assert 19 in result
    assert result[19].upper() == 'TYR'
