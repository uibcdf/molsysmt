"""
Unit and regression test for the get_ramachandran_angles module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_get_ramachandran_angles_from_molsysmt_MolSys_1():
    molsys = msm.convert(msm.demo['pentalanine']['traj.h5'], to_form='molsysmt.MolSys')
    phi_chains, psi_chains, phi_angles, psi_angles = msm.structure.get_ramachandran_angles(molsys)
    true_value_1 = np.array([-113.48003593, -161.21280086, -136.75724095, -144.99215202, -174.64791676])
    true_value_2 = np.array([149.55691211, 137.51702185, 133.44230978, 127.61043836, 163.17747611])
    check_shape_1 = np.all((5,4)==phi_chains.shape)
    check_shape_2 = np.all((5000,5)==phi_angles.shape)
    check_value_1 = np.allclose(true_value_1, msm.pyunitwizard.get_value(phi_angles[1000], to_unit='degrees'))
    check_value_2 = np.allclose(true_value_2, msm.pyunitwizard.get_value(psi_angles[1000], to_unit='degrees'))
    assert check_shape_1 and check_shape_2 and  check_value_1 and check_value_2

def test_get_ramachandran_angles_from_molsysmt_MolSys_2():
    molsys = msm.convert(msm.demo['pentalanine']['traj.h5'], to_form='molsysmt.MolSys')
    phi_chains, psi_chains, phi_angles, psi_angles = msm.structure.get_ramachandran_angles(molsys, selection='group_index==[1,2]')
    true_value_1 = np.array([[-161.21280086],
       [ -71.93406033],
       [ -73.2385    ],
       [-124.81261977],
       [ -69.92631791]])
    true_value_2 = np.array([[149.55691211],
       [153.02215527],
       [124.80226598],
       [117.3054522 ],
       [138.19847597]])
    check_shape_1 = np.all((1,4)==phi_chains.shape)
    check_shape_2 = np.all((5000,1)==phi_angles.shape)
    check_value_1 = np.allclose(true_value_1, msm.pyunitwizard.get_value(phi_angles[1000:1005], to_unit='degrees'))
    check_value_2 = np.allclose(true_value_2, msm.pyunitwizard.get_value(psi_angles[1000:1005], to_unit='degrees'))
    assert check_shape_1 and check_shape_2 and  check_value_1 and check_value_2

