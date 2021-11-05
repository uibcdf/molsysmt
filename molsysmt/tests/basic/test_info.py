"""
Unit and regression test for the info module of the molsysmt package.
"""

import molsysmt as msm
import numpy as np
from pandas import DataFrame

def test_info_1():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    df = msm.info(molsys, target='atom', indices=[9,10,11,12], output='dataframe')
    true_dict = {'index': {0: 9, 1: 10, 2: 11, 3: 12},
                 'id': {0: 10, 1: 11, 2: 12, 3: 13},
                 'name': {0: 'N', 1: 'CA', 2: 'C', 3: 'O'},
                 'type': {0: 'N', 1: 'C', 2: 'C', 3: 'O'},
                 'group index': {0: 1, 1: 1, 2: 1, 3: 1},
                 'group id': {0: 5, 1: 5, 2: 5, 3: 5},
                 'group name': {0: 'PRO', 1: 'PRO', 2: 'PRO', 3: 'PRO'},
                 'group type': {0: 'aminoacid',
                  1: 'aminoacid',
                  2: 'aminoacid',
                  3: 'aminoacid'},
                 'component index': {0: 0, 1: 0, 2: 0, 3: 0},
                 'chain index': {0: 0, 1: 0, 2: 0, 3: 0},
                 'molecule index': {0: 0, 1: 0, 2: 0, 3: 0},
                 'molecule type': {0: 'protein', 1: 'protein', 2: 'protein', 3: 'protein'},
                 'entity index': {0: 0, 1: 0, 2: 0, 3: 0},
                 'entity name': {0: 'TRIOSEPHOSPHATE ISOMERASE',
                  1: 'TRIOSEPHOSPHATE ISOMERASE',
                  2: 'TRIOSEPHOSPHATE ISOMERASE',
                  3: 'TRIOSEPHOSPHATE ISOMERASE'}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

def test_info_2():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    df = msm.info(molsys, target='atom', selection='group_index==6')
    true_dict = {'index': {0: 45, 1: 46, 2: 47, 3: 48, 4: 49},
                 'id': {0: 46, 1: 47, 2: 48, 3: 49, 4: 50},
                 'name': {0: 'N', 1: 'CA', 2: 'C', 3: 'O', 4: 'CB'},
                 'type': {0: 'N', 1: 'C', 2: 'C', 3: 'O', 4: 'C'},
                 'group index': {0: 6, 1: 6, 2: 6, 3: 6, 4: 6},
                 'group id': {0: 10, 1: 10, 2: 10, 3: 10, 4: 10},
                 'group name': {0: 'ALA', 1: 'ALA', 2: 'ALA', 3: 'ALA', 4: 'ALA'},
                 'group type': {0: 'aminoacid',
                  1: 'aminoacid',
                  2: 'aminoacid',
                  3: 'aminoacid',
                  4: 'aminoacid'},
                 'component index': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
                 'chain index': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
                 'molecule index': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
                 'molecule type': {0: 'protein',
                  1: 'protein',
                  2: 'protein',
                  3: 'protein',
                  4: 'protein'},
                 'entity index': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
                 'entity name': {0: 'TRIOSEPHOSPHATE ISOMERASE',
                  1: 'TRIOSEPHOSPHATE ISOMERASE',
                  2: 'TRIOSEPHOSPHATE ISOMERASE',
                  3: 'TRIOSEPHOSPHATE ISOMERASE',
                  4: 'TRIOSEPHOSPHATE ISOMERASE'}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

def test_info_3():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    df = msm.info(molsys, target='group', indices=[20,21,22,23])
    true_dict ={'index': {0: 20, 1: 21, 2: 22, 3: 23},
                'id': {0: 24, 1: 25, 2: 26, 3: 27},
                'name': {0: 'PRO', 1: 'LEU', 2: 'ILE', 3: 'GLU'},
                'type': {0: 'aminoacid', 1: 'aminoacid', 2: 'aminoacid', 3: 'aminoacid'},
                'n atoms': {0: 7, 1: 8, 2: 8, 3: 9},
                'component index': {0: 0, 1: 0, 2: 0, 3: 0},
                'chain index': {0: 0, 1: 0, 2: 0, 3: 0},
                'molecule index': {0: 0, 1: 0, 2: 0, 3: 0},
                'molecule type': {0: 'protein', 1: 'protein', 2: 'protein', 3: 'protein'},
                'entity index': {0: 0, 1: 0, 2: 0, 3: 0},
                'entity name': {0: 'TRIOSEPHOSPHATE ISOMERASE',
                 1: 'TRIOSEPHOSPHATE ISOMERASE',
                 2: 'TRIOSEPHOSPHATE ISOMERASE',
                 3: 'TRIOSEPHOSPHATE ISOMERASE'}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

def test_info_4():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    df = msm.info(molsys, target='component', selection='molecule_type!="water"')
    true_dict = {'index': {0: 0, 1: 1},
                 'n atoms': {0: 1906, 1: 1912},
                 'n groups': {0: 248, 1: 249},
                 'chain index': {0: 0, 1: 1},
                 'molecule index': {0: 0, 1: 0},
                 'molecule type': {0: 'protein', 1: 'protein'},
                 'entity index': {0: 0, 1: 0},
                 'entity name': {0: 'TRIOSEPHOSPHATE ISOMERASE',
                  1: 'TRIOSEPHOSPHATE ISOMERASE'}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

#def test_info_5():
#    molsys = msm.demo.classes.TcTIM_in_pdbid_1tcd(to_form='molsysmt.MolSys')
#    df = msm.info(molsys, target='chain')
#    true_dict = {'index': {0: 0, 1: 1, 2: 2, 3: 3},
#                 'id': {0: 'A', 1: 'B', 2: 'C', 3: 'D'},
#                 'name': {0: 'A', 1: 'B', 2: 'A', 3: 'B'},
#                 'n atoms': {0: 1906, 1: 1912, 2: 73, 3: 92},
#                 'n groups': {0: 248, 1: 249, 2: 73, 3: 92},
#                 'n components': {0: 1, 1: 1, 2: 73, 3: 92},
#                 'molecule index': {0: 0,
#                  1: 0,
#                  2: np.array(list(range(1, 74))),
#                  3: np.array(list(range(74, 166)))},
#                 'molecule type': {0: 'protein',
#                  1: 'protein',
#                  2: np.array(['water' for ii in range(73)], dtype=object),
#                  3: np.array(['water' for ii in range(92)], dtype=object)},
#                 'entity index': {0: 0, 1: 0, 2: 1, 3: 1},
#                 'entity name': {0: 'TRIOSEPHOSPHATE ISOMERASE',
#                  1: 'TRIOSEPHOSPHATE ISOMERASE',
#                  2: 'water',
#                  3: 'water'}}
#    true_df = DataFrame(true_dict)
#    assert df.data.equals(true_df)

def test_info_6():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    df = msm.info(molsys, target='molecule', selection='molecule_type!="water"')
    true_dict = {'index': {0: 0},
                 'name': {0: 'TRIOSEPHOSPHATE ISOMERASE'},
                 'type': {0: 'protein'},
                 'n atoms': {0: 3818},
                 'n groups': {0: 497},
                 'n components': {0: 2},
                 'chain index': {0: np.array([0, 1], dtype=object)},
                 'entity index': {0: 0},
                 'entity name': {0: 'TRIOSEPHOSPHATE ISOMERASE'}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

def test_info_7():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    df = msm.info(molsys, target='entity')
    true_dict = {'index': {0: 0, 1: 1},
                 'name': {0: 'TRIOSEPHOSPHATE ISOMERASE', 1: 'water'},
                 'type': {0: 'protein', 1: 'water'},
                 'n atoms': {0: 3818, 1: 165},
                 'n groups': {0: 497, 1: 165},
                 'n components': {0: 2, 1: 165},
                 'n chains': {0: 2, 1: 2},
                 'n molecules': {0: 1, 1: 165}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

def test_info_8():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    df = msm.info(molsys)
    true_dict = {'form': {0: 'molsysmt.MolSys'},
                 'n_atoms': {0: 3983},
                 'n_groups': {0: 662},
                 'n_components': {0: 167},
                 'n_chains': {0: 4},
                 'n_molecules': {0: 166},
                 'n_entities': {0: 2},
                 'n_waters': {0: 165},
                 'n_proteins': {0: 1},
                 'n_frames': {0: 1}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

def test_info_9():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    molsys = msm.convert(molsys, to_form='molsysmt.Topology')
    df = msm.info(molsys)
    true_dict = {'form': {0: 'molsysmt.Topology'},
                 'n_atoms': {0: 3983},
                 'n_groups': {0: 662},
                 'n_components': {0: 167},
                 'n_chains': {0: 4},
                 'n_molecules': {0: 166},
                 'n_entities': {0: 2},
                 'n_waters': {0: 165},
                 'n_proteins': {0: 1},
                 'n_frames': {0: None}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

def test_info_10():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    molsys = msm.convert(molsys, to_form='molsysmt.Trajectory')
    df = msm.info(molsys)
    true_dict = {'form': {0: 'molsysmt.Trajectory'},
                 'n_atoms': {0: 3983},
                 'n_groups': {0: None},
                 'n_components': {0: None},
                 'n_chains': {0: None},
                 'n_molecules': {0: None},
                 'n_entities': {0: None},
                 'n_frames': {0: 1}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

def test_info_11():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    molsys = msm.convert(molsys, to_form=['molsysmt.Topology', 'molsysmt.Trajectory'])
    df = msm.info(molsys)
    true_dict = {'form': {0: ['molsysmt.Topology', 'molsysmt.Trajectory']},
                 'n_atoms': {0: 3983},
                 'n_groups': {0: 662},
                 'n_components': {0: 167},
                 'n_chains': {0: 4},
                 'n_molecules': {0: 166},
                 'n_entities': {0: 2},
                 'n_waters': {0: 165},
                 'n_proteins': {0: 1},
                 'n_frames': {0: 1}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

def test_info_12():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.info(molsys, target='atom', indices=10, output='short_string')
    true_output = 'CA-11@10'
    assert output == true_output

def test_info_13():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.info(molsys, target='atom', indices=[10,11,12,13], output='short_string')
    true_output = ['CA-11@10', 'C-12@11', 'O-13@12', 'CB-14@13']
    assert np.all(output == true_output)

def test_info_14():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.info(molsys, target='atom', indices=10, output='long_string')
    true_output = 'CA-11@10/PRO-5@1/A-A@0/TRIOSEPHOSPHATE ISOMERASE@0'
    assert output == true_output

def test_info_15():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.info(molsys, target='group', indices=0, output='short_string')
    true_output = 'LYS-4@0'
    assert output == true_output

def test_info_15():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.info(molsys, target='group', indices=3, output='long_string')
    true_output = 'PRO-7@3/A-A@0/TRIOSEPHOSPHATE ISOMERASE@0'
    assert output == true_output

def test_info_16():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.info(molsys, target='component', indices=2, output='short_string')
    true_output = '2'
    assert output == true_output

def test_info_17():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.info(molsys, target='component', indices=2, output='long_string')
    true_output = '2/A-C@2/water@1'
    assert output == true_output

def test_info_18():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.info(molsys, target='chain', indices=2, output='short_string')
    true_output = 'A-C@2'
    assert output == true_output

def test_info_19():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.info(molsys, target='chain', indices=2, output='long_string')
    true_output = 'A-C@2'
    assert output == true_output

def test_info_20():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.info(molsys, target='molecule', indices=0, output='short_string')
    true_output = 'TRIOSEPHOSPHATE ISOMERASE@0'
    assert output == true_output

def test_info_21():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.info(molsys, target='molecule', indices=0, output='long_string')
    true_output = 'TRIOSEPHOSPHATE ISOMERASE@0'
    assert output == true_output

def test_info_22():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.info(molsys, target='entity', indices=0, output='short_string')
    true_output = 'TRIOSEPHOSPHATE ISOMERASE@0'
    assert output == true_output

def test_info_23():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.info(molsys, target='entity', indices=0, output='long_string')
    true_output = 'TRIOSEPHOSPHATE ISOMERASE@0'
    assert output == true_output

def test_info_24():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    df = msm.info(molsys, target='component', selection='molecule_type=="protein"')
    true_dict = {'index': {0: 0, 1: 1},
        'n atoms': {0: 1906, 1: 1912},
        'n groups': {0: 248, 1: 249},
        'chain index': {0: 0, 1: 1},
        'molecule index': {0: 0, 1: 0},
        'molecule type': {0: 'protein', 1: 'protein'},
        'entity index': {0: 0, 1: 0},
        'entity name': {0: 'TRIOSEPHOSPHATE ISOMERASE',
         1: 'TRIOSEPHOSPHATE ISOMERASE'}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)


def test_info_24():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    group_index_in_component_0 = msm.get(molsys, target='group',
                                     selection='component_index==0', index=True)[69]
    group_index_in_component_1 = msm.get(molsys, target='group',
                                     selection='component_index==1', index=True)[12]
    df = msm.info(molsys, target='group', indices=[group_index_in_component_0,
                                                    group_index_in_component_1])
    true_dict = {'index': {0: 69, 1: 260},
        'id': {0: 73, 1: 15},
        'name': {0: 'GLY', 1: 'CYS'},
        'type': {0: 'aminoacid', 1: 'aminoacid'},
        'n atoms': {0: 4, 1: 6},
        'component index': {0: 0, 1: 1},
        'chain index': {0: 0, 1: 1},
        'molecule index': {0: 0, 1: 0},
        'molecule type': {0: 'protein', 1: 'protein'},
        'entity index': {0: 0, 1: 0},
        'entity name': {0: 'TRIOSEPHOSPHATE ISOMERASE',
         1: 'TRIOSEPHOSPHATE ISOMERASE'}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

