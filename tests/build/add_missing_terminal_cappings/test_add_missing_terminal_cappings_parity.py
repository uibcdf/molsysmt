"""
Parity tests for add_missing_terminal_cappings: MolSysMT engine vs PDBFixer engine.

Both engines should produce the same total atom count, the same number of OXT
atoms, and OXT bonded correctly to the C of the terminal residue.

Structure used: Barnase-Barstar (1brs.bcif.gz) — has one C-terminal residue
(SER, group 412) with missing OXT.
"""

import pytest
import molsysmt as msm


@pytest.fixture(scope='module')
def barnase_barstar():
    return msm.convert(msm.systems['Barnase-Barstar']['1brs.bcif.gz'])


@pytest.fixture(scope='module')
def t4_lysozyme():
    return msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'])


# ── Barnase-Barstar ───────────────────────────────────────────────────────────

def test_parity_1brs_total_atom_count(barnase_barstar):
    """Both engines produce the same total atom count after adding OXT."""
    r_native = msm.build.add_missing_terminal_cappings(barnase_barstar, engine='MolSysMT')
    r_pdb    = msm.build.add_missing_terminal_cappings(barnase_barstar, engine='PDBFixer')
    assert msm.get(r_native, n_atoms=True) == msm.get(r_pdb, n_atoms=True)


def test_parity_1brs_oxt_count(barnase_barstar):
    """Both engines add exactly the same number of OXT atoms."""
    r_native = msm.build.add_missing_terminal_cappings(barnase_barstar, engine='MolSysMT')
    r_pdb    = msm.build.add_missing_terminal_cappings(barnase_barstar, engine='PDBFixer')
    oxt_n = msm.get(r_native, element='atom', selection='atom_name=="OXT"', n_atoms=True)
    oxt_p = msm.get(r_pdb,    element='atom', selection='atom_name=="OXT"', n_atoms=True)
    assert oxt_n == oxt_p


def test_parity_1brs_group_412_has_oxt(barnase_barstar):
    """Both engines add OXT to group 412 (the missing one)."""
    for eng in ('MolSysMT', 'PDBFixer'):
        r = msm.build.add_missing_terminal_cappings(barnase_barstar, engine=eng)
        names_412 = msm.get(r, element='atom', selection='group_index==412', atom_name=True)
        assert 'OXT' in names_412, f"{eng}: OXT missing from group 412"


def test_parity_1brs_no_missing_terminal_after_fix(barnase_barstar):
    """After native fix, get_missing_terminal_cappings returns empty dict."""
    r_native = msm.build.add_missing_terminal_cappings(barnase_barstar, engine='MolSysMT')
    missing = msm.build.get_missing_terminal_cappings(r_native, engine='MolSysMT')
    assert missing == {}


# ── T4 lysozyme ───────────────────────────────────────────────────────────────

def test_parity_t4_total_atom_count(t4_lysozyme):
    """Both engines produce the same total atom count on T4 lysozyme."""
    r_native = msm.build.add_missing_terminal_cappings(t4_lysozyme, engine='MolSysMT')
    r_pdb    = msm.build.add_missing_terminal_cappings(t4_lysozyme, engine='PDBFixer')
    assert msm.get(r_native, n_atoms=True) == msm.get(r_pdb, n_atoms=True)


def test_parity_t4_no_missing_terminal_after_fix(t4_lysozyme):
    """After native fix on T4, no terminal cappings are reported missing."""
    r_native = msm.build.add_missing_terminal_cappings(t4_lysozyme, engine='MolSysMT')
    missing = msm.build.get_missing_terminal_cappings(r_native, engine='MolSysMT')
    assert missing == {}


# ── Capped peptide (no change expected) ──────────────────────────────────────

def test_parity_capped_peptide_no_change():
    """ACE-capped peptide is unchanged by both engines (nothing missing)."""
    mol = msm.build.build_peptide('AceAlaTrpLysNme')
    n_before = msm.get(mol, n_atoms=True)
    for eng in ('MolSysMT', 'PDBFixer'):
        r = msm.build.add_missing_terminal_cappings(mol, engine=eng)
        assert msm.get(r, n_atoms=True) == n_before, f"{eng}: atom count changed on capped peptide"
