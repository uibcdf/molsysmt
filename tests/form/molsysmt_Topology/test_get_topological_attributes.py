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
    assert all_component_name_Hk2[2685:2688] == ['protein 1', 'protein 1', 'protein 1']
    assert all_component_name_Hk2[13374:13380] == ['UNX', 'UNX', 'UNX', 'unknown 4', 'unknown 4', 'unknown 4']
    assert all_component_name_Hk2[0] == 'protein 0'
    assert all_component_name_Hk2[-1] == 'water'
    assert all_component_name_BB[2685:2688] == ['protein 3', 'protein 3', 'protein 3']
    assert all_component_name_BB[-515:-510] == ['protein 5', 'protein 5', 'water', 'water', 'water']
    assert all_component_name_BB[0] == 'protein 0'
    assert all_component_name_BB[-1] == 'water'
    assert list_component_name_Hk2 == ['protein 0', 'protein 0', 'protein 0']
    assert list_component_name_BB == ['protein 0', 'protein 0', 'protein 0', 'protein 0']

def test_get_component_type_from_atom():

    all_component_type_Hk2 = aux.get_component_type_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_component_type_BB = aux.get_component_type_from_atom(molsys_BB.topology, skip_digestion=True)
    list_component_type_Hk2 = aux.get_component_type_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_component_type_BB = aux.get_component_type_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_component_type_Hk2, list)
    assert len(all_component_type_Hk2) == 13546
    assert len(all_component_type_BB) == 5151
    assert all_component_type_Hk2[2685:2688] == ['protein', 'protein', 'protein']
    assert all_component_type_Hk2[13374:13380] == ['ion', 'ion', 'ion', 'saccharide', 'saccharide', 'saccharide']
    assert all_component_type_Hk2[0] == 'protein'
    assert all_component_type_Hk2[-1] == 'water'
    assert all_component_type_BB[2685:2688] == ['protein', 'protein', 'protein']
    assert all_component_type_BB[-515:-510] == ['protein', 'protein', 'water', 'water', 'water']
    assert all_component_type_BB[0] == 'protein'
    assert all_component_type_BB[-1] == 'water'
    assert list_component_type_Hk2 == ['protein', 'protein', 'protein']
    assert list_component_type_BB == ['protein', 'protein', 'protein', 'protein']

def test_get_molecule_index_from_atom():

    all_molecule_index_Hk2 = aux.get_molecule_index_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_molecule_index_BB = aux.get_molecule_index_from_atom(molsys_BB.topology, skip_digestion=True)
    list_molecule_index_Hk2 = aux.get_molecule_index_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_molecule_index_BB = aux.get_molecule_index_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_molecule_index_Hk2, list)
    assert len(all_molecule_index_Hk2) == 13546
    assert len(all_molecule_index_BB) == 5151
    assert all_molecule_index_Hk2[2685:2688] == [0, 0, 0]
    assert all_molecule_index_Hk2[13374:13380] == [15, 16, 17, 18, 18, 18]
    assert all_molecule_index_Hk2[0] == 0
    assert all_molecule_index_Hk2[-1] == 134
    assert all_molecule_index_BB[2685:2688] == [3, 3, 3]
    assert all_molecule_index_BB[-515:-510] == [5, 5, 6, 7, 8]
    assert all_molecule_index_BB[0] == 0
    assert all_molecule_index_BB[-1] == 518
    assert list_molecule_index_Hk2 == [0, 0, 0]
    assert list_molecule_index_BB == [0, 0, 0, 0]

def test_get_molecule_id_from_atom():

    all_molecule_id_Hk2 = aux.get_molecule_id_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_molecule_id_BB = aux.get_molecule_id_from_atom(molsys_BB.topology, skip_digestion=True)
    list_molecule_id_Hk2 = aux.get_molecule_id_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_molecule_id_BB = aux.get_molecule_id_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_molecule_id_Hk2, list)
    assert len(all_molecule_id_Hk2) == 13546
    assert len(all_molecule_id_BB) == 5151
    assert all_molecule_id_Hk2[2685:2688] == [0, 0, 0]
    assert all_molecule_id_Hk2[13374:13380] == [15, 16, 17, 18, 18, 18]
    assert all_molecule_id_Hk2[0] == 0
    assert all_molecule_id_Hk2[-1] == 134
    assert all_molecule_id_BB[2685:2688] == [3, 3, 3]
    assert all_molecule_id_BB[-515:-510] == [5, 5, 6, 7, 8]
    assert all_molecule_id_BB[0] == 0
    assert all_molecule_id_BB[-1] == 518
    assert list_molecule_id_Hk2 == [0, 0, 0]
    assert list_molecule_id_BB == [0, 0, 0, 0]

