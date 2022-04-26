"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import os

# Whole systems (selection='all' and structure_indices='all')

# Selection

## Multiple outputs

def test_file_h5_to_molsysmt_Topology_and_molsysmt_Structures():
    molsys = msm.demo['pentalanine']['traj.h5']
    molsys = msm.convert(molsys, to_form=['molsysmt.Topology', 'molsysmt.Trajectory'])
    form = msm.get_form(molsys)
    assert ['molsysmt.Topology', 'molsysmt.Trajectory']==form

