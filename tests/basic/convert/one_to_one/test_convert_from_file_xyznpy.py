"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np
import os

# Whole systems (selection='all' and structure_indices='all')

def test_file_xyznpy_to_XYZ():
    molsys = systems['particles 4']['traj_particles_4.xyznpy']
    molsys = msm.convert(molsys, to_form='XYZ')
    check = ('XYZ'==msm.get_form(molsys))
    assert check

# Selection

## Multiple outputs

