"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

# Whole systems (selection='all' and structure_indices='all')

def test_file_psf_to_molsysmt_MolSys():
    file_psf = systems['POPC membrane']['popc_membrane.psf']
    molsys = msm.convert(file_psf, to_form='molsysmt.MolSys')
    form = msm.get_form(molsys)
    n_atoms, n_lipids, n_structures = msm.get(molsys, n_atoms=True, n_lipids=True, n_structures=True)
    assert form=='molsysmt.MolSys'
    assert n_atoms==78974
    assert n_lipids==294
    assert n_structures==0

def test_file_psf_to_molsysmt_Topology():
    file_psf = systems['POPC membrane']['popc_membrane.psf']
    molsys = msm.convert(file_psf, to_form='molsysmt.Topology')
    form = msm.get_form(molsys)
    n_atoms, n_lipids, n_structures = msm.get(molsys, n_atoms=True, n_lipids=True, n_structures=True)
    assert form=='molsysmt.Topology'
    assert n_atoms==78974
    assert n_lipids==294
    assert n_structures==None


