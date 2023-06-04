"""
Unit and regression test for the unwrap method of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import math

# Distance between atoms in space and time

def test_unwrap_molsysmt_StructuresDict_1():
    molsys = msm.convert(msm.demo['two LJ particles']['traj.trjpk'], to_form='molsysmt.StructuresDict')
    molsys_wrapped = msm.pbc.wrap_to_pbc(molsys)
    molsys_unwrapped = msm.pbc.unwrap(molsys_wrapped)
    box_length = msm.get(molsys_wrapped, element='system', box_lengths=True)[0,0]
    check_limits_wrapped = ( box_length >= (np.max(molsys_wrapped['coordinates']) - np.min(molsys_wrapped['coordinates'])))
    check_limits = ( box_length <= (np.max(molsys['coordinates']) - np.min(molsys['coordinates'])))
    check_limits_unwrapped = ( box_length <= (np.max(molsys_unwrapped['coordinates']) - np.min(molsys['coordinates'])))
    check = np.allclose(molsys_unwrapped['coordinates'][:,:,:], molsys['coordinates'][:,:,:])
    assert check_limits
    assert check_limits_unwrapped
    assert check_limits_wrapped
    assert check


