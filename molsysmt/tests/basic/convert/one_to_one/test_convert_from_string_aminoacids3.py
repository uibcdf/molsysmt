"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.systems import tests as tests_systems
import numpy as np
import os

# Whole systems (selection='all' and structure_indices='all')

def test_string_aminoacids3_to_string_aminoacids3_1():

    molsys = msm.convert('aminoacids3:AlaValPro', to_form='string:aminoacids3')
    check = (molsys == 'aminoacids3:AlaValPro')
    assert check

def test_string_aminoacids3_to_string_aminoacids3_2():

    molsys = msm.convert('AlaValPro', to_form='string:aminoacids3')
    check = (molsys == 'AlaValPro')
    assert check

# Selection


## Multiple outputs



