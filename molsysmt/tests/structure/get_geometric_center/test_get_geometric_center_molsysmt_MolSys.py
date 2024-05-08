"""
Unit and regression test for the get_geometric_center module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

# Distance between atoms in space and time

def test_get_geometric_center_molsysmt_MolSys_1():

    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    center = msm.structure.get_center(molsys)
    n_structures = msm.get(molsys, element='system', n_structures=True)
    check_shape = np.all((n_structures,1,3)==center.shape)
    check_values = np.allclose([0.800907, 1.0867966, -0.02075539], msm.pyunitwizard.get_value(center[1000, 0, :], to_unit='nm'))
    assert check_shape and check_values

def test_get_geometric_center_molsysmt_MolSys_2():

    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    center_group_0 = msm.structure.get_center(molsys, selection='group_index==0')
    center_group_1 = msm.structure.get_center(molsys, selection='group_index==1')
    distance_groups = msm.structure.get_distances(center_group_0, molecular_system_2=center_group_1)
    distance_groups_2 = msm.structure.get_distances(molsys, selection='group_index==0',
            center_of_atoms=True, selection_2='group_index==1', center_of_atoms_2=True)
    check = np.allclose(distance_groups, distance_groups_2)
    assert check

def test_get_geometric_center_molsysmt_MolSys_3():

    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    center_group_0 = msm.structure.get_center(molsys, selection='group_index==0')
    center_group_1 = msm.structure.get_center(molsys, selection='group_index==1')
    distance_groups = msm.structure.get_distances(center_group_0, molecular_system_2=center_group_1)
    true_distance = [0.3654746, 0.3619029, 0.38273572, 0.37043084, 0.37867113, 0.35408696,
            0.370594580, 0.363487730, 0.372687990, 0.34901823]
    check_value = np.allclose(true_distance, msm.pyunitwizard.get_value(distance_groups[1000:1010, 0, 0], to_unit='nm'))
    assert check_value

