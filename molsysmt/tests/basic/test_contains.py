"""
Unit and regression test for the merge module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

def test_contains_1():
    molsys = msm.convert(msm.demo['T4 lysozyme L99A']['181l.pdb'], to_form='molsysmt.MolSys')
    output = msm.contains(molsys, waters=True)
    assert output == True

def test_contains_2():
    molsys = msm.convert(msm.demo['T4 lysozyme L99A']['181l.pdb'], to_form='molsysmt.MolSys')
    output = msm.contains(molsys, ions=True, small_molecules=True, proteins=True)
    assert output == True

def test_contains_3():
    molsys = msm.convert(msm.demo['T4 lysozyme L99A']['181l.pdb'], to_form='molsysmt.MolSys')
    output = msm.contains(molsys, proteins=True, lipids=True)
    assert output == False

def test_contains_4():
    molsys = msm.convert(msm.demo['T4 lysozyme L99A']['181l.pdb'], to_form='molsysmt.MolSys')
    output = msm.contains(molsys, lipids=False)
    assert output == True

def test_contains_5():
    molsys = msm.convert(msm.demo['T4 lysozyme L99A']['181l.pdb'], to_form='molsysmt.MolSys')
    output = msm.contains(molsys, proteins=True, lipids=False)
    assert output == True

def test_contains_6():
    molsys = msm.convert(msm.demo['T4 lysozyme L99A']['181l.pdb'], to_form='molsysmt.MolSys')
    output = msm.contains(molsys, waters=100, ions=2)
    assert output == True

def test_contains_7():
    molsys = msm.convert(msm.demo['T4 lysozyme L99A']['181l.pdb'], to_form='molsysmt.MolSys')
    output = msm.contains(molsys, small_molecules=3, ions=2)
    assert output == False

