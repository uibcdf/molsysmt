"""
Tests for string_smiles/is_form.py.

Covers both the smiles: prefix path and the regex/rdkit fallback.
The rdkit-dependent getter tests are skipped when rdkit is not installed.
"""

import pytest
from molsysmt.form.string_smiles.is_form import is_form
import molsysmt as msm

try:
    import rdkit
    HAS_RDKIT = True
except ImportError:
    HAS_RDKIT = False

needs_rdkit = pytest.mark.skipif(not HAS_RDKIT, reason="rdkit not installed")


# ---------------------------------------------------------------------------
# is_form — prefix path (always works, no rdkit needed)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("smiles", [
    "smiles:CN1C=NC2=C1C(=O)N(C(=O)N2C)C",   # caffeine
    "smiles:CCO",                               # ethanol (simple, forced prefix)
    "smiles:CC(N)C(=O)O",                       # alanine
    "smiles:c1ccccc1",                           # benzene (aromatic)
])
def test_is_form_with_prefix(smiles):
    assert is_form(smiles) is True


@pytest.mark.parametrize("bad", [
    "smiles:",       # empty after prefix
    "",              # empty string
    42,              # not a string
    None,
])
def test_is_form_prefix_rejects_bad(bad):
    assert is_form(bad) is False


# ---------------------------------------------------------------------------
# is_form — no prefix, regex fallback (rdkit may or may not be present)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("smiles", [
    "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",   # caffeine — has =, (, digits
    "c1ccccc1",                          # benzene — lowercase atoms
    "CC(N)C(=O)O",                       # alanine — has (, =
])
def test_is_form_no_prefix_structural(smiles):
    """Strings with structural markers are detected with or without rdkit."""
    assert is_form(smiles) is True


@pytest.mark.parametrize("not_smiles", [
    "ACDEFGHIKL",    # amino-acid sequence — uppercase only, no structural marker
    "1aki",          # PDB id
    "CCO",           # ethanol — only uppercase, rejected by regex (use smiles: prefix)
    "hello world",   # garbage
])
def test_is_form_no_prefix_rejects_non_smiles(not_smiles):
    assert is_form(not_smiles) is False


# ---------------------------------------------------------------------------
# get_form dispatch
# ---------------------------------------------------------------------------

def test_get_form_with_prefix():
    assert msm.get_form("smiles:CN1C=NC2=C1C(=O)N(C(=O)N2C)C") == "string:smiles"


def test_get_form_no_prefix_structural():
    assert msm.get_form("CN1C=NC2=C1C(=O)N(C(=O)N2C)C") == "string:smiles"


# ---------------------------------------------------------------------------
# Getter tests — require rdkit
# ---------------------------------------------------------------------------

@needs_rdkit
def test_n_atoms_caffeine():
    # Caffeine: C8H10N4O2 → 24 heavy atoms
    assert msm.get("smiles:CN1C=NC2=C1C(=O)N(C(=O)N2C)C", element='system', n_atoms=True) == 24


@needs_rdkit
def test_n_bonds_caffeine():
    # Caffeine has 25 bonds
    assert msm.get("smiles:CN1C=NC2=C1C(=O)N(C(=O)N2C)C", element='system', n_bonds=True) == 25


@needs_rdkit
def test_roundtrip_rdkit_mol():
    caffeine = "smiles:CN1C=NC2=C1C(=O)N(C(=O)N2C)C"
    mol = msm.convert(caffeine, to_form='rdkit.Mol')
    back = msm.convert(mol, to_form='string:smiles')
    assert back.startswith('smiles:')
    assert msm.get(back, element='system', n_atoms=True) == 24
