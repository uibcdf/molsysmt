"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np
import os

# Whole systems (selection='all' and structure_indices='all')

def test_string_amino_acids_3_to_string_amino_acids_3_1():

    molsys = msm.convert('amino_acids_3:AlaValPro', to_form='string:amino_acids_3')
    check = (molsys == 'amino_acids_3:AlaValPro')
    assert check

def test_string_amino_acids_3_to_string_amino_acids_3_2():

    molsys = msm.convert('AlaValPro', to_form='string:amino_acids_3')
    check = (molsys == 'AlaValPro')
    assert check

# Selection


## Multiple outputs



