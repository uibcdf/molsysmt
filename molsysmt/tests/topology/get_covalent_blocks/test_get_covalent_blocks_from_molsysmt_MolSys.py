"""
Unit and regression test for the get_covalent_blocks module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_get_covalent_blocks_molsysmt_MolSys_1():
    molsys = msm.demo.classes.metenkephalin(to_form='molsysmt.MolSys')
    blocks = msm.topology.get_covalent_blocks(molsys)
    true_blocks = np.array([{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
        21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43,
        44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66,
        67, 68, 69, 70, 71}],
      dtype=object)
    check = np.all(blocks==true_blocks)
    assert check

def test_get_covalent_blocks_molsysmt_MolSys_2():
    molsys = msm.demo.classes.metenkephalin(to_form='molsysmt.MolSys')
    blocks = msm.topology.get_covalent_blocks(molsys, remove_bonds=[[19,21],[33,35]])
    true_blocks = np.array([{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20},
       {32, 33, 34, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31},
       {35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71}],
      dtype=object)
    check = np.all(blocks==true_blocks)
    assert check

def test_get_covalent_blocks_molsysmt_MolSys_3():
    molsys = msm.demo.classes.metenkephalin(to_form='molsysmt.MolSys')
    blocks = msm.topology.get_covalent_blocks(molsys, remove_bonds=[[19,21],[33,35]])
    blocks_np = msm.topology.get_covalent_blocks(molsys, remove_bonds=[[19,21],[33,35]], output_form='array')
    true_blocks = np.array([{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20},
       {32, 33, 34, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31},
       {35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71}],
      dtype=object)
    true_blocks_np = np.zeros(72, dtype=int)
    true_blocks_np[list(true_blocks[1])]=1
    true_blocks_np[list(true_blocks[2])]=2
    check = np.all(blocks_np==true_blocks_np)
    assert check


