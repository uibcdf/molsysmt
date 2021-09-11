"""
Unit and regression test for the wrap_to_pbc method of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import math

# Distance between atoms in space and time

def test_wrap_to_pbc_molsysmt_TrajectoryDict_1():
    molsys = msm.demo.classes.Ar_Xe_pbc_vacuum_traj(to_form='molsysmt.TrajectoryDict')
    distance = msm.structure.get_distances(molsys, selection=0, selection_2=1, pbc=True)
    molsys_wrapped = msm.pbc.wrap_to_pbc(molsys)
    distance_wrapped = msm.structure.get_distances(molsys_wrapped, selection=0, selection_2=1, pbc=True)
    check_distances = np.allclose(distance[:,:,:], distance_wrapped[:,:,:])
    box_length = msm.get(molsys_wrapped, target='system', box_lengths=True)[0,0]
    check_limits_wrapped = ( box_length >= (np.max(molsys_wrapped['coordinates']) - np.min(molsys_wrapped['coordinates'])))
    check_limits = ( box_length <= (np.max(molsys['coordinates']) - np.min(molsys['coordinates'])))
    assert check_limits and check_distances and check_limits_wrapped


