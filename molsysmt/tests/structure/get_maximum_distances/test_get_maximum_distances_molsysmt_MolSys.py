"""
Unit and regression test for the get_mininum_distances module of the molsysmt package on XYZ molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.systems import tests as tests_systems
from molsysmt import pyunitwizard as puw
import numpy as np

# Distance between atoms in space and time

def test_get_maximum_distances_from_molsysmt_MolSys_1():
    molsys = msm.convert(tests_systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    list_atom_groups = msm.get(molsys, element='group', selection='all', atom_index=True)
    max_pairs, max_distances = msm.structure.get_maximum_distances(molsys, groups_of_atoms=list_atom_groups,
                                                group_behavior='geometric center')
    check_shape_1 = ((5000,2)==max_pairs.shape)
    check_shape_2 = ((5000,)==max_distances.shape)
    check_pairs = np.all(max_pairs[0]==np.array([0, 6]))
    check_distance = np.isclose(puw.get_value(max_distances[1000], to_unit='nm'), 2.05848188)
    assert check_shape_1
    assert check_shape_2
    assert check_pairs
    assert check_distance

def test_get_maximum_distances_from_molsysmt_MolSys_2():
    molsys = msm.convert(tests_systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    list_atom_groups = msm.get(molsys, element='group', selection='all', atom_index=True)
    frames=np.arange(msm.get(molsys, n_structures=True))
    max_group, max_distances = msm.structure.get_maximum_distances(molsys,
                                                groups_of_atoms=list_atom_groups,
                                                group_behavior='geometric center',
                                                groups_of_atoms_2=list_atom_groups,
                                                group_behavior_2='geometric center',
                                                structure_indices=frames[:-1],
                                                structure_indices_2=frames[1:],
                                                pairs=True)
    check_shape_1 = ((4999,)==max_group.shape)
    check_distance = np.isclose(puw.get_value(max_distances[1000], to_unit='nm'), 0.85040462)
    assert check_shape_1
    assert check_distance

