"""
Unit and regression test for the get_distances module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np

# Distances between atoms in space and time

def test_get_distances_from_molsysmt_MolSys_1():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    distances = msm.structure.get_distances(molsys, selection="group_index==0", selection_2="group_index==1")
    check_shape = ((1,9,7)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[0,5,5], to_unit='nm'), 0.5271685)
    assert check_shape and check_distance


# Distances between atom groups

def test_get_distances_from_molsysmt_MolSys_groups_1():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    distances = msm.structure.get_distances(molsys, selection="group_index==0",
                         center_of_atoms=True, selection_2="group_index==1")
    check_shape = ((1,1,7)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[0, 0, 4], to_unit='nm'), 0.5724921)
    assert check_shape and check_distance

def test_get_distances_from_molsysmt_MolSys_groups_2():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    distances = msm.structure.get_distances(molsys, selection="group_index==0",
            center_of_atoms=True, selection_2="group_index==1", center_of_atoms_2=True)
    check_shape = ((1,1,1)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[0, 0, 0], to_unit='nm'), 0.43703472)
    assert check_shape and check_distance

def test_get_distances_from_molsysmt_MolSys_groups_3():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    list_groups_2 = msm.get(molsys, element="group", selection="group_index in [4,5,6,7,8]", atom_index=True)
    distances = msm.structure.get_distances(molsys, selection="group_index==0",
                         selection_2=list_groups_2, center_of_atoms_2=True)
    check_shape = ((1,9,5)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[0, 3, 3], to_unit='nm'), 2.070343)
    assert check_shape and check_distance

def test_get_distances_from_molsysmt_MolSys_groups_4():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    list_groups_1 = msm.get(molsys, element="group", selection="group_index in [0,1,2,3]", atom_index=True)
    list_groups_2 = msm.get(molsys, element="group", selection="group_index in [4,5,6,7,8]", atom_index=True)
    distances = msm.structure.get_distances(molsys, selection="group_index==0",
            center_of_atoms=True, selection_2=list_groups_2, center_of_atoms_2=True)
    check_shape = ((1,1,5)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[0, 0, 4], to_unit='nm'), 2.291778)
    assert check_shape and check_distance

def test_get_distances_from_molsysmt_MolSys_groups_5():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    list_groups_1 = msm.get(molsys, element="group", selection="group_index in [0,1,2,3]", atom_index=True)
    list_groups_2 = msm.get(molsys, element="group", selection="group_index in [4,5,6,7,8]", atom_index=True)
    distances = msm.structure.get_distances(molsys, selection=list_groups_1, center_of_atoms=True,
                         selection_2=list_groups_2, center_of_atoms_2=True)
    check_shape = ((1,4,5)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[0, 2, 2], to_unit='nm'), 1.240669)
    assert check_shape and check_distance

def test_get_distances_from_molsysmt_MolSys_groups_6():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    list_groups_1 = msm.get(molsys, element="group", selection="group_index in [0,1,2,3]", atom_index=True)
    list_groups_2 = msm.get(molsys, element="group", selection="group_index in [4,5,6,7,8]", atom_index=True)
    distances = msm.structure.get_distances(molsys, selection=list_groups_1, center_of_atoms=True)
    check_shape = ((1,4,4)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[0, 2, 3], to_unit='nm'), 0.386833)
    assert check_shape and check_distance

def test_get_distances_from_molsysmt_MolSys_groups_7():
    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    distances = msm.structure.get_distances(molsys, selection="group_index==0",
            center_of_atoms=True, selection_2="group_index==6", center_of_atoms_2=True)
    check_shape = ((5000,1,1)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[1000, 0, 0], to_unit='nm'), 0.818624)
    assert check_shape and check_distance

def test_get_distances_from_molsysmt_MolSys_groups_8():
    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    list_groups_1 = msm.get(molsys, element="group", selection="all", atom_index=True)
    distances = msm.structure.get_distances(molsys, selection=list_groups_1, center_of_atoms=True,
                         structure_indices=3000)
    check_shape = ((1,7,7)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[0, 2, 4], to_unit='nm'), 0.681850)
    assert check_shape and check_distance

def test_get_distances_from_molsysmt_MolSys_groups_9():
    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    distances = msm.structure.get_distances(molsys,
                         selection="group_index==0", center_of_atoms=True,
                         structure_indices=100,
                         selection_2="group_index==6", center_of_atoms_2=True,
                         structure_indices_2=200)
    check_shape = ((1,1,1)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[0, 0, 0], to_unit='nm'), 0.5978502)
    assert check_shape and check_distance

def test_get_distances_from_molsysmt_MolSys_groups_10():
    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    n_structures = msm.get(molsys, n_structures=True)
    all_structure_indices = np.arange(n_structures)
    displacements = msm.structure.get_distances(molsys, selection="group_index==0",
            center_of_atoms=True, structure_indices=all_structure_indices[:-1], structure_indices_2=all_structure_indices[1:])
    check_shape = ((4999,1,6)==displacements.shape)
    check_distance = np.isclose(puw.get_value(displacements[1000, 0, 3], to_unit='nm'), 0.84082184)
    assert check_shape and check_distance

def test_get_distances_from_molsysmt_MolSys_groups_11():
    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    n_structures = msm.get(molsys, n_structures=True)
    all_structure_indices = np.arange(n_structures)
    displacements = msm.structure.get_distances(molsys, selection="all",
                             structure_indices=np.zeros(n_structures, dtype=int), structure_indices_2=all_structure_indices)
    check_shape = ((5000,62,62)==displacements.shape)
    check_distance = np.isclose(puw.get_value(displacements[1000, 30, 30], to_unit='nm'), 0.4517681)
    assert check_shape and check_distance

def test_get_distances_from_molsysmt_MolSys_groups_12():
    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    list_atom_groups = msm.get(molsys, element='group', selection='all', atom_index=True)
    distances = msm.structure.get_distances(molsys, selection=list_atom_groups, center_of_atoms=True)
    check_shape = ((5000,7,7)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[1000, 2, 3], to_unit='nm'), 0.4240467)
    assert check_shape and check_distance

def test_get_distances_from_molsysmt_MolSys_groups_13():
    from itertools import combinations
    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    list_atom_groups = msm.get(molsys, element='group', selection='all', atom_index=True)
    list_atom_groups_1=[]
    list_atom_groups_2=[]
    aux_list_1=[]
    aux_list_2=[]
    for ii,jj in combinations(range(7), 2):
        aux_list_1.append(ii)
        aux_list_2.append(jj)
        list_atom_groups_1.append(list_atom_groups[ii])
        list_atom_groups_2.append(list_atom_groups[jj])
    distances = msm.structure.get_distances(molsys, selection=list_atom_groups_1, center_of_atoms=True,
                         selection_2=list_atom_groups_2, center_of_atoms_2=True, pairs=True)
    check_shape = ((5000, 21)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[1000, 12], to_unit='nm'), 0.69240215)
    assert check_shape and check_distance

