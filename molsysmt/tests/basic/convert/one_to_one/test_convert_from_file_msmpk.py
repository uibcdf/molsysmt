"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.systems import tests as tests_systems
import numpy as np
import os

# Whole systems (selection='all' and structure_indices='all')

def test_file_msmpk_to_molsysmt_MolSys():
    molsys = tests_systems['T4 lysozyme L99A']['t4_lysozyme_L99A.msmpk']
    molsys = msm.convert(molsys, to_form='molsysmt.MolSys')
    assert 'molsysmt.MolSys'==msm.get_form(molsys)

def test_file_msmpk_to_nglview_NGLWidget():
    molsys = tests_systems['T4 lysozyme L99A']['t4_lysozyme_L99A.msmpk']
    molsys_ref = msm.convert(molsys, to_form='molsysmt.MolSys')
    molsys = msm.convert(molsys, to_form='nglview.NGLWidget')
    n_molecules, n_structures = msm.get(molsys, element='system', n_molecules=True, n_structures=True)
    n_molecules_ref, n_structures_ref = msm.get(molsys_ref, element='system', n_molecules=True, n_structures=True)
    assert n_molecules==n_molecules_ref
    assert n_structures==n_structures_ref
    assert 'nglview.NGLWidget'==msm.get_form(molsys)

# Selection

## Multiple outputs

