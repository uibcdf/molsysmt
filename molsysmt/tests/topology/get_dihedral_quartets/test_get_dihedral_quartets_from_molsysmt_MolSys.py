"""
Unit and regression test for the get_dihedral_quartets module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_get_dihedral_quartets_from_molsysmt_MolSys_1():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    chains = msm.topology.get_dihedral_quartets(molsys, phi=True)
    true_value_1 = np.array([[ 2,  9, 10, 11],
       [11, 16, 17, 18],
       [18, 25, 26, 27],
       [27, 32, 33, 34],
       [34, 40, 41, 42]])
    true_value_2 = np.array([[781, 783, 784, 785],
       [785, 792, 793, 794],
       [794, 799, 800, 801],
       [801, 807, 808, 809],
       [809, 816, 817, 818]])
    true_value_3 = np.array([[1541, 1544, 1545, 1546],
       [1546, 1549, 1550, 1551],
       [1551, 1558, 1559, 1560],
       [1560, 1566, 1567, 1568],
       [1568, 1577, 1578, 1579]])
    check_shape_1 = np.all((495, 4)==chains.shape)
    check_value_1 = np.all(true_value_1==chains[:5,:])
    check_value_2 = np.all(true_value_2==chains[100:105,:])
    check_value_3 = np.all(true_value_3==chains[200:205,:])
    assert check_shape_1 and check_value_1 and check_value_2 and check_value_3

def test_get_dihedral_quartets_from_molsysmt_MolSys_2():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    chains = msm.topology.get_dihedral_quartets(molsys, selection='10<=group_index<=15', psi=True)
    true_value_1 = np.array([[ 77,  78,  79,  86],
       [ 86,  87,  88,  92],
       [ 92,  93,  94, 100],
       [100, 101, 102, 104],
       [104, 105, 106, 110]])
    check_value_1 = np.all(true_value_1==chains)
    assert check_value_1

def test_get_dihedral_quartets_from_molsysmt_MolSys_3():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    chains = msm.topology.get_dihedral_quartets(molsys, chi5=True)
    true_value_1 = np.array([[1572, 1573, 1574, 1575],
       [1666, 1667, 1668, 1669],
       [1721, 1722, 1723, 1724],
       [2303, 2304, 2305, 2306],
       [2428, 2429, 2430, 2431]])
    n_args = msm.get(molsys, element='group', selection='group_name=="ARG"', n_groups=True)
    check_shape_1 = np.all((n_args, 4)==chains.shape)
    check_value_1 = np.all(true_value_1==chains[10:15])
    assert check_shape_1 and check_value_1

def test_get_dihedral_quartets_from_molsysmt_MolSys_4():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    chains = msm.topology.get_dihedral_quartets(molsys, phi=True, psi=True)
    chains = np.vstack(chains)
    true_value_1 = np.array([[ 2,  9, 10, 11],
       [11, 16, 17, 18],
       [18, 25, 26, 27],
       [27, 32, 33, 34],
       [34, 40, 41, 42]])
    true_value_2 = np.array([[3067, 3071, 3072, 3073],
       [3073, 3080, 3081, 3082],
       [3082, 3089, 3090, 3091],
       [3091, 3094, 3095, 3096],
       [3096, 3108, 3109, 3110]])
    true_value_3 = np.array([[2347, 2348, 2349, 2358],
       [2358, 2359, 2360, 2367],
       [2367, 2368, 2369, 2375],
       [2375, 2376, 2377, 2380],
       [2380, 2381, 2382, 2385]])
    check_shape_1 = np.all((990, 4)==chains.shape)
    check_value_1 = np.all(true_value_1==chains[:5,:])
    check_value_2 = np.all(true_value_2==chains[400:405,:])
    check_value_3 = np.all(true_value_3==chains[800:805,:])
    assert check_shape_1 and check_value_1 and check_value_2 and check_value_3

def test_get_dihedral_quartets_from_molsysmt_MolSys_6():
    molsys = msm.convert(msm.demo['Met-enkephalin']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    phi_chains, phi_blocks = msm.topology.get_dihedral_quartets(molsys, with_blocks=True, phi=True)
    true_value_1 = np.array([33, 35, 37, 53])
    true_value_2 = np.array([{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36},
       {37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71}], dtype=object)
    check_value_1 = np.all(true_value_1==phi_chains[2])
    check_value_2 = np.all(true_value_2==phi_blocks[2])
    assert check_value_1 and check_value_2


