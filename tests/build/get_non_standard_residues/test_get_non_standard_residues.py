"""
Tests for msm.build.get_non_standard_residues.

The function wraps PDBFixer's findNonstandardResidues and returns a dict
mapping group (residue) indices to replacement standard-residue names.

Systems used
------------
- T4 lysozyme L99A (181l.h5msm): well-curated, no non-standard residues → {}
- chicken villin HP35 (chicken_villin_HP35.h5msm): all-standard protein → {}
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

def test_get_non_standard_residues_returns_dict(t4_lysozyme):
    """Return value is always a dict."""
    result = msm.build.get_non_standard_residues(t4_lysozyme)
    assert isinstance(result, dict)


def test_get_non_standard_residues_keys_are_ints(t4_lysozyme):
    """Dict keys (group indices) are integers when result is non-empty, dict is empty otherwise."""
    result = msm.build.get_non_standard_residues(t4_lysozyme)
    for k in result:
        assert isinstance(k, int)


def test_get_non_standard_residues_values_are_strings(t4_lysozyme):
    """Dict values (residue names) are strings when result is non-empty."""
    result = msm.build.get_non_standard_residues(t4_lysozyme)
    for v in result.values():
        assert isinstance(v, str)


# ---------------------------------------------------------------------------
# Known results
# ---------------------------------------------------------------------------

def test_get_non_standard_residues_t4_lysozyme_empty(t4_lysozyme):
    """181l has no non-standard residues after pre-processing into h5msm."""
    result = msm.build.get_non_standard_residues(t4_lysozyme)
    assert result == {}


def test_get_non_standard_residues_villin_empty(villin):
    """Chicken villin HP35 has no non-standard residues."""
    result = msm.build.get_non_standard_residues(villin)
    assert result == {}


# ---------------------------------------------------------------------------
# Selection argument
# ---------------------------------------------------------------------------

def test_get_non_standard_residues_with_selection(t4_lysozyme):
    """Passing an explicit selection restricts the search without error."""
    result = msm.build.get_non_standard_residues(t4_lysozyme, selection='molecule_type=="protein"')
    assert isinstance(result, dict)


def test_get_non_standard_residues_selection_first_chain(t4_lysozyme):
    """Selection by chain_index restricts search to that chain."""
    result = msm.build.get_non_standard_residues(t4_lysozyme, selection='chain_index==0')
    assert isinstance(result, dict)
