"""
Unit and regression test for the get module of the molsysmt package on h5 file systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np


def test_get_file_h5_1():
    molsys = systems['pentalanine']['traj_pentalanine.h5']
    n_atoms, n_structures = msm.get(molsys, element='system', n_atoms=True, n_structures=True)
    assert (n_atoms==62) and (n_structures==5000)

