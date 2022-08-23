"""
Unit and regression test for the center module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_translate_molsysmt_MolSys_1():
    molsys = msm.convert(msm.demo['Met-enkephalin']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    coordinates_0 = msm.get(molsys, coordinates=True)
    n_atoms = msm.get(molsys, n_atoms=True)
    shifts = np.ones([n_atoms,3], dtype=float)*msm.pyunitwizard.unit('nm')
    molsys = msm.structure.translate(molsys, translation=shifts)
    coordinates = msm.get(molsys, coordinates=True)
    check_value = np.allclose(coordinates_0+shifts, coordinates)
    assert check_value

def test_translate_molsysmt_MolSys_2():
    molsys = msm.convert(msm.demo['Met-enkephalin']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    coordinates_0 = msm.get(molsys, coordinates=True)
    shifts = np.array([1.0, 1.0, 1.0], dtype=float)*msm.pyunitwizard.unit('nm')
    molsys = msm.structure.translate(molsys, translation=shifts, selection=[0,1,2], in_place=False)
    coordinates = msm.get(molsys, coordinates=True)
    coordinates_0[0,0,:]=coordinates_0[0,0,:]+shifts
    coordinates_0[0,1,:]=coordinates_0[0,1,:]+shifts
    coordinates_0[0,2,:]=coordinates_0[0,2,:]+shifts
    check_value = np.allclose(coordinates_0, coordinates)
    assert check_value


