"""
Tests for msm.build.get_missing_residues.

The function wraps PDBFixer's findMissingResidues and returns a dict mapping
(chain_index, insertion_position) tuples to lists of residue names.

Systems used
------------
- T4 lysozyme L99A (181l.h5msm): complete structure → {}
- chicken villin HP35 (chicken_villin_HP35.h5msm): complete structure → {}
"""

import molsysmt as msm
from molsysmt import systems
import pytest


@pytest.fixture(scope="module")
def t4_lysozyme():
    return systems['T4 lysozyme L99A']['181l.h5msm']


@pytest.fixture(scope="module")
def villin():
    return systems['chicken villin HP35']['chicken_villin_HP35.h5msm']


# ---------------------------------------------------------------------------
# Return type and structure
# ---------------------------------------------------------------------------

def test_get_missing_residues_returns_dict(t4_lysozyme):
    """Return value is always a dict."""
    result = msm.build.get_missing_residues(t4_lysozyme)
    assert isinstance(result, dict)


def test_get_missing_residues_keys_are_tuples(t4_lysozyme):
    """Dict keys are (chain_index, insertion_position) int tuples."""
    result = msm.build.get_missing_residues(t4_lysozyme)
    for k in result:
        assert isinstance(k, tuple)
        assert len(k) == 2
        assert isinstance(k[0], int)
        assert isinstance(k[1], int)


def test_get_missing_residues_values_are_lists_of_strings(t4_lysozyme):
    """Dict values are lists of residue name strings."""
    result = msm.build.get_missing_residues(t4_lysozyme)
    for v in result.values():
        assert isinstance(v, list)
        for name in v:
            assert isinstance(name, str)


# ---------------------------------------------------------------------------
# Known results
# ---------------------------------------------------------------------------

def test_get_missing_residues_t4_lysozyme_complete(t4_lysozyme):
    """181l.h5msm is a complete structure: no missing residues."""
    result = msm.build.get_missing_residues(t4_lysozyme)
    assert result == {}


def test_get_missing_residues_villin_complete(villin):
    """Chicken villin HP35 h5msm is a complete structure: no missing residues."""
    result = msm.build.get_missing_residues(villin)
    assert result == {}


# ---------------------------------------------------------------------------
# Selection argument
# ---------------------------------------------------------------------------

def test_get_missing_residues_with_selection(t4_lysozyme):
    """Passing an explicit selection restricts the search without error."""
    result = msm.build.get_missing_residues(t4_lysozyme, selection='molecule_type=="protein"')
    assert isinstance(result, dict)


def test_get_missing_residues_selection_first_chain(t4_lysozyme):
    """Selection by chain_index restricts search to that chain."""
    result = msm.build.get_missing_residues(t4_lysozyme, selection='chain_index==0')
    assert isinstance(result, dict)
