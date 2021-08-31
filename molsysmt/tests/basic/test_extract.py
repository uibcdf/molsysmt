"""
Unit and regression test for the extract module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np


def test_extract_1():
    molsys = msm.demo.files['1sux.mmtf']
    molsys = msm.convert(molsys, to_form='molsysmt.MolSys')
    molsys = msm.extract(molsys, selection='molecule_type=="small molecule"')
    output = msm.is_composed_of(molsys, small_molecules=1)
    assert output == True

def test_extract_2():
    molsys = msm.demo.files['1sux.mmtf']
    molsys = msm.convert(molsys, to_form='molsysmt.MolSys')
    molsys = msm.extract(molsys, selection='molecule_type=="water"')
    output = msm.is_composed_of(molsys, waters=374)
    assert output == True

def test_extract_3():
    molsys = msm.demo.files['1sux.mmtf']
    molsys = msm.convert(molsys, to_form='molsysmt.MolSys')
    molsys = msm.extract(molsys, selection='molecule_type==["water", "protein"]')
    output = msm.is_composed_of(molsys, waters=True, proteins=True)
    assert output == True

