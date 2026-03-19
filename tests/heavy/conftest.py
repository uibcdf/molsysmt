"""
Fixtures for heavy trajectory tests.

Uses the bundled pentalanine h5msm trajectory (5000 frames, 62 atoms)
directly from molsysmt.data.h5msm.
"""
import pytest
import molsysmt as msm

N_ATOMS = 62
N_STRUCTURES = 5000


@pytest.fixture(scope='session')
def pentalanine_h5msm():
    """
    Path to the bundled pentalanine h5msm trajectory (5000 frames, 62 atoms).
    """
    return msm.systems['pentalanine']['traj_pentalanine.h5msm']
