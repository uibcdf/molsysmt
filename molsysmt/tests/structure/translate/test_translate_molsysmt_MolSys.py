"""
Unit and regression test for the center module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_translate_molsysmt_MolSys_1():

    molsys = msm.demo.classes.metenkephalin(to_form='molsysmt.MolSys')
    n_atoms = msm.get(molsys, n_atoms=True)
    shifts = np.ones([n_atoms,3], dtype=float)*msm.puw.unit('nm')
    molsys = msm.structure.translate(molsys, translation=shifts)
    coordinates = msm.get(molsys, coordinates=True)
    true_value_1 = np.array([[1.3326, 1.1548, 1.    ],
       [1.3909, 1.0724, 1.    ],
       [1.397 , 1.2846, 1.    ]])
    true_value_2 = np.array([[2.8161, 2.4927, 1.2287],
       [2.7833, 2.0413, 1.    ],
       [2.8356, 1.9301, 1.    ]])
    check_value_1 = np.allclose(true_value_1, msm.puw.get_value(coordinates[0,:3,:]))
    check_value_2 = np.allclose(true_value_2, msm.puw.get_value(coordinates[0,-3:,:]))
    assert check_value_1 and check_value_2

def test_translate_molsysmt_MolSys_2():

    molsys = msm.demo.classes.metenkephalin(to_form='molsysmt.MolSys')
    shifts = np.array([1.0, 1.0, 1.0], dtype=float)*msm.puw.unit('nm')
    molsys = msm.structure.translate(molsys, translation=shifts, selection=[0,1,2], in_place=False)
    coordinates = msm.get(molsys, coordinates=True)
    true_value_1 = np.array([[1.3326, 1.1548, 1.    ],
       [1.3909, 1.0724, 1.    ],
       [1.397 , 1.2846, 1.    ]])
    true_value_2 = np.array([[1.8161, 1.4927, 0.2287],
       [1.7833, 1.0413, 0.    ],
       [1.8356, 0.9301, 0.    ]])
    check_value_1 = np.allclose(true_value_1, msm.puw.get_value(coordinates[0,:3,:]))
    check_value_2 = np.allclose(true_value_2, msm.puw.get_value(coordinates[0,-3:,:]))
    assert check_value_1 and check_value_2


