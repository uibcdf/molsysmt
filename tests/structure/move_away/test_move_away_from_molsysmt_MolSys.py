"""
Unit and regression test for the shift_dihedral_angles module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np

# Distance between atoms in space and time

def test_move_away_from_molsysmt_MolSys_1():

    molsys1 = msm.convert(systems['alanine dipeptide']['alanine_dipeptide.h5msm'])
    molsys2 = msm.convert(systems['valine dipeptide']['valine_dipeptide.h5msm'])

    msm.structure.center(molsys1, in_place=True)

    molsys2 = msm.structure.move_away(molsys2, reference_molecular_system=molsys1,
                                      direction=[1,0,0], distance='1 nanometer')

    center1 = msm.structure.get_center(molsys1)
    center2 = msm.structure.get_center(molsys2)

    assert np.allclose(puw.get_value(center1[0,0,:]),[0,0,0])
    assert np.allclose(puw.get_value(center2[0,0,:]),[1,0,0])

def test_move_away_from_molsysmt_MolSys_2():

    molsys1 = msm.convert(systems['alanine dipeptide']['alanine_dipeptide.h5msm'])
    molsys2 = msm.convert(systems['valine dipeptide']['valine_dipeptide.h5msm'])

    molsys1 = msm.structure.center(molsys1, in_place=False)

    msm.structure.move_away(molsys2, reference_molecular_system=molsys1,
                            direction=[1,0,0], distance='1 nanometer', in_place=True)

    center1 = msm.structure.get_center(molsys1)
    center2 = msm.structure.get_center(molsys2)

    assert np.allclose(puw.get_value(center1[0,0,:]),[0,0,0])
    assert np.allclose(puw.get_value(center2[0,0,:]),[1,0,0])

def test_move_away_from_molsysmt_MolSys_3():

    molsys1 = msm.convert(systems['alanine dipeptide']['alanine_dipeptide.h5msm'])
    molsys2 = msm.convert(systems['valine dipeptide']['valine_dipeptide.h5msm'])

    molsys1 = msm.structure.center(molsys1, in_place=False)
    molsys2 = msm.structure.center(molsys2, center_coordinates="[1.0,0.0,0.0] nm", in_place=False)

    molsys2 = msm.structure.move_away(molsys2, reference_molecular_system=molsys1,
                                      direction=None, distance='2 nanometer')

    center1 = msm.structure.get_center(molsys1)
    center2 = msm.structure.get_center(molsys2)

    assert np.allclose(puw.get_value(center1[0,0,:]),[0,0,0])
    assert np.allclose(puw.get_value(center2[0,0,:]),[3,0,0])

def test_move_away_from_molsysmt_MolSys_4():

    molsys1 = msm.convert(systems['alanine dipeptide']['alanine_dipeptide.h5msm'])
    molsys2 = msm.convert(systems['valine dipeptide']['valine_dipeptide.h5msm'])

    msm.structure.center(molsys1, in_place=True)
    msm.structure.center(molsys2, center_coordinates="[1.0,0.0,0.0] nm", in_place=True)

    msm.structure.move_away(molsys2, reference_molecular_system=molsys1,
                                       direction=None, distance='2 nanometer', in_place=True)

    center1 = msm.structure.get_center(molsys1)
    center2 = msm.structure.get_center(molsys2)

    assert np.allclose(puw.get_value(center1[0,0,:]),[0,0,0])
    assert np.allclose(puw.get_value(center2[0,0,:]),[3,0,0])

