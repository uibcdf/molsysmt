"""
Unit and regression test for the compare module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.systems import tests as tests_systems
import numpy as np

def test_compare_all_eq_1():
    molsys_A = msm.convert(tests_systems['T4 lysozyme L99A']['t4_lysozyme_L99A.msmpk'], to_form='molsysmt.MolSys')
    molsys_B = msm.convert(tests_systems['T4 lysozyme L99A']['t4_lysozyme_L99A.msmpk'], to_form='molsysmt.MolSys')
    output = msm.compare(molsys_A, molsys_B, attributes_type='topological', coordinates=True, box=True)
    assert output == True

def test_compare_all_eq_2():
    molsys_A = msm.convert(tests_systems['T4 lysozyme L99A']['t4_lysozyme_L99A.msmpk'], to_form='molsysmt.MolSys')
    molsys_B = msm.convert(tests_systems['chicken villin HP35']['chicken_villin_HP35.msmpk'], to_form='molsysmt.MolSys')
    output = msm.compare(molsys_A, molsys_B, attributes_type='topological', coordinates=True, box=True)
    assert output == False

def test_compare_all_eq_3():
    molsys_A = msm.convert(tests_systems['T4 lysozyme L99A']['181l.mmtf'], to_form='openmm.Modeller')
    molsys_B = msm.convert(molsys_A, to_form='molsysmt.MolSys')
    output = msm.compare(molsys_A, molsys_B)
    assert output == True
