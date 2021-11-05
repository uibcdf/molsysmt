"""
Unit and regression test for the center module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_center_molsysmt_MolSys_1():

    molsys = msm.convert(msm.demo['pentalanine']['traj.h5'], to_form='molsysmt.MolSys')
    n_frames = msm.get(molsys, n_frames=True)
    origin = np.zeros([n_frames, 1, 3])*msm.puw.unit('nanometers')
    molsys = msm.structure.center(molsys)
    distance = msm.structure.get_distances(molsys, group_behavior='geometric_center', molecular_system_2=origin)
    true_distance = np.zeros([n_frames, 1, 1])*msm.puw.unit('nanometers')
    check = np.allclose(distance, true_distance)
    assert check

