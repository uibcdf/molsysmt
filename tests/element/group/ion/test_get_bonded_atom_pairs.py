"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

def test_get_bonded_atom_pairs1():

    pairs = msm.element.group.ion.get_bonded_atom_pairs('NH4', ['N', 'HN1', 'HN2', 'HN3', 'HN4']) 

    assert pairs == [[0, 1], [0, 2], [0, 3], [0, 4]]


def test_get_bonded_atom_pairs2():

    pairs = msm.element.group.ion.get_bonded_atom_pairs('NH4', ['N', 'HN1', 'HN2', 'HN3', 'HN4'],
                                                       atom_indices=[10,11,12,13,14]) 

    assert pairs == [[10, 11], [10, 12], [10, 13], [10, 14]]


def test_get_bonded_atom_pairs3():

    pairs = msm.element.group.ion.get_bonded_atom_pairs('K', 'K') 

    assert len(pairs)==0


