"""
Unit and regression test for the get_distances module of the molsysmt package on XYZ molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import puw
import numpy as np

# Distance between atoms in space and time

def test_get_distances_from_XYZ_1():
    molsys = msm.demo.classes.particles_4_frames_3(to_form='XYZ')
    distances = msm.structure.get_distances(molsys)
    check_shape = ((3,4,4)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[1,0,2], to_unit='nm'), 3.741657)
    assert check_shape and check_distance

def test_get_distances_from_XYZ_2():
    molsys = msm.demo.classes.particles_4_frames_3(to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=0, selection_2=2)
    check_shape = ((3,1,1)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[2,0,0], to_unit='nm'), 1.7320508)
    assert check_shape and check_distance

def test_get_distances_from_XYZ_3():
    molsys = msm.demo.classes.particles_4_frames_3(to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=1, selection_2=[0,2])
    check_shape = ((3,1,2)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[0,0,1], to_unit='nm'), 1.41421356)
    assert check_shape and check_distance

def test_get_distances_from_XYZ_4():
    molsys = msm.demo.classes.particles_4_frames_3(to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=1, selection_2=[0,2], output_form='dict')
    check_form = (type(distances)==dict)
    check_distance = np.isclose(puw.get_value(distances[1][2][0], to_unit='nm'), 1.41421356)
    assert check_form and check_distance

def test_get_distances_from_XYZ_5():
    molsys = msm.demo.classes.particles_4_frames_3(to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=1, selection_2=[0,2], frame_indices=[1,2])
    check_distance = np.isclose(puw.get_value(distances[1,0,1], to_unit='nm'), 1.73205080)
    assert check_distance

def test_get_distances_from_XYZ_6():
    molsys = msm.demo.classes.particles_4_frames_3(to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=1, selection_2=[0,2], frame_indices=[1,2], output_form='dict')
    check_distance = np.isclose(puw.get_value(distances[1][2][2], to_unit='nm'), 1.73205080)
    assert check_distance

def test_get_distances_from_XYZ_7():
    molsys = msm.demo.classes.particles_4_frames_3(to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=[1,2], frame_indices=[0,1], selection_2=1, frame_indices_2=[1,2])
    check_distance = np.isclose(puw.get_value(distances[1,1,0], to_unit='nm'), 2.2360679)
    assert check_distance

def test_get_distances_from_XYZ_8():
    molsys = msm.demo.classes.particles_4_frames_3(to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=[1,2], frame_indices=[0,1],
                         selection_2=1, frame_indices_2=[1,2], output_form='dict')
    check_distance = np.isclose(puw.get_value(distances[2][1][1], to_unit='nm'), 2.2360679)
    assert check_distance

def test_get_distances_from_XYZ_9():
    molsys = msm.demo.classes.particles_4_frames_3(to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=1, frame_indices=[0,1], frame_indices_2=[1,2])
    check_shape = ((2,1,1)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[0,0,0], to_unit='nm'), 1.0)
    assert check_shape and check_distance

def test_get_distances_from_XYZ_10():
    molsys = msm.demo.classes.particles_4_frames_3(to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=1, frame_indices=[0,1,2], frame_indices_2=[0,0,0],
                         output_form='dict')
    check_distance = np.isclose(puw.get_value(distances[1][1][1], to_unit='nm'), 1.0)
    assert check_distance

def test_get_distances_from_XYZ_10():
    molsys = msm.demo.classes.particles_4_frames_3(to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=[0,0,1], selection_2=[1,2,2],
                         frame_indices=[1,2], pairs=True)
    check_shape = ((2,3)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[0,1], to_unit='nm'), 3.741657)
    assert check_shape and check_distance

def test_get_distances_from_XYZ_11():
    molsys = msm.demo.classes.particles_4_frames_3(to_form='XYZ')
    distances = msm.structure.get_distances(molsys, selection=[0,0,1], selection_2=[1,2,2],
                         frame_indices=[1,2], pairs=True, output_form='dict')
    check_distance = np.isclose(puw.get_value(distances[0][2][1], to_unit='nm'), 3.741657)
    assert check_distance

