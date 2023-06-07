"""
Unit and regression test for the wrap_to_pbc method of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.systems import tests as tests_systems
import numpy as np
import math

# Distance between atoms in space and time

def test_wrap_to_pbc_molsysmt_StructuresDict_1():
    molsys = msm.convert(tests_systems['two LJ particles']['traj_two_lj_particles.trjpk'], to_form='molsysmt.StructuresDict')
    distance = msm.structure.get_distances(molsys, selection=0, selection_2=1, pbc=True)
    molsys_wrapped = msm.pbc.wrap_to_pbc(molsys)
    distance_wrapped = msm.structure.get_distances(molsys_wrapped, selection=0, selection_2=1, pbc=True)
    check_distances = np.allclose(distance[:,:,:], distance_wrapped[:,:,:])
    box_length = msm.get(molsys_wrapped, element='system', box_lengths=True)[0,0]
    check_limits_wrapped = ( box_length >= (np.max(molsys_wrapped['coordinates']) - np.min(molsys_wrapped['coordinates'])))
    check_limits = ( box_length <= (np.max(molsys['coordinates']) - np.min(molsys['coordinates'])))
    assert check_limits
    assert check_distances
    assert check_limits_wrapped


