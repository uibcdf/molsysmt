"""
Unit and regression test for the is solvate module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_is_solvate_molsysmt_MolSys_1():
    molsys = msm.demo.classes.metenkephalin(to_form='molsysmt.MolSys')
    molsys = msm.build.add_terminal_capping(molsys)
    molsys = msm.build.add_hydrogens(molsys)
    molsys = msm.build.solvate([molsys, {'forcefield':'AMBER14', 'water_model':'TIP3P'}],
                                box_geometry='cubic', clearance='14.0 angstroms',
                                to_form='molsysmt.MolSys', engine="OpenMM", verbose=False)
    output_before = msm.build.is_solvated(molsys)
    molsys = msm.build.remove_solvent(molsys)
    output_after = msm.build.is_solvated(molsys)
    check_before = (output_before == True)
    check_after = (output_after == False)
    assert check_before and check_after

