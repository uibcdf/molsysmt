"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import os

# Whole systems (selection='all' and frame_indices='all')

def test_file_mmtf_to_string_aminoacids1():
    molsys = msm.demo.files['1tcd.mmtf']
    molsys = msm.convert(molsys, to_form='string:aminoacids1')
    form = msm.get_form(molsys)
    assert 'string:aminoacids1'==form

def test_file_mmtf_to_molsysmt_MolSys():
    molsys = msm.demo.files['1tcd.mmtf']
    molsys = msm.convert(molsys, to_form='molsysmt.MolSys')
    form = msm.get_form(molsys)
    assert 'molsysmt.MolSys'==form

# Selection

## Multiple outputs


