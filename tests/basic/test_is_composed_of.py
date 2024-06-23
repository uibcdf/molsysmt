"""
Unit and regression test for the is_composed_of module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

molsys = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'], to_form='molsysmt.MolSys')

def test_is_composed_of_1():
    output = msm.is_composed_of(molsys, proteins=True)
    assert output == False

def test_is_composed_of_2():
    output = msm.is_composed_of(molsys, ions=True, waters=True, peptides=True)
    assert output == True

def test_is_composed_of_3():
    output = msm.is_composed_of(molsys, ions=True, waters=True, peptides=1)
    assert output == True

def test_is_composed_of_4():
    molsys_ext = msm.extract(molsys, selection='molecule_type=="peptide"')
    output = msm.is_composed_of(molsys_ext, peptides=1)
    assert output == True

def test_is_composed_of_5():
    output = msm.is_composed_of(molsys, ions=2, waters=2, proteins=1)
    assert output == False

def test_is_composed_of_6():
    output = msm.is_composed_of(molsys, ions=2, waters=1483, peptides=1)
    assert output == True

