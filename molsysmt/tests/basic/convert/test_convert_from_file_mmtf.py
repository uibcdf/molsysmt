"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import os

# Whole systems (selection='all' and frame_indices='all')

def test_file_mmtf_to_molsysmt_MolSys_1():
    molsys = msm.demo.t4_lysozyme_L99A['181l.mmtf']
    molsys = msm.convert(molsys, to_form='molsysmt.MolSys')
    form = msm.get_form(molsys)
    assert 'molsysmt.MolSys'==form

def test_file_mmtf_to_molsysmt_MolSys_2():
    molsys = msm.demo.villin_HP35['1vii.mmtf']
    molsys = msm.convert(molsys, to_form='molsysmt.MolSys')
    form = msm.get_form(molsys)
    assert 'molsysmt.MolSys'==form

#def test_file_mmtf_to_string_aminoacids1():
#    molsys = msm.demo.t4_lysozyme_L99A['181l.mmtf']
#    molsys = msm.convert(molsys, to_form='string:aminoacids1')
#    form = msm.get_form(molsys)
#    assert 'string:aminoacids1'==form


# Selection

## Multiple outputs


