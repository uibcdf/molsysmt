"""
Unit and regression tests for get_missing_terminal_cappings on molsysmt.MolSys systems.

Tests cover both engine='MolSysMT' (native, default) and engine='PDBFixer'.
"""

import pytest
import molsysmt as msm


@pytest.fixture(scope='module')
def barnase_barstar():
    return msm.convert(msm.systems['Barnase-Barstar']['1brs.bcif.gz'])


@pytest.fixture(scope='module')
def t4_lysozyme():
    return msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'])


def test_get_missing_terminal_cappings_native_barnase(barnase_barstar):
    """MolSysMT engine finds OXT missing at group 412 (SER, chain 3 C-terminus)."""
    result = msm.build.get_missing_terminal_cappings(barnase_barstar, engine='MolSysMT')
    assert len(result) == 1
    assert result[412] == ['OXT']


def test_get_missing_terminal_cappings_pdbfixer_barnase(barnase_barstar):
    """PDBFixer engine finds the same missing OXT (regression test)."""
    result = msm.build.get_missing_terminal_cappings(barnase_barstar, engine='PDBFixer')
    assert len(result) == 1
    assert result[412] == ['OXT']


def test_get_missing_terminal_cappings_native_t4(t4_lysozyme):
    """MolSysMT engine finds OXT missing at group 161 (LYS, C-terminus of T4)."""
    result = msm.build.get_missing_terminal_cappings(t4_lysozyme, engine='MolSysMT')
    assert len(result) == 1
    assert result[161] == ['OXT']


def test_get_missing_terminal_cappings_pdbfixer_t4(t4_lysozyme):
    """PDBFixer engine agrees with native on T4 lysozyme."""
    result = msm.build.get_missing_terminal_cappings(t4_lysozyme, engine='PDBFixer')
    assert len(result) == 1
    assert result[161] == ['OXT']


def test_get_missing_terminal_cappings_returns_dict(barnase_barstar):
    """Return value is always a dict."""
    result = msm.build.get_missing_terminal_cappings(barnase_barstar)
    assert isinstance(result, dict)


def test_get_missing_terminal_cappings_capped_peptide():
    """NME-capped peptide returns empty dict (no missing OXT)."""
    molsys = msm.build.build_peptide('AceAlaTrpLysNme')
    result = msm.build.get_missing_terminal_cappings(molsys, engine='MolSysMT')
    assert result == {}


def test_get_missing_terminal_cappings_engines_agree(barnase_barstar):
    """MolSysMT and PDBFixer engines return the same group indices."""
    native = msm.build.get_missing_terminal_cappings(barnase_barstar, engine='MolSysMT')
    pdbfixer = msm.build.get_missing_terminal_cappings(barnase_barstar, engine='PDBFixer')
    assert set(native.keys()) == set(pdbfixer.keys())
