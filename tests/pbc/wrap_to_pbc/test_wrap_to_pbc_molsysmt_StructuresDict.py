"""
Unit and regression test for the wrap_to_pbc method of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt import systems
import numpy as np

# Distance between atoms in space and time

def test_wrap_to_pbc_molsysmt_StructuresDict_1():

    coordinates = puw.quantity([[[1.0, 1.0, 1.0]]], 'nm')
    box = puw.quantity([[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]], 'nm')
    molsys = {'coordinates':coordinates, 'box':box}

    molsys = msm.pbc.wrap_to_pbc(molsys)

    assert np.allclose(puw.get_value(molsys['coordinates']), [[[1.0, 1.0, 1.0]]])
    assert np.allclose(puw.get_value(molsys['box']), [[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]])

def test_wrap_to_pbc_molsysmt_StructuresDict_2():

    coordinates = puw.quantity([[[3.0, 3.0, 3.0]]], 'nm')
    box = puw.quantity([[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]], 'nm')
    molsys = {'coordinates':coordinates, 'box':box}

    molsys = msm.pbc.wrap_to_pbc(molsys)

    assert np.allclose(puw.get_value(molsys['coordinates']), [[[1.0, 1.0, 1.0]]])
    assert np.allclose(puw.get_value(molsys['box']), [[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]])

def test_wrap_to_pbc_molsysmt_StructuresDict_3():

    coordinates = puw.quantity([[[-1.0, -1.0, -1.0]]], 'nm')
    box = puw.quantity([[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]], 'nm')
    molsys = {'coordinates':coordinates, 'box':box}

    molsys = msm.pbc.wrap_to_pbc(molsys)

    assert np.allclose(puw.get_value(molsys['coordinates']), [[[1.0, 1.0, 1.0]]])
    assert np.allclose(puw.get_value(molsys['box']), [[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]])

def test_wrap_to_pbc_molsysmt_StructuresDict_4():

    coordinates=puw.quantity([[[2.0, 2.0, 2.0]]], 'nm')
    origin=puw.quantity([1.0, 1.0, 1.0], 'nm')
    box=puw.quantity([[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]], 'nm')
    molsys = {'coordinates':coordinates, 'box':box}

    molsys = msm.pbc.wrap_to_pbc(molsys, box_origin=origin)

    assert np.allclose(puw.get_value(molsys['coordinates']), [[[2.0, 2.0, 2.0]]])
    assert np.allclose(puw.get_value(molsys['box']), [[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]])

def test_wrap_to_pbc_molsysmt_StructuresDict_5():

    coordinates=puw.quantity([[[4.0, 4.0, 4.0]]], 'nm')
    origin=puw.quantity([1.0, 1.0, 1.0], 'nm')
    box=puw.quantity([[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]], 'nm')
    molsys = {'coordinates':coordinates, 'box':box}

    molsys = msm.pbc.wrap_to_pbc(molsys, box_origin=origin)

    assert np.allclose(puw.get_value(molsys['coordinates']), [[[2.0, 2.0, 2.0]]])
    assert np.allclose(puw.get_value(molsys['box']), [[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]])

def test_wrap_to_pbc_molsysmt_StructuresDict_6():

    coordinates=puw.quantity([[[0.0, 0.0, 0.0]]], 'nm')
    origin=puw.quantity([1.0, 1.0, 1.0], 'nm')
    box=puw.quantity([[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]], 'nm')
    molsys = {'coordinates':coordinates, 'box':box}

    molsys = msm.pbc.wrap_to_pbc(molsys, box_origin=origin)

    assert np.allclose(puw.get_value(molsys['coordinates']), [[[2.0, 2.0, 2.0]]])
    assert np.allclose(puw.get_value(molsys['box']), [[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]])

def test_wrap_to_pbc_molsysmt_StructuresDict_7():

    coordinates=puw.quantity([[[1.0, 1.0, 1.0]]], 'nm')
    origin=puw.quantity([1.0, 1.0, 1.0], 'nm')
    box=puw.quantity([[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]], 'nm')
    molsys = {'coordinates':coordinates, 'box':box}

    molsys = msm.pbc.wrap_to_pbc(molsys, box_origin=origin)

    assert np.allclose(puw.get_value(molsys['coordinates']), [[[1.0, 1.0, 1.0]]])
    assert np.allclose(puw.get_value(molsys['box']), [[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]])

def test_wrap_to_pbc_molsysmt_StructuresDict_8():

    coordinates=puw.quantity([[[3.0, 3.0, 3.0]]], 'nm')
    origin=puw.quantity([1.0, 1.0, 1.0], 'nm')
    box=puw.quantity([[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]], 'nm')
    molsys = {'coordinates':coordinates, 'box':box}

    molsys = msm.pbc.wrap_to_pbc(molsys, box_origin=origin)

    assert np.allclose(puw.get_value(molsys['coordinates']), [[[1.0, 1.0, 1.0]]])
    assert np.allclose(puw.get_value(molsys['box']), [[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]])

def test_wrap_to_pbc_molsysmt_StructuresDict_9():

    coordinates=puw.quantity(np.random.uniform(-10.0, 10.0, size=(10,100,3)), 'nm')
    origin=puw.quantity([3.0, 3.0, 3.0], 'nm')
    box=puw.quantity([[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]], 'nm')
    molsys = {'coordinates':coordinates, 'box':box}

    molsys = msm.pbc.wrap_to_pbc(molsys, box_origin=origin)

    coordinates = puw.get_value(molsys['coordinates'])

    assert coordinates[:,:,0].min()>3.0
    assert coordinates[:,:,1].min()>3.0
    assert coordinates[:,:,2].min()>3.0
    assert coordinates[:,:,0].max()<5.0
    assert coordinates[:,:,1].max()<5.0
    assert coordinates[:,:,2].max()<5.0

def test_wrap_to_pbc_molsysmt_StructuresDict_10():

    origin=puw.quantity([0.0, 0.0, 0.0], 'nm')
    box=msm.pbc.get_box_with_shape(shape='rhombic dodecahedral', length='2.0 nm')
    coordinates= np.dot(box[0].T, np.array([2.0, 2.0, 2.0]))
    coordinates = coordinates.reshape(1, 1, 3)
    molsys={'coordinates':coordinates, 'box':box}

    molsys = msm.pbc.wrap_to_pbc(molsys, box_origin=origin)

    assert np.allclose(puw.get_value(molsys['coordinates']), [[[0.0, 0.0, 0.0]]])

def test_wrap_to_pbc_molsysmt_StructuresDict_11():

    origin=puw.quantity([0.0, 0.0, 0.0], 'nm')
    box=msm.pbc.get_box_with_shape(shape='rhombic dodecahedral', length='2.0 nm')
    coordinates= np.dot(box[0].T, np.array([-2.0, -2.0, -2.0]))
    coordinates = coordinates.reshape(1, 1, 3)
    molsys={'coordinates':coordinates, 'box':box}

    molsys = msm.pbc.wrap_to_pbc(molsys, box_origin=origin)

    assert np.allclose(puw.get_value(molsys['coordinates']), [[[0.0, 0.0, 0.0]]])

def test_wrap_to_pbc_molsysmt_StructuresDict_12():

    origin=puw.quantity([0.0, 0.0, 0.0], 'nm')
    box=msm.pbc.get_box_with_shape(shape='rhombic dodecahedral', length='2.0 nm')
    coordinates= np.dot(box[0].T, np.array([0.5, 0.5, 0.5]))
    coordinates = coordinates.reshape(1, 1, 3)
    molsys={'coordinates':coordinates, 'box':box}

    molsys = msm.pbc.wrap_to_pbc(molsys, box_origin=origin)

    assert np.allclose(puw.get_value(molsys['coordinates']), puw.get_value(coordinates))


def test_wrap_to_pbc_molsysmt_StructuresDict_13():

    coordinates=puw.quantity([[[0.0, 0.0, 0.0]]], 'nm')
    origin=puw.quantity([0.0, 0.0, 0.0], 'nm')
    box=msm.pbc.get_box_with_shape(shape='rhombic dodecahedral', length='2.0 nm')
    molsys={'coordinates':coordinates, 'box':box}

    molsys = msm.pbc.wrap_to_pbc(molsys, box_origin=origin)

    assert np.allclose(puw.get_value(molsys['coordinates']), [[[0.0, 0.0, 0.0]]])

def test_wrap_to_pbc_molsysmt_StructuresDict_14():

    coordinates=puw.quantity(np.random.uniform(-10.0, 10.0, size=(10,100,3)), 'nm')
    origin=puw.quantity([0.0, 0.0, 0.0], 'nm')
    box=msm.pbc.get_box_with_shape(shape='rhombic dodecahedral', length='2.0 nm')
    molsys = {'coordinates':coordinates, 'box':box}

    molsys = msm.pbc.wrap_to_pbc(molsys, box_origin=origin)

    coordinates = puw.get_value(molsys['coordinates'])
    box = puw.get_value(box)

    assert coordinates[:,:,0].min()>0.0
    assert coordinates[:,:,1].min()>0.0
    assert coordinates[:,:,2].min()>0.0
    assert coordinates[:,:,0].max()<(box[0,0,0]+box[0,1,0]+box[0,2,0])
    assert coordinates[:,:,1].max()<(box[0,0,1]+box[0,1,1]+box[0,2,1])
    assert coordinates[:,:,2].max()<(box[0,0,2]+box[0,1,2]+box[0,2,2])



#def test_wrap_to_pbc_molsysmt_StructuresDict_100():
#    molsys = msm.convert(systems['two LJ particles']['traj_two_lj_particles.trjpk'], to_form='molsysmt.StructuresDict')
#    distance = msm.structure.get_distances(molsys, selection=0, selection_2=1, pbc=True)
#    molsys_wrapped = msm.pbc.wrap_to_pbc(molsys)
#    distance_wrapped = msm.structure.get_distances(molsys_wrapped, selection=0, selection_2=1, pbc=True)
#    check_distances = np.allclose(distance[:,:,:], distance_wrapped[:,:,:])
#    box_length = msm.get(molsys_wrapped, element='system', box_lengths=True)[0,0]
#    check_limits_wrapped = ( box_length >= (np.max(molsys_wrapped['coordinates']) - np.min(molsys_wrapped['coordinates'])))
#    check_limits = ( box_length <= (np.max(molsys['coordinates']) - np.min(molsys['coordinates'])))
#    assert check_limits
#    assert check_distances
#    assert check_limits_wrapped


