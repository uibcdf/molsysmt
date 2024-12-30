"""
Unit and regression test for the get_distances module of the molsysmt package on XYZ molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np

# Distance between atoms in space and time

def test_get_distances_from_XYZ_1():
    molsys = msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')
    distances = msm.structure.get_distances(molsys)
    check_shape = ((3,4,4)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[1,0,2], to_unit='nm'), 3.741657)
    assert check_shape and check_distance

def test_get_distances_from_XYZ_2():
    molsys = msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=0, selection_2=2)
    check_shape = ((3,1,1)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[2,0,0], to_unit='nm'), 1.7320508)
    assert check_shape and check_distance

def test_get_distances_from_XYZ_3():
    molsys = msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=1, selection_2=[0,2])
    check_shape = ((3,1,2)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[0,0,1], to_unit='nm'), 1.41421356)
    assert check_shape and check_distance

def test_get_distances_from_XYZ_4():
    molsys = msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=1, selection_2=[0,2], structure_indices=[1,2])
    check_distance = np.isclose(puw.get_value(distances[1,0,1], to_unit='nm'), 1.73205080)
    assert check_distance

def test_get_distances_from_XYZ_5():
    molsys = msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=[1,2], structure_indices=[0,1], selection_2=1, structure_indices_2=[1,2])
    check_distance = np.isclose(puw.get_value(distances[1,1,0], to_unit='nm'), 2.2360679)
    assert check_distance

def test_get_distances_from_XYZ_6():
    molsys = msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=1, structure_indices=[0,1], structure_indices_2=[1,2])
    check_shape = ((2,1,1)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[0,0,0], to_unit='nm'), 1.0)
    assert check_shape and check_distance

def test_get_distances_from_XYZ_7():
    molsys = msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=[0,0,1], selection_2=[1,2,2],
                         structure_indices=[1,2], pairs=True)
    check_shape = ((2,3)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[0,1], to_unit='nm'), 3.741657)
    assert check_shape and check_distance

def test_get_distances_from_XYZ_8():
    molsys = msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=[[0,1],[0,2],[1,2]],
                         structure_indices=[1,2], pairs=True)
    good_distances = np.array([[3.46410162, 3.74165739, 1.41421356], [2.82842712, 1.73205081, 1.73205081]])
    assert np.allclose(puw.get_value(distances), good_distances)

def test_get_distances_from_XYZ_9():
    molsys = msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')
    indices1, indices2, distances = msm.structure.get_distances(molsys, selection=[0,0,2], selection_2=[1,1,3], structure_indices=[1,2],
                                                 output_indices='selection')
    good_distances = np.array([[[3.46410162, 3.46410162, 2.44948974],
                                [3.46410162, 3.46410162, 2.44948974],
                                [1.41421356, 1.41421356, 2.        ]],
                               [[2.82842712, 2.82842712, 3.60555128],
                                [2.82842712, 2.82842712, 3.60555128],
                                [1.73205081, 1.73205081, 3.74165739]]])
    assert np.allclose(puw.get_value(distances), good_distances)
    assert indices1 == [0,1,2]
    assert indices2 == [0,1,2]

def test_get_distances_from_XYZ_10():
    molsys = msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')
    indices1, indices2, distances = msm.structure.get_distances(molsys, selection=[0,0,2], selection_2=[1,1,3], structure_indices=[1,2],
                                                 output_indices='atom')
    good_distances = np.array([[[3.46410162, 3.46410162, 2.44948974],
                                [3.46410162, 3.46410162, 2.44948974],
                                [1.41421356, 1.41421356, 2.        ]],
                               [[2.82842712, 2.82842712, 3.60555128],
                                [2.82842712, 2.82842712, 3.60555128],
                                [1.73205081, 1.73205081, 3.74165739]]])
    assert np.allclose(puw.get_value(distances), good_distances)
    assert indices1 == [0,0,2]
    assert indices2 == [1,1,3]

def test_get_distances_from_XYZ_11():
    molsys = msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')
    ind1, ind2, sind1, sind2, distances = msm.structure.get_distances(molsys, selection=[0,0,2], selection_2=[1,1,3],
                                                                structure_indices=[0,1], structure_indices_2=[1,2],
                                                                output_indices='selection', output_structure_indices='selection')
    good_distances = np.array([[[3.        , 3.        , 2.23606798],
                                [3.        , 3.        , 2.23606798],
                                [1.        , 1.        , 2.23606798]],
                               [[3.        , 3.        , 3.16227766],
                                [3.        , 3.        , 3.16227766],
                                [2.23606798, 2.23606798, 4.89897949]]])
    assert np.allclose(puw.get_value(distances), good_distances)
    assert ind1 == [0,1,2]
    assert ind2 == [0,1,2]
    assert sind1 == [0,1]
    assert sind2 == [0,1]

def test_get_distances_from_XYZ_12():
    molsys = msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')
    ind1, ind2, sind1, sind2, distances = msm.structure.get_distances(molsys, selection=[0,0,2], selection_2=[1,1,3],
                                                                structure_indices=[0,1], structure_indices_2=[1,2],
                                                                output_indices='atom', output_structure_indices='structure')
    good_distances = np.array([[[3.        , 3.        , 2.23606798],
                                [3.        , 3.        , 2.23606798],
                                [1.        , 1.        , 2.23606798]],
                               [[3.        , 3.        , 3.16227766],
                                [3.        , 3.        , 3.16227766],
                                [2.23606798, 2.23606798, 4.89897949]]])
    assert np.allclose(puw.get_value(distances), good_distances)
    assert ind1 == [0,0,2]
    assert ind2 == [1,1,3]
    assert sind1 == [0,1]
    assert sind2 == [1,2]

def test_get_distances_from_XYZ_13():
    molsys = msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=[0,1,2], selection_2=[1,2,3],
                                            structure_indices=[0,1],
                                            output_indices='atom', output_structure_indices='structure',
                                            output_type='dictionary')
    assert list(distances.keys()) == [0,1,2]
    assert list(distances[0].keys()) == [1,2,3]
    assert list(distances[0][1].keys()) == [0,1]
    assert np.isclose(puw.get_value(distances[1][1][0]), 0.0)
    assert np.isclose(puw.get_value(distances[1][1][1]), 0.0)

def test_get_distances_from_XYZ_14():
    molsys = msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=[0,1,2], selection_2=[1,2,3],
                                            structure_indices=[0,1], structure_indices_2=[1,2],
                                            output_indices='atom', output_structure_indices='structure',
                                            output_type='dictionary')
    assert list(distances.keys()) == [0,1,2]
    assert list(distances[0].keys()) == [1,2,3]
    assert list(distances[0][1].keys()) == [0,1]
    assert list(distances[0][1][0].keys()) == [1]
    assert list(distances[0][1][1].keys()) == [2]
    assert np.isclose(puw.get_value(distances[0][1][0][1]), 3.0)
    assert np.isclose(puw.get_value(distances[0][1][1][2]), 3.0)

def test_get_distances_from_XYZ_15():
    molsys = msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=[0,1,2], selection_2=[1,2,3],
                                            structure_indices=[0,1], structure_indices_2=[1,2],
                                            output_indices='selection', output_structure_indices='selection',
                                            output_type='dictionary')
    assert list(distances.keys()) == [0,1,2]
    assert list(distances[0].keys()) == [0,1,2]
    assert list(distances[0][0].keys()) == [0,1]
    assert list(distances[0][0][0].keys()) == [0]
    assert list(distances[0][0][1].keys()) == [1]
    assert np.isclose(puw.get_value(distances[0][0][0][0]), 3.0)
    assert np.isclose(puw.get_value(distances[0][0][1][1]), 3.0)

def test_get_distances_from_XYZ_16():
    molsys = msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=[0,1,2], selection_2=[1,2,3],
                                            structure_indices=[0,1],
                                            output_indices='atom', pairs=True,
                                            output_type='dictionary')
    assert list(distances.keys()) == [0,1,2]
    assert list(distances[0].keys()) == [1]
    assert list(distances[1].keys()) == [2]
    assert list(distances[2].keys()) == [3]
    assert np.allclose(puw.get_value(distances[0][1]), np.array([2.44948974, 3.46410162]))

def test_get_distances_from_XYZ_17():
    molsys = msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=[0,1,2], selection_2=[1,2,3],
                                            structure_indices=[0,1],
                                            output_indices='selection', pairs=True,
                                            output_type='dictionary')
    assert list(distances.keys()) == [0,1,2]
    assert np.allclose(puw.get_value(distances[0]), np.array([2.44948974, 3.46410162]))

