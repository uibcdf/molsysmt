"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import os

# Whole systems (selection='all' and frame_indices='all')

def test_string_pdbid_to_molsysmt_MolSys():
    molsys_ref = msm.demo.classes.T4_Lysozyme_L99A_in_pdbid_181l(to_form='molsysmt.MolSys')
    molsys = msm.convert('pdbid:181l', to_form='molsysmt.MolSys')
    output = msm.compare(molsys, molsys_ref, comparison='all', rule='A_eq_B')
    assert output == True

def test_string_pdbid_to_molsysmt_MolSys_2():
    molsys = msm.convert('pdbid:1tcd', to_form='molsysmt.MolSys')
    form = msm.get_form(molsys)
    assert 'molsysmt.MolSys'==form

def test_string_pdbid_to_file_pdb():
    molsys = msm.convert('pdbid:1sux', to_form='1sux.pdb')
    form = msm.get_form(molsys)
    os.remove(molsys)
    assert 'file:pdb'==form

def test_string_pdbid_to_file_mmtf():
    molsys = msm.convert('pdbid:1sux', to_form='1sux.mmtf')
    form = msm.get_form(molsys)
    os.remove(molsys)
    assert 'file:mmtf'==form

def test_string_pdbid_to_mdtraj_Trajectory():
    molsys = msm.convert('pdbid:1sux', to_form='mdtraj.Trajectory')
    form = msm.get_form(molsys)
    assert 'mdtraj.Trajectory'==form

# Selection


## Multiple outputs



