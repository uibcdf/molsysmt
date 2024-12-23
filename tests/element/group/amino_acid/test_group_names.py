"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

def test_group_names():

    assert list == type(msm.element.group.amino_acid.group_names)
    assert 'ALA' in msm.element.group.amino_acid.group_names
    assert 'ILE' in msm.element.group.amino_acid.group_names
    assert 'papa' not in msm.element.group.amino_acid.group_names