def test_get_molecule_name_from_atom():

    all_molecule_name_Hk2 = aux.get_molecule_name_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_molecule_name_BB = aux.get_molecule_name_from_atom(molsys_BB.topology, skip_digestion=True)
    list_molecule_name_Hk2 = aux.get_molecule_name_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_molecule_name_BB = aux.get_molecule_name_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_molecule_name_Hk2, list)
    assert len(all_molecule_name_Hk2) == 13546
    assert len(all_molecule_name_BB) == 5151
    assert all_molecule_name_Hk2[2685:2688] == ['Hexokinase-2', 'Hexokinase-2', 'Hexokinase-2']
    assert all_molecule_name_Hk2[13374:13380] == ['UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION',
                                                  'alpha-D-glucopyranose', 'alpha-D-glucopyranose', 'alpha-D-glucopyranose']
    assert all_molecule_name_Hk2[0] == 'Hexokinase-2'
    assert all_molecule_name_Hk2[-1] == 'water'
    assert all_molecule_name_BB[2685:2688] == ['BARSTAR', 'BARSTAR', 'BARSTAR']
    assert all_molecule_name_BB[-515:-510] ==  ['BARSTAR', 'BARSTAR', 'water', 'water', 'water']
    assert all_molecule_name_BB[0] == 'BARNASE'
    assert all_molecule_name_BB[-1] == 'water'
    assert list_molecule_name_Hk2 == ['Hexokinase-2', 'Hexokinase-2', 'Hexokinase-2']
    assert list_molecule_name_BB == ['BARNASE', 'BARNASE', 'BARNASE', 'BARNASE']

def test_get_molecule_type_from_atom():

    all_molecule_type_Hk2 = aux.get_molecule_type_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_molecule_type_BB = aux.get_molecule_type_from_atom(molsys_BB.topology, skip_digestion=True)
    list_molecule_type_Hk2 = aux.get_molecule_type_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_molecule_type_BB = aux.get_molecule_type_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_molecule_type_Hk2, list)
    assert len(all_molecule_type_Hk2) == 13546
    assert len(all_molecule_type_BB) == 5151
    assert all_molecule_type_Hk2[2685:2688] == ['protein', 'protein', 'protein']
    assert all_molecule_type_Hk2[13374:13380] == ['unknown', 'unknown', 'unknown', 'saccharide', 'saccharide', 'saccharide']
    assert all_molecule_type_Hk2[0] == 'protein'
    assert all_molecule_type_Hk2[-1] == 'water'
    assert all_molecule_type_BB[2685:2688] == ['protein', 'protein', 'protein']
    assert all_molecule_type_BB[-515:-510] ==  ['protein', 'protein', 'water', 'water', 'water']
    assert all_molecule_type_BB[0] == 'protein'
    assert all_molecule_type_BB[-1] == 'water'
    assert list_molecule_type_Hk2 == ['protein', 'protein', 'protein']
    assert list_molecule_type_BB == ['protein', 'protein', 'protein', 'protein']

def test_get_entity_index_from_atom():

    all_entity_index_Hk2 = aux.get_entity_index_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_entity_index_BB = aux.get_entity_index_from_atom(molsys_BB.topology, skip_digestion=True)
    list_entity_index_Hk2 = aux.get_entity_index_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_entity_index_BB = aux.get_entity_index_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_entity_index_Hk2, list)
    assert len(all_entity_index_Hk2) == 13546
    assert len(all_entity_index_BB) == 5151
    assert all_entity_index_Hk2[2685:2688] == [0, 0, 0]
    assert all_entity_index_Hk2[13374:13380] == [3, 3, 3, 1, 1, 1]
    assert all_entity_index_Hk2[0] == 0
    assert all_entity_index_Hk2[-1] == 4
    assert all_entity_index_BB[2685:2688] == [1, 1, 1]
    assert all_entity_index_BB[-515:-510] == [1, 1, 2, 2, 2]
    assert all_entity_index_BB[0] == 0
    assert all_entity_index_BB[-1] == 2
    assert list_entity_index_Hk2 == [0, 0, 0]
    assert list_entity_index_BB == [0, 0, 0, 0]

def test_get_entity_id_from_atom():

    all_entity_id_Hk2 = aux.get_entity_id_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_entity_id_BB = aux.get_entity_id_from_atom(molsys_BB.topology, skip_digestion=True)
    list_entity_id_Hk2 = aux.get_entity_id_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_entity_id_BB = aux.get_entity_id_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_entity_id_Hk2, list)
    assert len(all_entity_id_Hk2) == 13546
    assert len(all_entity_id_BB) == 5151
    assert all_entity_id_Hk2[2685:2688] == [1, 1, 1]
    assert all_entity_id_Hk2[13374:13380] == [4, 4, 4, 2, 2, 2]
    assert all_entity_id_Hk2[0] == 1
    assert all_entity_id_Hk2[-1] == 5
    assert all_entity_id_BB[2685:2688] == [2, 2, 2]
    assert all_entity_id_BB[-515:-510] == [2, 2, 3, 3, 3]
    assert all_entity_id_BB[0] == 1
    assert all_entity_id_BB[-1] == 3
    assert list_entity_id_Hk2 == [1, 1, 1]
    assert list_entity_id_BB == [1, 1, 1, 1]

