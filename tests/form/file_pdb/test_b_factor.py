"""
Regression tests for B-factor extraction from file:pdb.

Oracle: 1atp.pdb — 3070 atoms, X-ray structure.
Known B-factor values from PDB columns 60-66 (Angstroms²):
  atom 0 (N   VAL E  15): 64.39 Å²
  atom 1 (CA  VAL E  15): 47.83 Å²
  atom 2 (C   VAL E  15): 35.56 Å²
  atom 3 (O   VAL E  15): 99.02 Å²
  atom 4 (CB  VAL E  15): 100.00 Å²

These tests catch regressions where b_factor is None (was a bug: the PDB
parser read tempFactor but did not transfer it to the Structures object).
"""

import pytest
from pathlib import Path
import numpy as np
import molsysmt as msm
from molsysmt import pyunitwizard as puw


PDB_PATH  = str(Path(msm.__file__).parent / 'data' / 'pdb' / '1atp.pdb')
N_ATOMS   = 3070

# Ground-truth B-factors (Å²) for first five atoms, taken directly from
# the PDB ATOM records (columns 60-66).
KNOWN_B_FACTORS_AA2 = [64.39, 47.83, 35.56, 99.02, 100.0]


@pytest.fixture(scope='module')
def molsys_1atp_pdb():
    return msm.convert(PDB_PATH, to_form='molsysmt.MolSys')


# ---------------------------------------------------------------------------
# B-factor is present (not None)
# ---------------------------------------------------------------------------

def test_b_factor_is_not_none(molsys_1atp_pdb):
    """B-factor must not be None after reading from PDB."""
    assert molsys_1atp_pdb.structures.b_factor is not None


# ---------------------------------------------------------------------------
# Shape
# ---------------------------------------------------------------------------

def test_b_factor_shape(molsys_1atp_pdb):
    """B-factor shape must be (1, n_atoms)."""
    val = puw.get_value(molsys_1atp_pdb.structures.b_factor)
    assert val.shape == (1, N_ATOMS)


# ---------------------------------------------------------------------------
# Known values (in Å²)
# ---------------------------------------------------------------------------

def test_b_factor_known_values(molsys_1atp_pdb):
    """First 5 B-factors must match the values in the PDB ATOM records."""
    val = puw.get_value(molsys_1atp_pdb.structures.b_factor, to_unit='angstroms**2')
    np.testing.assert_allclose(val[0, :5], KNOWN_B_FACTORS_AA2, atol=1e-2)


# ---------------------------------------------------------------------------
# Via msm.get
# ---------------------------------------------------------------------------

def test_b_factor_via_get(molsys_1atp_pdb):
    """msm.get(..., b_factor=True) must return a pint quantity."""
    b = msm.get(molsys_1atp_pdb, element='atom', selection='all', b_factor=True)
    assert b is not None
    val = puw.get_value(b, to_unit='angstroms**2')
    assert val.shape == (1, N_ATOMS)
    np.testing.assert_allclose(val[0, :5], KNOWN_B_FACTORS_AA2, atol=1e-2)
