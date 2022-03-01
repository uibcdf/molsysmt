"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import os

# Whole systems (selection='all' and structure_indices='all')

def test_file_xyznpy_to_XYZ():
    molsys = msm.demo['4 particles']['traj.xyznpy']
    molsys = msm.convert(molsys, to_form='XYZ')
    check_form = ('XYZ'==msm.get_form(molsys))
    assert check_form

# Selection

## Multiple outputs

