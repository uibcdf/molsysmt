"""
Unit and regression test for the get_structure_alignment module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

# Distance between atoms in space and time

def test_flip_molsysmt_MolSys_1():

    crd = msm.systems['POPC']['popc.crd']
    psf = msm.systems['POPC']['popc.psf']
    molsys = msm.convert([crd, psf])

    molsys = msm.structure.center(molsys, selection='all', center_of_selection='atom_name=="P"',
                              center_coordinates=[0.0, 0.0, 2.0]*msm.pyunitwizard.quantity('nm'))

    coors1 = msm.get(molsys, selection='atom_name=="P"', coordinates=True)
    good_coors1 = np.array([[[0.0, 0.0, 2.0]]])

    molsys2 = msm.structure.flip(molsys, vector=[0,0,1], point='[0,0,0] nm')

    coors2 = msm.get(molsys2, selection='atom_name=="P"', coordinates=True)
    good_coors2 = np.array([[[0.0, 0.0, -2.0]]])


    assert np.allclose(msm.pyunitwizard.get_value(coors1), good_coors1)
    assert np.allclose(msm.pyunitwizard.get_value(coors2), good_coors2)

def test_flip_molsysmt_MolSys_2():

    crd = msm.systems['POPC']['popc.crd']
    psf = msm.systems['POPC']['popc.psf']
    molsys = msm.convert([crd, psf])

    molsys = msm.structure.center(molsys, selection='all', center_of_selection='atom_name=="P"',
                              center_coordinates=[0.0, 0.0, 2.0]*msm.pyunitwizard.quantity('nm'))

    coors1 = msm.get(molsys, selection='atom_name=="P"', coordinates=True)
    good_coors1 = np.array([[[0.0, 0.0, 2.0]]])

    msm.structure.flip(molsys, vector=[0,0,1], point='[0,0,0] nm', in_place=True)

    coors2 = msm.get(molsys, selection='atom_name=="P"', coordinates=True)
    good_coors2 = np.array([[[0.0, 0.0, -2.0]]])


    assert np.allclose(msm.pyunitwizard.get_value(coors1), good_coors1)
    assert np.allclose(msm.pyunitwizard.get_value(coors2), good_coors2)


