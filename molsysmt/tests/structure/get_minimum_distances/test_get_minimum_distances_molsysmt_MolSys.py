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

def test_get_minimum_distances_from_molsysmt_MolSys_1():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    atoms_groups_component_0 = msm.get(molsys, element='group', selection='component_index==0', atom_index=True)
    atoms_groups_component_1 = msm.get(molsys, element='group', selection='component_index==1', atom_index=True)
    min_pairs, min_distances = msm.structure.get_minimum_distances(molsys,
                                                selection=atoms_groups_component_0,
                                                selection_2=atoms_groups_component_1)
    check_shape_1 = ((1,2)==min_pairs.shape)
    check_shape_2 = ((1,)==min_distances.shape)
    check_pairs = np.all(min_pairs[0]==np.array([69, 12]))
    check_distance = np.isclose(puw.get_value(min_distances[0], to_unit='nm'), 0.38221311)
    assert check_shape_1 and check_shape_2 and check_pairs and check_distance