def test_get_entity_name_from_atom():

    all_entity_name_Hk2 = aux.get_entity_name_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_entity_name_BB = aux.get_entity_name_from_atom(molsys_BB.topology, skip_digestion=True)
    list_entity_name_Hk2 = aux.get_entity_name_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_entity_name_BB = aux.get_entity_name_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_entity_name_Hk2, list)
    assert len(all_entity_name_Hk2) == 13546
    assert len(all_entity_name_BB) == 5151
    assert all_entity_name_Hk2[2685:2688] == ['Hexokinase-2', 'Hexokinase-2', 'Hexokinase-2']
    assert all_entity_name_Hk2[13374:13380] == ['UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION',
                                                'alpha-D-glucopyranose', 'alpha-D-glucopyranose', 'alpha-D-glucopyranose']
    assert all_entity_name_Hk2[0] == 'Hexokinase-2'
    assert all_entity_name_Hk2[-1] == 'water'
    assert all_entity_name_BB[2685:2688] == ['BARSTAR', 'BARSTAR', 'BARSTAR']
    assert all_entity_name_BB[-515:-510] == ['BARSTAR', 'BARSTAR', 'water', 'water', 'water']
    assert all_entity_name_BB[0] == 'BARNASE'
    assert all_entity_name_BB[-1] == 'water'
    assert list_entity_name_Hk2 == ['Hexokinase-2', 'Hexokinase-2', 'Hexokinase-2']
    assert list_entity_name_BB == ['BARNASE', 'BARNASE', 'BARNASE', 'BARNASE']

def test_get_entity_type_from_atom():

    all_entity_type_Hk2 = aux.get_entity_type_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_entity_type_BB = aux.get_entity_type_from_atom(molsys_BB.topology, skip_digestion=True)
    list_entity_type_Hk2 = aux.get_entity_type_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_entity_type_BB = aux.get_entity_type_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_entity_type_Hk2, list)
    assert len(all_entity_type_Hk2) == 13546
    assert len(all_entity_type_BB) == 5151
    assert all_entity_type_Hk2[2685:2688] == ['protein', 'protein', 'protein']
    assert all_entity_type_Hk2[13374:13380] == ['unknown', 'unknown', 'unknown', 'saccharide', 'saccharide', 'saccharide']
    assert all_entity_type_Hk2[0] == 'protein'
    assert all_entity_type_Hk2[-1] == 'water'
    assert all_entity_type_BB[2685:2688] == ['protein', 'protein', 'protein']
    assert all_entity_type_BB[-515:-510] == ['protein', 'protein', 'water', 'water', 'water']
    assert all_entity_type_BB[0] == 'protein'
    assert all_entity_type_BB[-1] == 'water'
    assert list_entity_type_Hk2 == ['protein', 'protein', 'protein']
    assert list_entity_type_BB == ['protein', 'protein', 'protein', 'protein']


def test_get_chain_index_from_atom():

    all_chain_index_Hk2 = aux.get_chain_index_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_chain_index_BB = aux.get_chain_index_from_atom(molsys_BB.topology, skip_digestion=True)
    list_chain_index_Hk2 = aux.get_chain_index_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_chain_index_BB = aux.get_chain_index_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_chain_index_Hk2, list)
    assert len(all_chain_index_Hk2) == 13546
    assert len(all_chain_index_BB) == 5151
    assert all_chain_index_Hk2[2685:2688] == [0, 0, 0]
    assert all_chain_index_Hk2[13374:13380] == [15, 16, 17, 18, 18, 18]
    assert all_chain_index_Hk2[0] == 0
    assert all_chain_index_Hk2[-1] == 39
    assert all_chain_index_BB[2685:2688] == [3, 3, 3]
    assert all_chain_index_BB[-515:-510] == [5, 5, 6, 6, 6]
    assert all_chain_index_BB[0] == 0
    assert all_chain_index_BB[-1] == 11
    assert list_chain_index_Hk2 == [0, 0, 0]
    assert list_chain_index_BB == [0, 0, 0, 0]

def test_get_chain_id_from_atom():

    all_chain_id_Hk2 = aux.get_chain_id_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_chain_id_BB = aux.get_chain_id_from_atom(molsys_BB.topology, skip_digestion=True)
    list_chain_id_Hk2 = aux.get_chain_id_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_chain_id_BB = aux.get_chain_id_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_chain_id_Hk2, list)
    assert len(all_chain_id_Hk2) == 13546
    assert len(all_chain_id_BB) == 5151
    assert all_chain_id_Hk2[2685:2688] == ['A', 'A', 'A']
    assert all_chain_id_Hk2[13374:13380] == ['P', 'Q', 'R', 'S', 'S', 'S']
    assert all_chain_id_Hk2[0] == 'A'
    assert all_chain_id_Hk2[-1] == 'NA'
    assert all_chain_id_BB[2685:2688] == ['D', 'D', 'D']
    assert all_chain_id_BB[-515:-510] == ['F', 'F', 'G', 'G', 'G']
    assert all_chain_id_BB[0] == 'A'
    assert all_chain_id_BB[-1] == 'L'
    assert list_chain_id_Hk2 == ['A', 'A', 'A']
    assert list_chain_id_BB == ['A', 'A', 'A', 'A']























