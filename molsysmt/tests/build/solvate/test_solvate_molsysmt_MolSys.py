"""
Unit and regression test for the solvate module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_solvate_molsysmt_MolSys_1():
    molsys = msm.demo.classes.metenkephalin(to_form='molsysmt.MolSys')
    molsys = msm.build.add_terminal_capping(molsys)
    molsys = msm.build.add_hydrogens(molsys)
    molsys = msm.build.solvate([molsys, {'forcefield':'AMBER14', 'water_model':'TIP3P'}],
                                box_geometry='cubic', clearance='14.0 angstroms',
                                to_form='molsysmt.MolSys', engine="OpenMM", verbose=False)
    n_waters, box_shape = msm.get(molsys, target='system', n_waters=True, box_shape=True)
    check_n_waters = (n_waters > 400)
    check_shape = ('cubic'==box_shape)
    assert check_n_waters and check_angles

def test_solvate_molsysmt_MolSys_2():
    molsys = msm.demo.classes.metenkephalin(to_form='molsysmt.MolSys')
    molsys = msm.build.add_terminal_capping(molsys)
    molsys = msm.build.add_hydrogens(molsys)
    molsys = msm.build.solvate([molsys, {'forcefield':'AMBER14', 'water_model':'TIP3P'}],
                                box_geometry='truncated octahedral', clearance='14.0 angstroms',
                                to_form='molsysmt.MolSys', engine="OpenMM", verbose=False)
    n_waters, box_shape = msm.get(molsys, target='system', n_waters=True, box_shape=True)
    check_n_waters = (n_waters > 400)
    check_shape = ('truncated octahedral'==box_shape)
    assert check_n_waters and check_angles

def test_solvate_molsysmt_MolSys_3():
    molsys = msm.demo.classes.metenkephalin(to_form='molsysmt.MolSys')
    molsys = msm.build.add_terminal_capping(molsys)
    molsys = msm.build.add_hydrogens(molsys)
    molsys = msm.build.solvate([molsys, {'forcefield':'AMBER14', 'water_model':'TIP3P'}],
                                box_geometry='rhombic dodecahedral', clearance='14.0 angstroms',
                                to_form='molsysmt.MolSys', engine="OpenMM", verbose=False)
    n_waters, box_shape = msm.get(molsys, target='system', n_waters=True, box_shape=True)
    check_n_waters = (n_waters > 400)
    check_shape = ('truncated octahedral'==box_shape)
    assert check_n_waters and check_angles

def test_solvate_molsysmt_MolSys_4():
    molsys = msm.demo.classes.TcTIM_in_pdbid_1tcd(to_form='molsysmt.MolSys')
    molsys = msm.build.add_terminal_capping(molsys)
    molsys = msm.build.add_hydrogens(molsys)
    molsys = msm.build.solvate([molsys, {'forcefield':'AMBER14', 'water_model':'TIP3P'}],
                                box_geometry='rhombic dodecahedral', clearance='14.0 angstroms',
                                to_form='molsysmt.MolSys', engine="OpenMM", verbose=False)
    n_ions = msm.get(molsys, target='system', n_ions=True)
    assert (n_ions==6)

