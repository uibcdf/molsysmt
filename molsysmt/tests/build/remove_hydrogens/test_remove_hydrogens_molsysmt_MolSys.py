"""
Unit and regression test for the remove_hydrogens module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_remove_hydrogens_molsysmt_MolSys_1():
    molsys = msm.convert(msm.demo['Met-enkephalin']['vacuum.pdb'], to_form='molsysmt.MolSys')
    molsys = msm.build.remove_hydrogens(molsys)
    output = msm.build.has_hydrogens(molsys)
    check = (output == False)
    assert check


