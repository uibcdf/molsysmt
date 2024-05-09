"""
Unit and regression test for the get_covalent_chains module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

# Distance between atoms in space and time

def test_get_covalent_chains_molsysmt_MolSys_1():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    covalent_chains =msm.topology.get_covalent_chains(molsys, chain=['atom_name=="C"', 'atom_name=="N"', 'atom_name=="CA"', 'atom_name=="C"'],
                                                      selection="component_index==0")
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
    check_shape_1 = np.all((247, 4)==covalent_chains.shape)
    check_value_1 = np.all(true_value_1==covalent_chains[:5,:])
    check_value_2 = np.all(true_value_2==covalent_chains[100:105,:])
    check_value_3 = np.all(true_value_3==covalent_chains[200:205,:])
    assert check_shape_1 and check_value_1 and check_value_2 and check_value_3

def test_get_covalent_chains_molsysmt_MolSys_2():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    covalent_chains =msm.topology.get_covalent_chains(molsys, chain=['atom_name=="C"', 'atom_name=="N"',
                                                              'atom_name=="CA"', 'atom_name==["C", "CB"]'],
                                                              selection="component_index==0")
    true_value_1 = np.array([[ 2,  9, 10, 11],
       [ 2,  9, 10, 13],
       [11, 16, 17, 18],
       [11, 16, 17, 20],
       [18, 25, 26, 27]])
    true_value_2 = np.array([[382, 385, 386, 389],
       [387, 396, 397, 398],
       [387, 396, 397, 400],
       [398, 404, 405, 406],
       [398, 404, 405, 408]])
    true_value_3 = np.array([[801, 807, 808, 809],
       [801, 807, 808, 811],
       [809, 816, 817, 818],
       [809, 816, 817, 820],
       [818, 824, 825, 826]])
    check_shape_1 = np.all((477, 4)==covalent_chains.shape)
    check_value_1 = np.all(true_value_1==covalent_chains[:5,:])
    check_value_2 = np.all(true_value_2==covalent_chains[100:105,:])
    check_value_3 = np.all(true_value_3==covalent_chains[200:205,:])
    assert check_shape_1 and check_value_1 and check_value_2 and check_value_3

