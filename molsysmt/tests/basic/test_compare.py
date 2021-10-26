"""
Unit and regression test for the compare module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

def test_compare_all_eq_1():
    molsys_A = msm.convert(msm.demo.t4_lysozyme_L99A['vacuum.msmpk'], to_form='molsysmt.MolSys')
    molsys_B = msm.convert(msm.demo.t4_lysozyme_L99A['vacuum.msmpk'], to_form='molsysmt.MolSys')
    output = msm.compare(molsys_A, molsys_B, comparison='all', rule='A_eq_B')
    assert output == True

def test_compare_all_eq_2():
    molsys_A = msm.convert(msm.demo.t4_lysozyme_L99A['vacuum.msmpk'], to_form='molsysmt.MolSys')
    molsys_B = msm.convert(msm.demo.villin_HP35['vacuum.msmpk'], to_form='molsysmt.MolSys')
    output = msm.compare(molsys_A, molsys_B, comparison='all', rule='A_eq_B')
    assert output == False


