"""
Unit and regression test for the is_composed_of module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

def test_is_composed_of_1():
    molsys = msm.convert(msm.demo['chicken villin HP35']['solvated.msmpk'], to_form='molsysmt.MolSys')
    output = msm.is_composed_of(molsys, proteins=True)
    assert output == False

def test_is_composed_of_2():
    molsys = msm.convert(msm.demo['chicken villin HP35']['solvated.msmpk'], to_form='molsysmt.MolSys')
    output = msm.is_composed_of(molsys, peptides=True, waters=True, ions=True)
    assert output == True

def test_is_composed_of_3():
    molsys = msm.convert(msm.demo['chicken villin HP35']['solvated.msmpk'], to_form='molsysmt.MolSys')
    output = msm.is_composed_of(molsys, peptides=1, waters=True, ions=True)
    assert output == True

def test_is_composed_of_4():
    molsys = msm.convert(msm.demo['chicken villin HP35']['solvated.msmpk'], to_form='molsysmt.MolSys')
    molsys = msm.extract(molsys, selection='molecule_type=="peptide"')
    output = msm.is_composed_of(molsys, peptides=1)
    assert output == True

def test_is_composed_of_5():
    molsys = msm.convert(msm.demo['chicken villin HP35']['solvated.msmpk'], to_form='molsysmt.MolSys')
    molsys = msm.extract(molsys, selection='molecule_type=="protein"')
    output = msm.is_composed_of(molsys, proteins=1, waters=2, ions=2)
    assert output == False

