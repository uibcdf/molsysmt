"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

def test_pdbid_to_molsysmt_MolSys():
    molsys = msm.demo.classes.T4_lysozyme_L99A_in_pdbid_181l(to_form='molsysmt.MolSys')
    output = msm.contains(molsys, water=True)
    assert output == True

