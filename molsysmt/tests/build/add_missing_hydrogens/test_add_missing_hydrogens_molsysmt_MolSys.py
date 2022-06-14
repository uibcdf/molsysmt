"""
Unit and regression test for the add_hydrogens module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_add_hydrogens_molsysmt_MolSys_1():
    molsys = msm.convert(msm.demo['Met-enkephalin']['vacuum.pdb'], to_form='molsysmt.MolSys')
    molsys = msm.remove(molsys, selection='atom_type=="H"')
    output_before = msm.contains(molsys, hydrogens=True)
    molsys = msm.build.add_missing_hydrogens(molsys)
    output_after = msm.contains(molsys, hydrogens=True)
    check = (output_after == True) and (output_before == False)
    assert check

