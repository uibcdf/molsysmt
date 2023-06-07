"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.systems import tests as tests_systems
import numpy as np
import os

# Whole systems (selection='all' and structure_indices='all')

def test_file_pdb_to_mdtraj_Trajectory():
    molsys = tests_systems['T4 lysozyme L99A']['181l.pdb']
    molsys = msm.convert(molsys, to_form='mdtraj.Trajectory')
    form = msm.get_form(molsys)
    assert 'mdtraj.Trajectory'==form

def test_file_pdb_to_openmm_Topology():
    molsys = tests_systems['T4 lysozyme L99A']['181l.pdb']
    molsys = msm.convert(molsys, to_form='openmm.Topology')
    form = msm.get_form(molsys)
    assert 'openmm.Topology'==form

def test_file_pdb_to_string_pdb_text():
    molsys = tests_systems['T4 lysozyme L99A']['181l.pdb']
    molsys = msm.convert(molsys, to_form='string:pdb_text')
    form = msm.get_form(molsys)
    assert 'string:pdb_text'==form

def test_file_pdb_to_pdbfixer_PDBFixer():
    molsys = tests_systems['T4 lysozyme L99A']['181l.pdb']
    molsys = msm.convert(molsys, to_form='pdbfixer.PDBFixer')
    form = msm.get_form(molsys)
    assert 'pdbfixer.PDBFixer'==form

def test_file_pdb_to_parmed_Structure():
    molsys = tests_systems['T4 lysozyme L99A']['181l.pdb']
    molsys = msm.convert(molsys, to_form='parmed.Structure')
    form = msm.get_form(molsys)
    assert 'parmed.Structure'==form

# Selection

## Multiple outputs


