"""
Unit and regression test for the solvate module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import pytest
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

@pytest.mark.skip
def test_solvate_molsysmt_MolSys_1():
    molsys = msm.convert(msm.demo['chicken villin HP35']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    molsys = msm.build.add_missing_terminal_cappings(molsys)
    molsys = msm.build.add_missing_hydrogens(molsys)
    molsys = msm.build.solvate([molsys, {'forcefield':'AMBER14', 'water_model':'TIP3P'}],
                                box_geometry='cubic', clearance='14.0 angstroms',
                                to_form='molsysmt.MolSys', engine="OpenMM", verbose=False)
    n_waters, box_shape, n_ions = msm.get(molsys, target='system', n_waters=True, box_shape=True,
            n_ions=True)
    check_n_waters = (n_waters > 400)
    check_shape = ('cubic'==box_shape)
    check_n_ions = (n_ions==2)
    assert check_n_waters and check_shape and check_n_ions

@pytest.mark.skip
def test_solvate_molsysmt_MolSys_2():
    molsys = msm.convert(msm.demo['chicken villin HP35']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    molsys = msm.build.add_missing_terminal_cappings(molsys)
    molsys = msm.build.add_missing_hydrogens(molsys)
    molsys = msm.build.solvate([molsys, {'forcefield':'AMBER14', 'water_model':'TIP3P'}],
                                box_geometry='truncated octahedral', clearance='14.0 angstroms',
                                to_form='molsysmt.MolSys', engine="OpenMM", verbose=False)
    n_waters, box_shape = msm.get(molsys, target='system', n_waters=True, box_shape=True)
    check_n_waters = (n_waters > 400)
    check_shape = ('truncated octahedral'==box_shape)
    assert check_n_waters and check_shape

@pytest.mark.skip
def test_solvate_molsysmt_MolSys_3():
    molsys = msm.convert(msm.demo['chicken villin HP35']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    molsys = msm.build.add_missing_terminal_cappings(molsys)
    molsys = msm.build.add_missing_hydrogens(molsys)
    molsys = msm.build.solvate([molsys, {'forcefield':'AMBER14', 'water_model':'TIP3P'}],
                                box_geometry='rhombic dodecahedral', clearance='14.0 angstroms',
                                to_form='molsysmt.MolSys', engine="OpenMM", verbose=False)
    n_waters, box_shape = msm.get(molsys, target='system', n_waters=True, box_shape=True)
    check_n_waters = (n_waters > 400)
    check_shape = ('rhombic dodecahedral'==box_shape)
    assert check_n_waters and check_shape

