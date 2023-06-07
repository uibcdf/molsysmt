"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.systems import tests as tests_systems
import numpy as np
import os

# Whole systems (selection='all' and structure_indices='all')

def test_file_mol2_to_openmm_Modeller():
    molsys = tests_systems['caffeine']['caffeine.mol2']
    molsys = msm.convert(molsys, to_form='openmm.Modeller')
    form = msm.get_form(molsys)
    assert 'openmm.Modeller'==form

def test_file_mol2_to_mdtraj_Trajectory():
    molsys = tests_systems['caffeine']['caffeine.mol2']
    molsys = msm.convert(molsys, to_form='mdtraj.Trajectory')
    form = msm.get_form(molsys)
    assert 'mdtraj.Trajectory'==form

# Selection

## Multiple outputs


