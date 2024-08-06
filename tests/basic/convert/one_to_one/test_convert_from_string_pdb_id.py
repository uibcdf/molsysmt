"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np
import os

# Whole systems (selection='all' and structure_indices='all')

def test_string_pdb_id_to_molsysmt_MolSys_1():
    molsys = msm.convert('pdb_id:181l', to_form='molsysmt.MolSys')
    form = msm.get_form(molsys)
    assert 'molsysmt.MolSys'==form

def test_string_pdb_id_to_molsysmt_MolSys_2():
    molsys = msm.convert('181l', selection='molecule_type=="protein"')
    form = msm.get_form(molsys)
    is_only_protein = msm.is_composed_of(molsys, n_proteins=1)
    assert 'molsysmt.MolSys'==form and is_only_protein==True

def test_string_pdb_id_to_file_pdb():
    molsys = msm.convert('pdb_id:181l', to_form='181l.pdb')
    form = msm.get_form(molsys)
    os.remove(molsys)
    assert 'file:pdb'==form

def test_string_pdb_id_to_file_bcif():
    molsys = msm.convert('pdb_id:181l', to_form='181l.bcif')
    form = msm.get_form(molsys)
    os.remove(molsys)
    assert 'file:bcif'==form

def test_string_pdb_id_to_file_bcif_gz():
    molsys = msm.convert('pdb_id:181l', to_form='181l.bcif.gz')
    form = msm.get_form(molsys)
    os.remove(molsys)
    assert 'file:bcif.gz'==form

def test_string_pdb_id_to_mdtraj_Trajectory():
    molsys = msm.convert('pdb_id:181l', to_form='mdtraj.Trajectory')
    form = msm.get_form(molsys)
    assert 'mdtraj.Trajectory'==form

# Selection


## Multiple outputs



