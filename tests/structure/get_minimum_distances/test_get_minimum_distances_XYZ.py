"""
Unit and regression test for the get_mininum_distances module of the molsysmt package on XYZ molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np

# Distance between atoms in space and time

def test_get_minimum_distances_from_XYZ_1():
    molsys = msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')
    min_pairs, min_distances = msm.structure.get_minimum_distances(molsys)
    check_shape_1 = ((3,2)==min_pairs.shape)
    check_shape_2 = ((3,)==min_distances.shape)
    check_pairs = np.all(min_pairs==np.array([[0, 0], [0, 0], [0, 0]]))
    check_distance = np.isclose(puw.get_value(min_distances[2], to_unit='nm'), 0.0)
    assert check_shape_1 and check_shape_2 and check_pairs and check_distance

def test_get_minimum_distances_from_XYZ_2():
    molsys = msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')
    min_pairs, min_distances = msm.structure.get_minimum_distances(molsys, selection=[0,1,2], selection_2=[0,1,2],
                                               structure_indices=[0,1], structure_indices_2=[1,2], pairs=True)
    check_shape_1 = ((2,)==min_pairs.shape)
    check_shape_2 = ((2,)==min_distances.shape)
    check_distance = np.isclose(puw.get_value(min_distances[1], to_unit='nm'), 1.0)
    assert check_shape_1 and check_shape_2 and check_distance

def test_get_minimum_distances_from_XYZ_3():
    molsys = msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')
    min_pairs, min_distances = msm.structure.get_minimum_distances(molsys, selection=[1,2], structure_indices=[0,1,2],
                                                selection_2=[0,1], as_entity=False, as_entity_2=True)
    check_shape_1 = ((3,2)==min_pairs.shape)
    check_shape_2 = ((3,2)==min_distances.shape)
    check_distance = np.isclose(puw.get_value(min_distances[1,0], to_unit='nm'), 0.0)
    assert check_shape_1 and check_shape_2 and check_distance

