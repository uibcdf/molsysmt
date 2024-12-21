"""
Unit and regression test for the get_dihedral_angles module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

# Distance between atoms in space and time

def test_get_angles_from_molsysmt_MolSys_1():
    molsys = msm.systems['pentalanine']['traj_pentalanine.h5']
    molsys = msm.convert(molsys)
    angles = msm.structure.get_angles(molsys, [0,1,2])
    check1 = ((5000,1)==angles.shape)
    good_angles = [113.06116981671607, 107.22517056178846, 116.89755264175076, 114.74587424352482, 107.95984387161585]
    check2 = np.allclose(good_angles, msm.pyunitwizard.get_value(angles[:5,0], to_unit='degrees'))
    assert check1
    assert check2

def test_get_angles_from_molsysmt_MolSys_2():
    molsys = msm.systems['pentalanine']['traj_pentalanine.h5']
    molsys = msm.convert(molsys)
    angles = msm.structure.get_angles(molsys, [0,1,2], structure_indices=[0,1,2,3,4], pbc=True)
    check1 = ((5,1)==angles.shape)
    good_angles = [113.06116981671607, 107.22517056178846, 116.89755264175076, 114.74587424352482, 107.95984387161585]
    check2 = np.allclose(good_angles, msm.pyunitwizard.get_value(angles[:,0], to_unit='degrees'))
    assert check1
    assert check2

