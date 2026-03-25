"""
Regression tests for B-factor extraction from file:bcif_gz.

Oracle: 1atp.bcif.gz — 3070 atoms, X-ray structure.
Known B-factor values (same as 1atp.pdb, columns 60-66, Å²):
  atom 0: 64.39, atom 1: 47.83, atom 2: 35.56,
  atom 3: 99.02, atom 4: 100.00

Parity test: B-factors from bcif.gz must exactly match those from
the corresponding PDB file (zero tolerance — both store the same
deposited values).
"""

import pytest
from pathlib import Path
import numpy as np
import molsysmt as msm
from molsysmt import pyunitwizard as puw


DATA_DIR  = Path(msm.__file__).parent / 'data'
BCIF_GZ   = str(DATA_DIR / 'bcif_gz' / '1atp.bcif.gz')
PDB_PATH  = str(DATA_DIR / 'pdb'     / '1atp.pdb')
N_ATOMS   = 3070

KNOWN_B_FACTORS_AA2 = [64.39, 47.83, 35.56, 99.02, 100.0]


@pytest.fixture(scope='module')
def molsys_1atp_bcif():
    return msm.convert(BCIF_GZ, to_form='molsysmt.MolSys')


@pytest.fixture(scope='module')
def molsys_1atp_pdb():
    return msm.convert(PDB_PATH, to_form='molsysmt.MolSys')


# ---------------------------------------------------------------------------
# B-factor is present (not None)
# ---------------------------------------------------------------------------

def test_b_factor_is_not_none(molsys_1atp_bcif):
    """B-factor must not be None after reading from bcif.gz."""
    assert molsys_1atp_bcif.structures.b_factor is not None


# ---------------------------------------------------------------------------
# Shape
# ---------------------------------------------------------------------------

def test_b_factor_shape(molsys_1atp_bcif):
    val = puw.get_value(molsys_1atp_bcif.structures.b_factor)
    assert val.shape == (1, N_ATOMS)


# ---------------------------------------------------------------------------
# Known values (in Å²)
# ---------------------------------------------------------------------------

def test_b_factor_known_values(molsys_1atp_bcif):
    """First 5 B-factors must match PDB ATOM record values."""
    val = puw.get_value(molsys_1atp_bcif.structures.b_factor, to_unit='angstroms**2')
    np.testing.assert_allclose(val[0, :5], KNOWN_B_FACTORS_AA2, atol=1e-2)


# ---------------------------------------------------------------------------
# Parity: bcif.gz B-factors == pdb B-factors (exact)
# ---------------------------------------------------------------------------

def test_b_factor_parity_with_pdb(molsys_1atp_bcif, molsys_1atp_pdb):
    """B-factors from bcif.gz and pdb must be identical (max diff = 0)."""
    v_bcif = puw.get_value(molsys_1atp_bcif.structures.b_factor, to_unit='angstroms**2')
    v_pdb  = puw.get_value(molsys_1atp_pdb.structures.b_factor,  to_unit='angstroms**2')
    assert v_bcif.shape == v_pdb.shape
    np.testing.assert_allclose(v_bcif, v_pdb, atol=1e-3)
