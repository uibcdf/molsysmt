"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import os

# Whole systems (selection='all' and frame_indices='all')

def test_file_gro_to_mdtraj_Trajectory():
    import warnings
    warnings.filterwarnings('ignore')
    molsys = msm.demo.files['nglview_demo_md_1u19.gro']
    molsys = msm.convert(molsys, to_form='mdtraj.Trajectory')
    warnings.resetwarnings()
    form = msm.get_form(molsys)
    assert 'mdtraj.Trajectory'==form

# Selection

## Multiple outputs


