"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import os

# Whole systems (selection='all' and frame_indices='all')

# Selection

## Multiple outputs

def file_h5_to_molsysmt_Topology_and_molsysmt_Trajectory():
    molsys = msm.demo.files['pentalanine.h5']
    molsys = msm.convert(molsys, to_form=['molsysmt.Topology', 'molsysmt.Trajectory'])
    form = msm.get_form(molsys)
    assert ['molsysmt.Topology', 'molsysmt.Trajectory']==form

