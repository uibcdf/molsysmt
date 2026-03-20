"""
Tests for molsysmt.basic.contains covering all branches of the function
and the _evaluation internal helper.
"""
import molsysmt as msm
from molsysmt import systems
import pytest


@pytest.fixture()
def t4_molsys(t4_h5msm_molsys):
    return t4_h5msm_molsys


@pytest.fixture()
def hp35_sol(hp35_solvated_molsys):
    return hp35_solvated_molsys


# ---------------------------------------------------------------------------
# No kwargs (n_atoms branch)
# ---------------------------------------------------------------------------

def test_contains_no_kwargs_whole_system(t4_molsys):
    """No kwargs on non-empty system returns True."""
    result = msm.contains(t4_molsys)
    assert result is True


def test_contains_no_kwargs_with_selection(t4_molsys):
    """No kwargs with a valid selection that contains atoms returns True."""
    result = msm.contains(t4_molsys, selection='molecule_type=="protein"')
    assert result is True


def test_contains_no_kwargs_empty_selection(t4_molsys):
    """No kwargs with a selection that yields no atoms returns False."""
    result = msm.contains(t4_molsys, selection='molecule_type=="rna"')
    assert result is False


# ---------------------------------------------------------------------------
# Single boolean kwarg
# ---------------------------------------------------------------------------

def test_contains_single_kwarg_true_present(t4_molsys):
    """n_waters=True when waters are present returns True."""
    result = msm.contains(t4_molsys, n_waters=True)
    assert result is True


def test_contains_single_kwarg_true_absent(t4_molsys):
    """n_rnas=True when no RNAs returns False."""
    result = msm.contains(t4_molsys, n_rnas=True)
    assert result is False


def test_contains_single_kwarg_false_absent(t4_molsys):
    """n_rnas=False when no RNAs returns True (absence satisfies False condition)."""
    result = msm.contains(t4_molsys, n_rnas=False)
    assert result is True


def test_contains_single_kwarg_false_present(t4_molsys):
    """n_waters=False when waters are present returns False."""
    result = msm.contains(t4_molsys, n_waters=False)
    assert result is False


# ---------------------------------------------------------------------------
# Integer threshold kwarg
# ---------------------------------------------------------------------------

def test_contains_int_threshold_satisfied(t4_molsys):
    """n_waters=1 when system has >0 waters returns True."""
    result = msm.contains(t4_molsys, n_waters=1)
    assert result is True


def test_contains_int_threshold_not_satisfied(t4_molsys):
    """n_proteins=2 when system has only 1 protein returns False."""
    result = msm.contains(t4_molsys, n_proteins=2)
    assert result is False


# ---------------------------------------------------------------------------
# Multiple kwargs
# ---------------------------------------------------------------------------

def test_contains_multi_kwargs_all_true(t4_molsys):
    """n_waters=True and n_ions=True when both present returns True."""
    result = msm.contains(t4_molsys, n_waters=True, n_ions=True)
    assert result is True


def test_contains_multi_kwargs_one_fails(t4_molsys):
    """n_waters=True and n_rnas=True when RNAs absent returns False."""
    result = msm.contains(t4_molsys, n_waters=True, n_rnas=True)
    assert result is False


# ---------------------------------------------------------------------------
# Selection restricts the check
# ---------------------------------------------------------------------------

def test_contains_selection_restricts_waters(t4_molsys):
    """selection='molecule_type=="protein"' → n_waters=True fails (no waters in protein subset)."""
    result = msm.contains(t4_molsys, selection='molecule_type=="protein"', n_waters=True)
    assert result is False


def test_contains_selection_restricts_proteins(t4_molsys):
    """selection='molecule_type=="protein"' → n_proteins=True succeeds."""
    result = msm.contains(t4_molsys, selection='molecule_type=="protein"', n_proteins=True)
    assert result is True


# ---------------------------------------------------------------------------
# Solvated system
# ---------------------------------------------------------------------------

def test_contains_solvated_peptides(hp35_sol):
    """HP35 solvated has peptides, ions, and waters."""
    assert msm.contains(hp35_sol, n_peptides=True) is True
    assert msm.contains(hp35_sol, n_waters=True) is True
    assert msm.contains(hp35_sol, n_ions=True) is True
    assert msm.contains(hp35_sol, n_proteins=True) is False
