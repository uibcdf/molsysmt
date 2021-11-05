"""
Unit and regression test for the has_hydrogens module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_has_hydrogens_molsysmt_MolSys_1():
    molsys = msm.convert(msm.demo['Met-enkephalin']['vacuum.pdb'], to_form='molsysmt.MolSys')
    output = msm.build.has_hydrogens(molsys)
    check = (output == True)
    assert check

def test_has_hydrogens_molsysmt_MolSys_2():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.build.has_hydrogens(molsys)
    check = (output == False)
    assert check

