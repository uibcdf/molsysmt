"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import os

# Whole systems (selection='all' and frame_indices='all')

def test_file_msmpk_to_molsysmt_MolSys():
    molsys = msm.demo.files['T4_Lysozyme_L99A_in_pdbid_181l.msmpk']
    molsys = msm.convert(molsys, to_form='molsysmt.MolSys')
    check_form = ('molsysmt.MolSys'==msm.get_form(molsys))
    assert check_form

def test_file_msmpk_to_nglview_NGLWidget():
    molsys = msm.demo.files['T4_Lysozyme_L99A_in_pdbid_181l.msmpk']
    molsys_ref = msm.convert(molsys, to_form='molsysmt.MolSys')
    molsys = msm.convert(molsys, to_form='nglview.NGLWidget')
    check_form = ('nglview.NGLWidget'==msm.get_form(molsys))
    check_n_elements = msm.compare(molsys, molsys_ref, comparison='n_elements')
    check_n_molecules = msm.compare(molsys, molsys_ref, comparison='n_molecules')
    check_n_frames =msm.compare(molsys, molsys_ref, comparison='n_frames')
    assert check_form and check_n_elements and check_n_molecules and check_n_frames

# Selection

## Multiple outputs

