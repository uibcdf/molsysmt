"""
Unit and regression test for the is_composed_of module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

def test_is_composed_of_1():
    molsys = msm.demo.classes.T4_Lysozyme_L99A_in_pdbid_181l(to_form='molsysmt.MolSys')
    output = msm.is_composed_of(molsys, proteins=True)
    assert output == False

def test_is_composed_of_2():
    molsys = msm.demo.classes.T4_Lysozyme_L99A_in_pdbid_181l(to_form='molsysmt.MolSys')
    output = msm.is_composed_of(molsys, proteins=True, waters=True, small_molecules=True, ions=True)
    assert output == True

def test_is_composed_of_3():
    molsys = msm.demo.classes.T4_Lysozyme_L99A_in_pdbid_181l(to_form='molsysmt.MolSys')
    output = msm.is_composed_of(molsys, proteins=1, waters=True, small_molecules=2, ions=True)
    assert output == True

def test_is_composed_of_4():
    molsys = msm.demo.classes.T4_Lysozyme_L99A_in_pdbid_181l(to_form='molsysmt.MolSys')
    molsys = msm.extract(molsys, selection='molecule_type=="protein"')
    output = msm.is_composed_of(molsys, proteins=1)
    assert output == True

def test_is_composed_of_5():
    molsys = msm.demo.classes.T4_Lysozyme_L99A_in_pdbid_181l(to_form='molsysmt.MolSys')
    molsys = msm.extract(molsys, selection='molecule_type=="protein"')
    output = msm.is_composed_of(molsys, proteins=1, waters=2, ions=2)
    assert output == False

