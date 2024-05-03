"""
Unit and regression test for the get_label module of the molsysmt package.
"""

import molsysmt as msm
from molsysmt import systems
import numpy as np
from pandas import DataFrame

def test_get_label_1():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    output = msm.get_label(molsys, element='atom', selection=10)
    true_output = 'CA-11@10'
    assert output == true_output

def test_get_label_2():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    output = msm.get_label(molsys, element='atom', selection=[10, 11, 12, 13])
    true_output = ['CA-11@10', 'C-12@11', 'O-13@12', 'CB-14@13']
    assert np.all(output == true_output)

def test_get_label_3():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    output = msm.get_label(molsys, element='atom', selection=10,
            string='{atom_name}-{atom_id}@{atom_index}/{group_name}-{group_id}@{group_index}/{chain_name}-{chain_id}@{chain_index}/{entity_name}@{entity_index}')
    true_output = 'CA-11@10/PRO-5@1/A-0@0/TRIOSEPHOSPHATE ISOMERASE@0'
    assert output == true_output

def test_get_label_4():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    output = msm.get_label(molsys, element='group', selection=0)
    true_output = 'LYS-4@0'
    assert output == true_output

def test_get_label_5():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    output = msm.get_label(molsys, element='group', selection=3,
            string='{group_name}-{group_id}@{group_index}/{chain_name}-{chain_id}@{chain_index}/{entity_name}@{entity_index}')
    true_output = 'PRO-7@3/A-0@0/TRIOSEPHOSPHATE ISOMERASE@0'
    assert output == true_output

def test_get_label_6():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    output = msm.get_label(molsys, element='component', selection=2)
    true_output = 'water-2@2'
    assert output == true_output

def test_get_label_7():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    output = msm.get_label(molsys, element='component', selection=2,
            string='{component_index}/{chain_name}-{chain_id}@{chain_index}/{entity_name}@{entity_index}')
    true_output = '2/A-2@2/water@1'
    assert output == true_output

def test_get_label_8():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    output = msm.get_label(molsys, element='chain', selection=2)
    true_output = 'A-2@2'
    assert output == true_output

def test_get_label_9():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    output = msm.get_label(molsys, element='molecule', selection=0,
            string='{molecule_name}@{molecule_index}')
    true_output = 'TRIOSEPHOSPHATE ISOMERASE@0'
    assert output == true_output

def test_get_label_10():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    output = msm.get_label(molsys, element='entity', selection=0,
            string='{entity_name}@{entity_index}')
    true_output = 'TRIOSEPHOSPHATE ISOMERASE@0'
    assert output == true_output

