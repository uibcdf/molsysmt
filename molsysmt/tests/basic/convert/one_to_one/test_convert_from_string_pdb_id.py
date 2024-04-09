"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np
import os

# Whole systems (selection='all' and structure_indices='all')

def test_string_pdb_id_to_molsysmt_MolSys():
    molsys = msm.convert('pdb_id:181l', to_form='molsysmt.MolSys')
    form = msm.get_form(molsys)
    assert 'molsysmt.MolSys'==form

def test_string_pdb_id_to_file_pdb():
    molsys = msm.convert('pdb_id:181l', to_form='181l.pdb')
    form = msm.get_form(molsys)
    os.remove(molsys)
    assert 'file:pdb'==form

def test_string_pdb_id_to_file_mmtf():
    molsys = msm.convert('pdb_id:181l', to_form='181l.mmtf')
    form = msm.get_form(molsys)
    os.remove(molsys)
    assert 'file:mmtf'==form

def test_string_pdb_id_to_mdtraj_Trajectory():
    molsys = msm.convert('pdb_id:181l', to_form='mdtraj.Trajectory')
    form = msm.get_form(molsys)
    assert 'mdtraj.Trajectory'==form

# Selection


## Multiple outputs



