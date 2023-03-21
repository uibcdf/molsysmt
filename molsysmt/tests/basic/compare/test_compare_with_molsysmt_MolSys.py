"""
Unit and regression test for the compare module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

def test_compare_all_eq_1():
    molsys_A = msm.convert(msm.demo['T4 lysozyme L99A']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    molsys_B = msm.convert(msm.demo['T4 lysozyme L99A']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    output = msm.compare(molsys_A, molsys_B, rule='equal', elements=True, coordinates=True, box=True, form=True)
    assert output == True

def test_compare_all_eq_2():
    molsys_A = msm.convert(msm.demo['T4 lysozyme L99A']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    molsys_B = msm.convert(msm.demo['chicken villin HP35']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    output = msm.compare(molsys_A, molsys_B, rule='equal', elements=True, coordinates=True, box=True, form=True)
    assert output == False

def test_compare_all_eq_3():
    molsys_A = msm.convert(msm.demo['T4 lysozyme L99A']['181l.mmtf'], to_form='openmm.Modeller')
    molsys_B = msm.convert(molsys_A, to_form='molsysmt.MolSys')
    output = msm.compare(molsys_A, molsys_B)
    assert output == True
