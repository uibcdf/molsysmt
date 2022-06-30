"""
Unit and regression test for the is solvate module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import pytest
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_is_solvate_molsysmt_MolSys_1():
    molsys = msm.convert(msm.demo['Met-enkephalin']['vacuum.pdb'], to_form='molsysmt.MolSys')
    molsys = msm.build.add_missing_terminal_cappings(molsys)
    molsys = msm.build.add_missing_hydrogens(molsys)
    output_before = msm.build.is_solvated(molsys)
    molsys = msm.build.solvate([molsys, {'forcefield':'AMBER14', 'water_model':'TIP3P'}],
                                box_geometry='cubic', clearance='14.0 angstroms',
                                to_form='molsysmt.MolSys', engine="OpenMM")
    output_after = msm.build.is_solvated(molsys)
    check_before = (output_before == False)
    check_after = (output_after == True)
    assert check_before and check_after

