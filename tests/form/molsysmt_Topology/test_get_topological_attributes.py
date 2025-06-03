"""
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.form.molsysmt_Topology import get_topological_attributes as aux
import numpy as np

molsys_Hk2 = msm.convert(msm.systems['Hexokinase 2']['2nzt.bcif.gz'], to_form='molsysmt.MolSys')
molsys_BB = msm.convert(msm.systems['Barnase-Barstar']['1brs.bcif.gz'], to_form='molsysmt.MolSys')

def test_get_atom_index_from_atom():

    all_atom_indices_Hk2 = aux.get_atom_index_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_atom_indices_BB = aux.get_atom_index_from_atom(molsys_BB.topology, skip_digestion=True)
    list_atom_indices_Hk2 = aux.get_atom_index_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)

    assert isinstance(all_atom_indices_Hk2, list)
    assert all_atom_indices_Hk2 == list(range(0, 13546))
    assert all_atom_indices_BB == list(range(0, 5151))

def test_get_atom_id_from_atom():

    all_atom_ids_Hk2 = aux.get_atom_id_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_atom_ids_BB = aux.get_atom_id_from_atom(molsys_BB.topology, skip_digestion=True)
    list_atom_ids_Hk2 = aux.get_atom_id_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_atom_ids_BB = aux.get_atom_id_from_atom(molsys_Hk2.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_atom_ids_Hk2, list)
    assert all_atom_ids_Hk2 == list(range(1, 13547))
    assert all_atom_ids_BB == list(range(1,2688))+[2689,2691]+list(range(2692, 5154))
    assert list_atom_ids_Hk2 == [5,6,7]
    assert list_atom_ids_BB == [11,12,13,14]

def test_get_atom_name_from_atom():

    all_atom_names_Hk2 = aux.get_atom_name_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_atom_names_BB = aux.get_atom_name_from_atom(molsys_BB.topology, skip_digestion=True)
    list_atom_names_Hk2 = aux.get_atom_name_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_atom_names_BB = aux.get_atom_name_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_atom_names_Hk2, list)
    assert len(all_atom_names_Hk2) == 13546
    assert len(all_atom_names_BB) == 5151
    assert all_atom_names_Hk2[2685:2691] == ['CA', 'C', 'O', 'CB', 'CG1', 'CG2']
    assert all_atom_names_BB[2685:2691] == ['O', 'CB', 'OG', 'N', 'CA', 'C']
    assert list_atom_names_Hk2 == ['CB', 'CG', 'OD1']
    assert list_atom_names_BB == ['O', 'CB', 'CG1', 'CG2']

def test_get_atom_type_from_atom():

    all_atom_types_Hk2 = aux.get_atom_type_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_atom_types_BB = aux.get_atom_type_from_atom(molsys_BB.topology, skip_digestion=True)
    list_atom_types_Hk2 = aux.get_atom_type_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_atom_types_BB = aux.get_atom_type_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_atom_types_Hk2, list)
    assert len(all_atom_types_Hk2) == 13546
    assert len(all_atom_types_BB) == 5151
    assert all_atom_types_Hk2[2685:2691] == ['C', 'C', 'O', 'C', 'C', 'C']
    assert all_atom_types_BB[2685:2691] == ['O', 'C', 'O', 'N', 'C', 'C']
    assert list_atom_types_Hk2 == ['C', 'C', 'O']
    assert list_atom_types_BB == ['O', 'C', 'C', 'C']

def test_get_group_index_from_atom():

    all_group_index_Hk2 = aux.get_group_index_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_group_index_BB = aux.get_group_index_from_atom(molsys_BB.topology, skip_digestion=True)
    list_group_index_Hk2 = aux.get_group_index_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_group_index_BB = aux.get_group_index_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_group_index_Hk2, list)
    assert len(all_group_index_Hk2) == 13546
    assert len(all_group_index_BB) == 5151
    assert all_group_index_Hk2[2685:2691] == [345, 345, 345, 345, 345, 345]
    assert all_group_index_Hk2[0] == 0
    assert all_group_index_Hk2[-1] == 1870
    assert all_group_index_BB[2685:2691] == [339, 339, 339, 340, 340, 340]
    assert all_group_index_BB[0] == 0
    assert all_group_index_BB[-1] == 1100
    assert list_group_index_Hk2 == [0,0,0]
    assert list_group_index_BB == [1,1,1,1]

def test_get_group_id_from_atom():

    all_group_id_Hk2 = aux.get_group_id_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_group_id_BB = aux.get_group_id_from_atom(molsys_BB.topology, skip_digestion=True)
    list_group_id_Hk2 = aux.get_group_id_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_group_id_BB = aux.get_group_id_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_group_id_Hk2, list)
    assert len(all_group_id_Hk2) == 13546
    assert len(all_group_id_BB) == 5151
    assert all_group_id_Hk2[2685:2691] == [369, 369, 369, 369, 369, 369]
    assert all_group_id_Hk2[0] == 17
    assert all_group_id_Hk2[-1] == 1097
    assert all_group_id_BB[2685:2691] == [14, 14, 14, 15, 15, 15]
    assert all_group_id_BB[0] == 3
    assert all_group_id_BB[-1] == 129
    assert list_group_id_Hk2 == [17,17,17]
    assert list_group_id_BB == [4,4,4,4]

def test_get_group_name_from_atom():

    all_group_name_Hk2 = aux.get_group_name_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_group_name_BB = aux.get_group_name_from_atom(molsys_BB.topology, skip_digestion=True)
    list_group_name_Hk2 = aux.get_group_name_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_group_name_BB = aux.get_group_name_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_group_name_Hk2, list)
    assert len(all_group_name_Hk2) == 13546
    assert len(all_group_name_BB) == 5151
    assert all_group_name_Hk2[2685:2688] == ['VAL', 'VAL', 'VAL']
    assert all_group_name_Hk2[13374:13380] == ['UNX', 'UNX', 'UNX', 'GLC', 'GLC', 'GLC']
    assert all_group_name_Hk2[0] == 'ASP'
    assert all_group_name_Hk2[-1] == 'HOH'
    assert all_group_name_BB[2685:2688] == ['SER', 'SER', 'SER']
    assert all_group_name_BB[-515:-510] == ['SER', 'SER', 'HOH', 'HOH', 'HOH']
    assert all_group_name_BB[0] == 'VAL'
    assert all_group_name_BB[-1] == 'HOH'
    assert list_group_name_Hk2 == ['ASP', 'ASP', 'ASP']
    assert list_group_name_BB == ['ILE', 'ILE', 'ILE', 'ILE']

def test_get_group_type_from_atom():

    all_group_type_Hk2 = aux.get_group_type_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_group_type_BB = aux.get_group_type_from_atom(molsys_BB.topology, skip_digestion=True)
    list_group_type_Hk2 = aux.get_group_type_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_group_type_BB = aux.get_group_type_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_group_type_Hk2, list)
    assert len(all_group_type_Hk2) == 13546
    assert len(all_group_type_BB) == 5151
    assert all_group_type_Hk2[2685:2688] == ['amino acid', 'amino acid', 'amino acid']
    assert all_group_type_Hk2[13374:13380] == ['ion', 'ion', 'ion', 'saccharide', 'saccharide', 'saccharide']
    assert all_group_type_Hk2[0] == 'amino acid'
    assert all_group_type_Hk2[-1] == 'water'
    assert all_group_type_BB[2685:2688] == ['amino acid', 'amino acid', 'amino acid']
    assert all_group_type_BB[-515:-510] == ['amino acid', 'amino acid', 'water', 'water', 'water']
    assert all_group_type_BB[0] == 'amino acid'
    assert all_group_type_BB[-1] == 'water'
    assert list_group_type_Hk2 == ['amino acid', 'amino acid', 'amino acid']
    assert list_group_type_BB == ['amino acid', 'amino acid', 'amino acid', 'amino acid']

def test_get_component_index_from_atom():

    all_component_index_Hk2 = aux.get_component_index_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_component_index_BB = aux.get_component_index_from_atom(molsys_BB.topology, skip_digestion=True)
    list_component_index_Hk2 = aux.get_component_index_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_component_index_BB = aux.get_component_index_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_component_index_Hk2, list)
    assert len(all_component_index_Hk2) == 13546
    assert len(all_component_index_BB) == 5151
    assert all_component_index_Hk2[2685:2688] == [1,1,1]
    assert all_component_index_Hk2[13374:13380] == [26, 27, 28, 29, 29, 29]
    assert all_component_index_Hk2[0] == 0
    assert all_component_index_Hk2[-1] == 145
    assert all_component_index_BB[2685:2688] == [3,3,3]
    assert all_component_index_BB[-515:-510] == [7, 7, 8, 9, 10]
    assert all_component_index_BB[0] == 0
    assert all_component_index_BB[-1] == 520
    assert list_component_index_Hk2 == [0,0,0]
    assert list_component_index_BB == [0,0,0,0]

def test_get_component_id_from_atom():

    all_component_id_Hk2 = aux.get_component_id_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_component_id_BB = aux.get_component_id_from_atom(molsys_BB.topology, skip_digestion=True)
    list_component_id_Hk2 = aux.get_component_id_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_component_id_BB = aux.get_component_id_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_component_id_Hk2, list)
    assert len(all_component_id_Hk2) == 13546
    assert len(all_component_id_BB) == 5151
    assert all_component_id_Hk2[2685:2688] == [1,1,1]
    assert all_component_id_Hk2[13374:13380] == [26, 27, 28, 29, 29, 29]
    assert all_component_id_Hk2[0] == 0
    assert all_component_id_Hk2[-1] == 145
    assert all_component_id_BB[2685:2688] == [3,3,3]
    assert all_component_id_BB[-515:-510] == [7, 7, 8, 9, 10]
    assert all_component_id_BB[0] == 0
    assert all_component_id_BB[-1] == 520
    assert list_component_id_Hk2 == [0,0,0]
    assert list_component_id_BB == [0,0,0,0]

def test_get_component_name_from_atom():

    all_component_name_Hk2 = aux.get_component_name_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_component_name_BB = aux.get_component_name_from_atom(molsys_BB.topology, skip_digestion=True)
    list_component_name_Hk2 = aux.get_component_name_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_component_name_BB = aux.get_component_name_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_component_name_Hk2, list)
    assert len(all_component_name_Hk2) == 13546
    assert len(all_component_name_BB) == 5151
    assert all_component_name_Hk2[2685:2688] == [1,1,1]
    assert all_component_name_Hk2[13374:13380] == [26, 27, 28, 29, 29, 29]
    assert all_component_name_Hk2[0] == 0
    assert all_component_name_Hk2[-1] == 145
    assert all_component_name_BB[2685:2688] == [3,3,3]
    assert all_component_name_BB[-515:-510] == [7, 7, 8, 9, 10]
    assert all_component_name_BB[0] == 0
    assert all_component_name_BB[-1] == 520
    assert list_component_name_Hk2 == [0,0,0]
    assert list_component_name_BB == [0,0,0,0]









