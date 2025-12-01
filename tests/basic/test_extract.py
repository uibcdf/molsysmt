"""
Unit and regression test for the extract module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
from molsysmt import systems


def test_extract_1(t4_h5msm_molsys):
    molsys = t4_h5msm_molsys
    molsys = msm.extract(molsys, selection='molecule_type=="small molecule"')
    output = msm.is_composed_of(molsys, small_molecules=2)
    assert output == True

def test_extract_2(t4_h5msm_molsys):
    molsys = t4_h5msm_molsys
    molsys = msm.convert(molsys, to_form='molsysmt.MolSys')
    molsys = msm.extract(molsys, selection='molecule_type=="water"')
    output = msm.is_composed_of(molsys, waters=136)
    assert output == True

def test_extract_3(t4_h5msm_molsys):
    molsys = t4_h5msm_molsys
    molsys = msm.convert(molsys, to_form='molsysmt.MolSys')
    molsys = msm.extract(molsys, selection='molecule_type==["water", "protein"]')
    output = msm.is_composed_of(molsys, waters=True, proteins=True)
    assert output == True

