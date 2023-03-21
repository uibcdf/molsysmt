"""
Unit and regression test for the solvate module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import pytest
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_solvate_molsysmt_MolSys_1():
    molsys = msm.convert(msm.demo['chicken villin HP35']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    molsys = msm.build.add_missing_terminal_cappings(molsys)
    molsys = msm.build.add_missing_hydrogens(molsys)
    molsys = msm.build.solvate([molsys, {'forcefield':'AMBER14', 'water_model':'TIP3P'}],
                                box_shape='cubic', clearance='14.0 angstroms',
                                to_form='molsysmt.MolSys', engine="OpenMM")
    n_waters, box_shape, n_ions = msm.get(molsys, element='system', n_waters=True, box_shape=True,
            n_ions=True)
    assert n_waters > 400
    assert 'cubic'==box_shape
    assert n_ions==2

def test_solvate_molsysmt_MolSys_2():
    molsys = msm.convert(msm.demo['chicken villin HP35']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    molsys = msm.build.add_missing_terminal_cappings(molsys)
    molsys = msm.build.add_missing_hydrogens(molsys)
    molsys = msm.build.solvate([molsys, {'forcefield':'AMBER14', 'water_model':'TIP3P'}],
                                box_shape='truncated octahedral', clearance='14.0 angstroms',
                                to_form='molsysmt.MolSys', engine="OpenMM")
    n_waters, box_shape = msm.get(molsys, element='system', n_waters=True, box_shape=True)
    assert n_waters > 400
    assert 'truncated octahedral'==box_shape

def test_solvate_molsysmt_MolSys_3():
    molsys = msm.convert(msm.demo['chicken villin HP35']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    molsys = msm.build.add_missing_terminal_cappings(molsys)
    molsys = msm.build.add_missing_hydrogens(molsys)
    molsys = msm.build.solvate([molsys, {'forcefield':'AMBER14', 'water_model':'TIP3P'}],
                                box_shape='rhombic dodecahedral', clearance='14.0 angstroms',
                                to_form='molsysmt.MolSys', engine="OpenMM")
    n_waters, box_shape = msm.get(molsys, element='system', n_waters=True, box_shape=True)
    assert n_waters > 400
    assert 'rhombic dodecahedral'==box_shape

