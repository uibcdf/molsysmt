"""
Unit and regression test for the get_neighbors module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import pyunitwizard as puw
import numpy as np

# Distance between atoms in space and time

def test_get_neighbors_from_molsysmt_StructuresDict_1():
    coordinates = np.array([[[0.5, 4.5, 1.0],
               [2.5, 2.0, 3.0],
               [7.0, 3.5, 6.5],
               [6.5, 9.0, 2.5],
               [3.0, 4.5, 8.0]]])*puw.unit('nm')
    box = np.array([[[10.0, 0.0, 0.0],
       [0.0, 10.0, 0.0],
       [0.0, 0.0, 10.0]]])*puw.unit('nm')
    molsys = {'coordinates':coordinates, 'box':box}
    neighbors, distances = msm.structure.get_neighbors(molsys, n_neighbors=1, pbc=False)
    good_neighbors = np.array([[[1],[0],[4],[2],[2]]], dtype=int)
    good_distances = np.array([[[3.774917217635375], [3.774917217635375], [4.387482193696061],
        [6.819090848492928], [4.387482193696061]]])*puw.unit('nm')
    assert np.all(neighbors==good_neighbors)
    assert np.allclose(distances,good_distances)

def test_get_neighbors_from_molsysmt_StructuresDict_2():
    coordinates = np.array([[[0.5, 4.5, 1.0],
               [2.5, 2.0, 3.0],
               [7.0, 3.5, 6.5],
               [6.5, 9.0, 2.5],
               [3.0, 4.5, 8.0]]])*puw.unit('nm')
    box = np.array([[[10.0, 0.0, 0.0],
       [0.0, 10.0, 0.0],
       [0.0, 0.0, 10.0]]])*puw.unit('nm')
    molsys = {'coordinates':coordinates, 'box':box}
    neighbors, distances = msm.structure.get_neighbors(molsys, n_neighbors=1, pbc=True)
    good_neighbors = np.array([[[1],[0],[4],[1],[0]]], dtype=int)
    good_distances = np.array([[[3.774917217635375], [3.774917217635375], [4.387482193696061],
        [5.024937810560445], [3.905124837953327]]])*puw.unit('nm')
    assert np.all(neighbors==good_neighbors)
    assert np.allclose(distances,good_distances)




