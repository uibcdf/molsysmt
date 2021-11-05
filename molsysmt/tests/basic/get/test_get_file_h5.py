"""
Unit and regression test for the get module of the molsysmt package on h5 file systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np


def test_get_file_h5_1():
    molsys = msm.demo['pentalanine']['traj.h5']
    n_atoms, n_frames = msm.get(molsys, target='system', n_atoms=True, n_frames=True)
    assert (n_atoms==62) and (n_frames==5000)

