"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

def test_get_bonded_atom_pairs1():

    atom_names = ['N','CA','C','O','CB','CG1','CG2','OXT','H','HN2','HA','HB',
                  '1HG1','2HG1','3HG1','1HG2','2HG2','3HG2','HXT']
    pairs = msm.element.group.amino_acid.get_bonded_atom_pairs('VAL', atom_names)

    good_pairs = [[0, 1], [0, 8], [0, 9], [1, 2], [1, 4], [1, 10], [2, 3],
                  [2, 7], [4, 5], [4, 6], [4, 11], [5, 12], [5, 13], [5, 14],
                  [6, 15], [6, 16], [6, 17], [7, 18]]

    assert pairs == good_pairs

def test_get_bonded_atom_pairs2():

    atom_names = ['N','CA','C','O','CB','CG1','CG2','OXT','H','HN2','HA','HB',
                  '1HG1','2HG1','3HG1','1HG2','2HG2','3HG2','HXT']
    atom_indices = list(range(10, 10+len(atom_names)))
    pairs = msm.element.group.amino_acid.get_bonded_atom_pairs('VAL', atom_names, atom_indices=atom_indices)

    good_pairs = [[10, 11], [10, 18], [10, 19], [11, 12], [11, 14], [11, 20],
                  [12, 13], [12, 17], [14, 15], [14, 16], [14, 21], [15, 22],
                  [15, 23], [15, 24], [16, 25], [16, 26], [16, 27], [17, 28]]

    assert pairs == good_pairs

def test_get_bonded_atom_pairs3():

    atom_names = ['N','CA','C','O','CB','CG','ND1','CD2','CE1','NE2','OXT']
    pairs = msm.element.group.amino_acid.get_bonded_atom_pairs('HIS', atom_names)

    good_pairs = [[0, 1], [1, 2], [1, 4], [2, 3], [2, 10], [4, 5], [5, 6],
                  [5, 7], [6, 8], [7, 9], [8, 9]]

    assert pairs == good_pairs




