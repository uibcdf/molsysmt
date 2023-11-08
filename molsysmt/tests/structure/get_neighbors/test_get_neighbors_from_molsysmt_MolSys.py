"""
Unit and regression test for the get_neighbors module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.systems import tests as tests_systems
from molsysmt import pyunitwizard as puw
import numpy as np

# Distance between atoms in space and time

def test_get_neighbors_from_molsysmt_MolSys_1():
    molsys = msm.convert(tests_systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    CA_atoms_list = msm.select(molsys, selection='atom_name=="CA"')
    neighbors, distances = msm.structure.get_neighbors(molsys, selection=CA_atoms_list, n_neighbors=3)
    check_shape_1 = ((5000, 5, 3)==neighbors.shape)
    check_shape_2 = ((5000, 5, 3)==distances.shape)
    check_distance = np.isclose(puw.get_value(distances[2000,0,0], to_unit='nm'), 0.38743175)
    assert check_shape_1
    assert check_shape_2
    assert check_distance

def test_get_neighbors_from_molsysmt_MolSys_2():
    molsys = msm.convert(tests_systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    CA_atoms_list = msm.select(molsys, selection='atom_name=="CA"')
    neighbors, distances = msm.structure.get_neighbors(molsys, selection=CA_atoms_list, selection_2='all', n_neighbors=4)
    check_neighbors = (10==neighbors[2000,0,3])
    check_distance = np.isclose(puw.get_value(distances[2000,0,3], to_unit='nm'), 0.1532800)
    assert check_neighbors
    assert check_distance

def test_get_neighbors_from_molsysmt_MolSys_3():
    molsys = msm.convert(tests_systems['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    atoms_in_residues_chain_0 = msm.get(molsys, element='group',
                                        selection="molecule_type=='protein' and chain_index==0", atom_index=True)
    neighbors, distances = msm.structure.get_neighbors(molsys, selection=atoms_in_residues_chain_0, n_neighbors=8)
    check_shape_1 = ((1, 248, 8)==neighbors.shape)
    check_neighbors = (2==neighbors[0,0,7])
    check_distance = np.isclose(puw.get_value(distances[0,0,7], to_unit='nm'), 0.86807833)
    assert check_shape_1
    assert check_neighbors
    assert check_distance

def test_get_neighbors_from_molsysmt_MolSys_4():
    molsys = msm.convert(tests_systems['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    atoms_in_residues_chain_0 = msm.get(molsys, element='group',
                                        selection="molecule_type=='protein' and chain_index==0", atom_index=True)
    atoms_in_residues_chain_1 = msm.get(molsys, element='group',
                                        selection="molecule_type=='protein' and chain_index==1", atom_index=True)
    neighbors, distances = msm.structure.get_neighbors(molsys,
                                     selection=atoms_in_residues_chain_0,
                                     selection_2=atoms_in_residues_chain_1,
                                     n_neighbors=8)
    check_neighbors = (17==neighbors[0,0,7])
    check_distance = np.isclose(puw.get_value(distances[0,0,7], to_unit='nm'), 3.539767)
    assert check_neighbors
    assert check_distance

def test_get_neighbors_from_molsysmt_MolSys_5():
    molsys = msm.convert(tests_systems['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    atoms_in_residues_chain_1 = msm.get(molsys, element='group',
                                        selection="molecule_type=='protein' and chain_index==1", atom_index=True)
    neighbors, distances = msm.structure.get_neighbors(molsys, selection=100,
                                     selection_2=atoms_in_residues_chain_1,
                                     n_neighbors=4)
    check_neighbors = (77==neighbors[0,0,3])
    check_distance = np.isclose(puw.get_value(distances[0,0,3], to_unit='nm'), 0.8498448)
    assert check_neighbors
    assert check_distance

def test_get_neighbors_from_molsysmt_MolSys_6():
    molsys = msm.convert(tests_systems['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    CA_atoms = msm.select(molsys, selection='atom_name=="CA"')
    neighbors, distances = msm.structure.get_neighbors(molsys, selection=CA_atoms, threshold='8 angstroms')
    check_shape_1 = ((1, 497)==neighbors.shape)
    check_shape_2 = ((1, 497)==distances.shape)
    check_neighbors = (14==len(neighbors[0,9]))
    check_neighbors_2 = (21==neighbors[0, 20][0])
    check_distance = np.isclose(puw.get_value(distances[0, 20][0], to_unit='nm'), 0.3807746)
    assert check_shape_1
    assert check_shape_2
    assert check_neighbors
    assert check_neighbors_2
    assert check_distance

def test_get_neighbors_from_molsysmt_MolSys_7():
    molsys = msm.convert(tests_systems['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    atoms_in_residues_chain_0 = msm.get(molsys, element='group',
                                        selection="molecule_type=='protein' and chain_index==0", atom_index=True)
    atoms_in_residues_chain_1 = msm.get(molsys, element='group',
                                        selection="molecule_type=='protein' and chain_index==1", atom_index=True)
    neighbors, distances = msm.structure.get_neighbors(molsys,
                                     selection= atoms_in_residues_chain_0,
                                     selection_2= atoms_in_residues_chain_1,
                                     threshold=1.2*puw.unit('nanometers'))
    check_n_contacts = (18==len(neighbors[0,11]))
    assert check_n_contacts


