"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import os

# Whole systems (selection='all' and structure_indices='all')

def test_file_msmpk_to_molsysmt_MolSys():
    molsys = msm.demo['T4 lysozyme L99A']['vacuum.msmpk']
    molsys = msm.convert(molsys, to_form='molsysmt.MolSys')
    check = ('molsysmt.MolSys'==msm.get_form(molsys))
    assert check

def test_file_msmpk_to_nglview_NGLWidget():
    molsys = msm.demo['T4 lysozyme L99A']['vacuum.msmpk']
    molsys_ref = msm.convert(molsys, to_form='molsysmt.MolSys')
    molsys = msm.convert(molsys, to_form='nglview.NGLWidget')
    check = ('nglview.NGLWidget'==msm.get_form(molsys))
    check_n_molecules = msm.compare(molsys, molsys_ref, comparison='n_molecules')
    check_n_structures = msm.compare(molsys, molsys_ref, comparison='n_structures')
    assert check and check_n_molecules and check_n_structures

# Selection

## Multiple outputs

