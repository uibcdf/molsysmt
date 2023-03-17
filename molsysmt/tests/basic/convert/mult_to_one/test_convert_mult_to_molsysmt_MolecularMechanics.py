"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.basic.convert import _convert_multiple_to_one_with_shortcuts, _convert_multiple_to_one
import numpy as np
import os

def test_convert_molsysmt_MolSys_and_molsysmt_MolecularMechanicsDict_to_molsysmt_MolecularMechanics():
    molsys = msm.convert(msm.demo['chicken villin HP35']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    molsys.molecular_mechanics.dispersion_correction=True
    molsys = msm.convert([molsys, {'forcefield':'AMBER14', 'water_model':'TIP3P'}], to_form='molsysmt.MolecularMechanics')
    form = msm.get_form(molsys)
    assert 'molsysmt.MolecularMechanics'==form
    assert True==msm.get(molsys, dispersion_correction=True)
    assert 'AMBER14'==msm.get(molsys, forcefield=True)
    assert 'TIP3P'==msm.get(molsys, water_model=True)

def test_convert_molsysmt_MolecularMechanicsDict_and_molsysmt_MolecularMechanicsDict_to_molsysmt_MolecularMechanics():
    molsys = msm.convert([{'dispersion_correction':True}, {'forcefield':'AMBER14', 'water_model':'TIP3P'}], to_form='molsysmt.MolecularMechanics')
    form = msm.get_form(molsys)
    assert 'molsysmt.MolecularMechanics'==form
    assert True==msm.get(molsys, dispersion_correction=True)
    assert 'AMBER14'==msm.get(molsys, forcefield=True)
    assert 'TIP3P'==msm.get(molsys, water_model=True)

