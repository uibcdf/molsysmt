"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

def test_is_amino_acid():

    assert msm.element.group.amino_acid.is_amino_acid('ALA')
    assert msm.element.group.amino_acid.is_amino_acid('VAL')
    assert msm.element.group.amino_acid.is_amino_acid('ILE')
    assert msm.element.group.amino_acid.is_amino_acid('papa')==False
