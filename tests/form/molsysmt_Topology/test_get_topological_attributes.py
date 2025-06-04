"""
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.form.molsysmt_Topology import get_topological_attributes as aux
import numpy as np

molsys_Hk2 = msm.convert(msm.systems['Hexokinase 2']['2nzt.bcif.gz'], to_form='molsysmt.MolSys')
molsys_BB = msm.convert(msm.systems['Barnase-Barstar']['1brs.bcif.gz'], to_form='molsysmt.MolSys')

# From atom

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
    assert all_component_type_Hk2[13374:13380] == ['ion', 'ion', 'ion', 'polysaccharide', 'polysaccharide', 'polysaccharide']
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
    assert all_molecule_type_Hk2[13374:13380] == ['unknown', 'unknown', 'unknown', 'polysaccharide', 'polysaccharide',
                                                  'polysaccharide']
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
    assert all_entity_type_Hk2[13374:13380] == ['unknown', 'unknown', 'unknown', 'polysaccharide', 'polysaccharide',
                                                'polysaccharide']
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

def test_get_chain_name_from_atom():

    all_chain_name_Hk2 = aux.get_chain_name_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_chain_name_BB = aux.get_chain_name_from_atom(molsys_BB.topology, skip_digestion=True)
    list_chain_name_Hk2 = aux.get_chain_name_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_chain_name_BB = aux.get_chain_name_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_chain_name_Hk2, list)
    assert len(all_chain_name_Hk2) == 13546
    assert len(all_chain_name_BB) == 5151
    assert all_chain_name_Hk2[2685:2688] == ['A', 'A', 'A']
    assert all_chain_name_Hk2[13374:13380] == ['A', 'A', 'A', 'B', 'B', 'B']
    assert all_chain_name_Hk2[0] == 'A'
    assert all_chain_name_Hk2[-1] == 'B'
    assert all_chain_name_BB[2685:2688] == ['D', 'D', 'D']
    assert all_chain_name_BB[-515:-510] == ['F', 'F', 'A', 'A', 'A']
    assert all_chain_name_BB[0] == 'A'
    assert all_chain_name_BB[-1] == 'F'
    assert list_chain_name_Hk2 == ['A', 'A', 'A']
    assert list_chain_name_BB == ['A', 'A', 'A', 'A']

def test_get_chain_type_from_atom():

    all_chain_type_Hk2 = aux.get_chain_type_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_chain_type_BB = aux.get_chain_type_from_atom(molsys_BB.topology, skip_digestion=True)
    list_chain_type_Hk2 = aux.get_chain_type_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_chain_type_BB = aux.get_chain_type_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_chain_type_Hk2, list)
    assert len(all_chain_type_Hk2) == 13546
    assert len(all_chain_type_BB) == 5151
    assert all_chain_type_Hk2[2685:2688] == ['protein', 'protein', 'protein']
    assert all_chain_type_Hk2[13374:13380] == ['unknown', 'unknown', 'unknown', 'polysaccharide',
                                               'polysaccharide', 'polysaccharide']
    assert all_chain_type_Hk2[0] == 'protein'
    assert all_chain_type_Hk2[-1] == 'water'
    assert all_chain_type_BB[2685:2688] == ['protein', 'protein', 'protein']
    assert all_chain_type_BB[-515:-510] == ['protein', 'protein', 'water', 'water', 'water']
    assert all_chain_type_BB[0] == 'protein'
    assert all_chain_type_BB[-1] == 'water'
    assert list_chain_type_Hk2 == ['protein', 'protein', 'protein']
    assert list_chain_type_BB == ['protein', 'protein', 'protein', 'protein']

def test_get_bond_index_from_atom():

    all_bond_index_Hk2 = aux.get_bond_index_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_bond_index_BB = aux.get_bond_index_from_atom(molsys_BB.topology, skip_digestion=True)
    list_bond_index_Hk2 = aux.get_bond_index_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_bond_index_BB = aux.get_bond_index_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_bond_index_Hk2, list)
    assert len(all_bond_index_Hk2) == 13546
    assert len(all_bond_index_BB) == 5151
    assert all_bond_index_Hk2[2685:2688] == [[2728, 2729, 2730], [2729, 2731, 2732], [2731]]
    assert all_bond_index_Hk2[13374:13380] == [[], [], [], [13562, 13563, 13564], [13562, 13565, 13566],
                                               [13565, 13567, 13568]]
    assert all_bond_index_Hk2[0] == [0]
    assert all_bond_index_Hk2[-1] == []
    assert all_bond_index_BB[2685:2688] == [[2748], [2747, 2750], [2750]]
    assert all_bond_index_BB[-515:-510] == [[4737], [4736], [], [], []]
    assert all_bond_index_BB[0] == [0]
    assert all_bond_index_BB[-1] == []
    assert list_bond_index_Hk2 == [[2, 5], [5, 6, 7], [6]]
    assert list_bond_index_BB == [[10], [9, 12, 13], [12, 14], [13]]

def test_get_bond_type_from_atom():

    all_bond_type_Hk2 = aux.get_bond_type_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_bond_type_BB = aux.get_bond_type_from_atom(molsys_BB.topology, skip_digestion=True)
    list_bond_type_Hk2 = aux.get_bond_type_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_bond_type_BB = aux.get_bond_type_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_bond_type_Hk2, list)
    assert len(all_bond_type_Hk2) == 13546
    assert len(all_bond_type_BB) == 5151
    assert all_bond_type_Hk2[2685:2688] == [[None, None, None], [None, None, None], [None]]
    assert all_bond_type_Hk2[13374:13380] == [[], [], [], [None, None, None], [None, None, None], [None, None, None]]
    assert all_bond_type_Hk2[0] == [None]
    assert all_bond_type_Hk2[-1] == []
    assert all_bond_type_BB[2685:2688] == [[None], [None, None], [None]]
    assert all_bond_type_BB[-515:-510] == [[None], [None], [], [], []]
    assert all_bond_type_BB[0] == [None]
    assert all_bond_type_BB[-1] == []
    assert list_bond_type_Hk2 == [[None, None], [None, None, None], [None]]
    assert list_bond_type_BB == [[None], [None, None, None], [None, None], [None]]

def test_get_bonded_atoms_from_atom():

    all_bonded_atoms_Hk2 = aux.get_bonded_atoms_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_bonded_atoms_BB = aux.get_bonded_atoms_from_atom(molsys_BB.topology, skip_digestion=True)
    list_bonded_atoms_Hk2 = aux.get_bonded_atoms_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_bonded_atoms_BB = aux.get_bonded_atoms_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_bonded_atoms_Hk2, list)
    assert len(all_bonded_atoms_Hk2) == 13546
    assert len(all_bonded_atoms_BB) == 5151
    assert all_bonded_atoms_Hk2[2685:2688] == [[2684, 2686, 2688], [2685, 2687, 2691], [2686]]
    assert all_bonded_atoms_Hk2[13374:13380] == [[], [], [], [13378, 13383, 13387], [13377, 13379, 13384],
                                                 [13378, 13380, 13385]]
    assert all_bonded_atoms_Hk2[0] == [1]
    assert all_bonded_atoms_Hk2[-1] == []
    assert all_bonded_atoms_BB[2685:2688] == [[2684], [2683, 2687], [2686]]
    assert all_bonded_atoms_BB[-515:-510] == [[4635], [4634], [], [], []]
    assert all_bonded_atoms_BB[0] == [1]
    assert all_bonded_atoms_BB[-1] == []
    assert list_bonded_atoms_Hk2 == [[1, 5], [4, 6, 7], [5]]
    assert list_bonded_atoms_BB == [[9], [8, 12, 13], [11, 14], [11]]

def test_get_bonded_atom_pairs_from_atom():

    all_bonded_atom_pairs_Hk2 = aux.get_bonded_atom_pairs_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_bonded_atom_pairs_BB = aux.get_bonded_atom_pairs_from_atom(molsys_BB.topology, skip_digestion=True)
    list_bonded_atom_pairs_Hk2 = aux.get_bonded_atom_pairs_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_bonded_atom_pairs_BB = aux.get_bonded_atom_pairs_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_bonded_atom_pairs_Hk2, list)
    assert len(all_bonded_atom_pairs_Hk2) == 13618
    assert len(all_bonded_atom_pairs_BB) == 4738
    assert all_bonded_atom_pairs_Hk2[2685:2688] == [[2640, 2646], [2642, 2643], [2643, 2644]]
    assert all_bonded_atom_pairs_Hk2[13374:13380] == [[13175, 13176], [13176, 13177], [13176, 13178], [13179, 13180],
                                                      [13180, 13181], [13180, 13183]]
    assert all_bonded_atom_pairs_Hk2[0] == [0, 1]
    assert all_bonded_atom_pairs_Hk2[-1] == [13429, 13432]
    assert all_bonded_atom_pairs_BB[2685:2688] == [[2621, 2622], [2621, 2627], [2623, 2624]]
    assert all_bonded_atom_pairs_BB[-515:-510] == [[4134, 4137], [4135, 4136], [4135, 4141], [4137, 4138], [4138, 4139]]
    assert all_bonded_atom_pairs_BB[0] == [0, 1]
    assert all_bonded_atom_pairs_BB[-1] == [4635, 4636]
    assert list_bonded_atom_pairs_Hk2 == [[1, 4], [4, 5], [5, 6], [5, 7]]
    assert list_bonded_atom_pairs_BB == [[8, 11], [9, 10], [11, 12], [11, 13], [12, 14]]

def test_get_inner_bond_index_from_atom():

    all_inner_bond_index_Hk2 = aux.get_inner_bond_index_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_inner_bond_index_BB = aux.get_inner_bond_index_from_atom(molsys_BB.topology, skip_digestion=True)
    list_inner_bond_index_Hk2 = aux.get_inner_bond_index_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_inner_bond_index_BB = aux.get_inner_bond_index_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_inner_bond_index_Hk2, list)
    assert len(all_inner_bond_index_Hk2) == 13546
    assert len(all_inner_bond_index_BB) == 5151
    assert all_inner_bond_index_Hk2[2685:2688] == [[2728, 2729, 2730], [2729, 2731, 2732], [2731]]
    assert all_inner_bond_index_Hk2[13374:13380] == [[], [], [], [13562, 13563, 13564],
                                                     [13562, 13565, 13566], [13565, 13567, 13568]]
    assert all_inner_bond_index_Hk2[0] == [0]
    assert all_inner_bond_index_Hk2[-1] == []
    assert all_inner_bond_index_BB[2685:2688] == [[2748], [2747, 2750], [2750]]
    assert all_inner_bond_index_BB[-515:-510] == [[4737], [4736], [], [], []]
    assert all_inner_bond_index_BB[0] == [0]
    assert all_inner_bond_index_BB[-1] == []
    assert list_inner_bond_index_Hk2 == [[5], [5, 6], [6]]
    assert list_inner_bond_index_BB == [[], [12, 13], [12], [13]]


def test_get_inner_bonded_atoms_from_atom():

    all_inner_bonded_atoms_Hk2 = aux.get_inner_bonded_atoms_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_inner_bonded_atoms_BB = aux.get_inner_bonded_atoms_from_atom(molsys_BB.topology, skip_digestion=True)
    list_inner_bonded_atoms_Hk2 = aux.get_inner_bonded_atoms_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_inner_bonded_atoms_BB = aux.get_inner_bonded_atoms_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_inner_bonded_atoms_Hk2, list)
    assert len(all_inner_bonded_atoms_Hk2) == 13421
    assert len(all_inner_bonded_atoms_BB) == 4638
    assert all_inner_bonded_atoms_Hk2[2685:2688] == [[2684, 2686, 2688], [2685, 2687, 2691], [2685, 2689, 2690]]
    assert all_inner_bonded_atoms_Hk2[13374:13380] == [[13380], [13381, 13388], [13382], [13390, 13391, 13392],
                                                       [13389, 13393, 13394], [13389]]
    assert all_inner_bonded_atoms_Hk2[0] == [1]
    assert all_inner_bonded_atoms_Hk2[-1] == [13429]
    assert all_inner_bonded_atoms_BB[2685:2688] == [[2683, 2687], [2684], [2684, 2689]]
    assert all_inner_bonded_atoms_BB[-515:-510] == [[4121, 4125], [4122], [4122, 4129], [4124, 4126, 4127], [4125]]
    assert all_inner_bonded_atoms_BB[0] == [1]
    assert all_inner_bonded_atoms_BB[-1] == [4635]
    assert list_inner_bonded_atoms_Hk2 == [[5], [4, 6], [5]]
    assert list_inner_bonded_atoms_BB == [[], [12, 13], [11], [11]]


def test_get_inner_bonded_atom_pairs_from_atom():

    all_inner_bonded_atom_pairs_Hk2 = aux.get_inner_bonded_atom_pairs_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_inner_bonded_atom_pairs_BB = aux.get_inner_bonded_atom_pairs_from_atom(molsys_BB.topology, skip_digestion=True)
    list_inner_bonded_atom_pairs_Hk2 = aux.get_inner_bonded_atom_pairs_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_inner_bonded_atom_pairs_BB = aux.get_inner_bonded_atom_pairs_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_inner_bonded_atom_pairs_Hk2, list)
    assert len(all_inner_bonded_atom_pairs_Hk2) == 13618
    assert len(all_inner_bonded_atom_pairs_BB) == 4738
    assert all_inner_bonded_atom_pairs_Hk2[2685:2688] == [[2640, 2646], [2642, 2643], [2643, 2644]]
    assert all_inner_bonded_atom_pairs_Hk2[13374:13380] == [[13175, 13176], [13176, 13177], [13176, 13178],
                                                            [13179, 13180], [13180, 13181], [13180, 13183]]
    assert all_inner_bonded_atom_pairs_Hk2[0] == [0, 1]
    assert all_inner_bonded_atom_pairs_Hk2[-1] == [13429, 13432]
    assert all_inner_bonded_atom_pairs_BB[2685:2688] == [[2621, 2622], [2621, 2627], [2623, 2624]]
    assert all_inner_bonded_atom_pairs_BB[-515:-510] == [[4134, 4137], [4135, 4136], [4135, 4141], [4137, 4138], [4138, 4139]]
    assert all_inner_bonded_atom_pairs_BB[0] == [0, 1]
    assert all_inner_bonded_atom_pairs_BB[-1] == [4635, 4636]
    assert list_inner_bonded_atom_pairs_Hk2 == [[4, 5], [5, 6]]
    assert list_inner_bonded_atom_pairs_BB == [[11, 12], [11, 13]]


def test_get_n_atoms_from_atom():

    all_n_atoms_Hk2 = aux.get_n_atoms_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_n_atoms_BB = aux.get_n_atoms_from_atom(molsys_BB.topology, skip_digestion=True)
    list_n_atoms_Hk2 = aux.get_n_atoms_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_n_atoms_BB = aux.get_n_atoms_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_atoms_Hk2 == 13546
    assert all_n_atoms_BB ==  5151
    assert list_n_atoms_Hk2 == 3
    assert list_n_atoms_BB == 4

def test_get_n_groups_from_atom():

    all_n_groups_Hk2 = aux.get_n_groups_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_n_groups_BB = aux.get_n_groups_from_atom(molsys_BB.topology, skip_digestion=True)
    list_n_groups_Hk2 = aux.get_n_groups_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_n_groups_BB = aux.get_n_groups_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_groups_Hk2 == 1871
    assert all_n_groups_BB ==  1101
    assert list_n_groups_Hk2 == 1
    assert list_n_groups_BB == 1

def test_get_n_components_from_atom():

    all_n_components_Hk2 = aux.get_n_components_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_n_components_BB = aux.get_n_components_from_atom(molsys_BB.topology, skip_digestion=True)
    list_n_components_Hk2 = aux.get_n_components_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_n_components_BB = aux.get_n_components_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_components_Hk2 == 146
    assert all_n_components_BB ==  521
    assert list_n_components_Hk2 == 1
    assert list_n_components_BB == 1

def test_get_n_molecules_from_atom():

    all_n_molecules_Hk2 = aux.get_n_molecules_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_n_molecules_BB = aux.get_n_molecules_from_atom(molsys_BB.topology, skip_digestion=True)
    list_n_molecules_Hk2 = aux.get_n_molecules_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_n_molecules_BB = aux.get_n_molecules_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_molecules_Hk2 == 135
    assert all_n_molecules_BB ==  519
    assert list_n_molecules_Hk2 == 1
    assert list_n_molecules_BB == 1

def test_get_n_entities_from_atom():

    all_n_entities_Hk2 = aux.get_n_entities_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_n_entities_BB = aux.get_n_entities_from_atom(molsys_BB.topology, skip_digestion=True)
    list_n_entities_Hk2 = aux.get_n_entities_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_n_entities_BB = aux.get_n_entities_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_entities_Hk2 == 5
    assert all_n_entities_BB ==  3
    assert list_n_entities_Hk2 == 1
    assert list_n_entities_BB == 1

def test_get_n_chains_from_atom():

    all_n_chains_Hk2 = aux.get_n_chains_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_n_chains_BB = aux.get_n_chains_from_atom(molsys_BB.topology, skip_digestion=True)
    list_n_chains_Hk2 = aux.get_n_chains_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_n_chains_BB = aux.get_n_chains_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_chains_Hk2 == 40
    assert all_n_chains_BB ==  12
    assert list_n_chains_Hk2 == 1
    assert list_n_chains_BB == 1

def test_get_n_bonds_from_atom():

    all_n_bonds_Hk2 = aux.get_n_bonds_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_n_bonds_BB = aux.get_n_bonds_from_atom(molsys_BB.topology, skip_digestion=True)
    list_n_bonds_Hk2 = aux.get_n_bonds_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_n_bonds_BB = aux.get_n_bonds_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_bonds_Hk2 == 13618
    assert all_n_bonds_BB ==  4738
    assert list_n_bonds_Hk2 == 4
    assert list_n_bonds_BB == 5

def test_get_n_inner_bonds_from_atom():

    all_n_inner_bonds_Hk2 = aux.get_n_inner_bonds_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_n_inner_bonds_BB = aux.get_n_inner_bonds_from_atom(molsys_BB.topology, skip_digestion=True)
    list_n_inner_bonds_Hk2 = aux.get_n_inner_bonds_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_n_inner_bonds_BB = aux.get_n_inner_bonds_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_inner_bonds_Hk2 == 13618
    assert all_n_inner_bonds_BB ==  4738
    assert list_n_inner_bonds_Hk2 == 2
    assert list_n_inner_bonds_BB == 2

def test_get_n_amino_acids_from_atom():

    all_n_amino_acids_Hk2 = aux.get_n_amino_acids_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_n_amino_acids_BB = aux.get_n_amino_acids_from_atom(molsys_BB.topology, skip_digestion=True)
    list_n_amino_acids_Hk2 = aux.get_n_amino_acids_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_n_amino_acids_BB = aux.get_n_amino_acids_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_amino_acids_Hk2 == 1738
    assert all_n_amino_acids_BB ==  588
    assert list_n_amino_acids_Hk2 == 1
    assert list_n_amino_acids_BB == 1

def test_get_n_nucleotides_from_atom():

    all_n_nucleotides_Hk2 = aux.get_n_nucleotides_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_n_nucleotides_BB = aux.get_n_nucleotides_from_atom(molsys_BB.topology, skip_digestion=True)
    list_n_nucleotides_Hk2 = aux.get_n_nucleotides_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_n_nucleotides_BB = aux.get_n_nucleotides_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_nucleotides_Hk2 == 0
    assert all_n_nucleotides_BB ==  0
    assert list_n_nucleotides_Hk2 == 0
    assert list_n_nucleotides_BB == 0

def test_get_n_ions_from_atom():

    all_n_ions_Hk2 = aux.get_n_ions_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_n_ions_BB = aux.get_n_ions_from_atom(molsys_BB.topology, skip_digestion=True)
    list_n_ions_Hk2 = aux.get_n_ions_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_n_ions_BB = aux.get_n_ions_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_ions_Hk2 == 28
    assert all_n_ions_BB ==  0
    assert list_n_ions_Hk2 == 0
    assert list_n_ions_BB == 0

def test_get_n_waters_from_atom():

    all_n_waters_Hk2 = aux.get_n_waters_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_n_waters_BB = aux.get_n_waters_from_atom(molsys_BB.topology, skip_digestion=True)
    list_n_waters_Hk2 = aux.get_n_waters_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_n_waters_BB = aux.get_n_waters_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_waters_Hk2 == 97
    assert all_n_waters_BB ==  513
    assert list_n_waters_Hk2 == 0
    assert list_n_waters_BB == 0

def test_get_n_small_molecule_from_atom():

    all_n_small_molecules_Hk2 = aux.get_n_small_molecules_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_n_small_molecules_BB = aux.get_n_small_molecules_from_atom(molsys_BB.topology, skip_digestion=True)
    list_n_small_molecules_Hk2 = aux.get_n_small_molecules_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_n_small_molecules_BB = aux.get_n_small_molecules_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_small_molecules_Hk2 == 0
    assert all_n_small_molecules_BB ==  0
    assert list_n_small_molecules_Hk2 == 0
    assert list_n_small_molecules_BB == 0

def test_get_n_lipids_from_atom():

    all_n_lipids_Hk2 = aux.get_n_lipids_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_n_lipids_BB = aux.get_n_lipids_from_atom(molsys_BB.topology, skip_digestion=True)
    list_n_lipids_Hk2 = aux.get_n_lipids_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_n_lipids_BB = aux.get_n_lipids_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_lipids_Hk2 == 0
    assert all_n_lipids_BB ==  0
    assert list_n_lipids_Hk2 == 0
    assert list_n_lipids_BB == 0

def test_get_n_saccharides_from_atom():

    all_n_saccharides_Hk2 = aux.get_n_saccharides_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_n_saccharides_BB = aux.get_n_saccharides_from_atom(molsys_BB.topology, skip_digestion=True)
    list_n_saccharides_Hk2 = aux.get_n_saccharides_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_n_saccharides_BB = aux.get_n_saccharides_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_saccharides_Hk2 == 8
    assert all_n_saccharides_BB ==  0
    assert list_n_saccharides_Hk2 == 0
    assert list_n_saccharides_BB == 0

def test_get_n_peptides_from_atom():

    all_n_peptides_Hk2 = aux.get_n_peptides_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_n_peptides_BB = aux.get_n_peptides_from_atom(molsys_BB.topology, skip_digestion=True)
    list_n_peptides_Hk2 = aux.get_n_peptides_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_n_peptides_BB = aux.get_n_peptides_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_peptides_Hk2 == 0
    assert all_n_peptides_BB ==  0
    assert list_n_peptides_Hk2 == 0
    assert list_n_peptides_BB == 0

def test_get_n_proteins_from_atom():

    all_n_proteins_Hk2 = aux.get_n_proteins_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_n_proteins_BB = aux.get_n_proteins_from_atom(molsys_BB.topology, skip_digestion=True)
    list_n_proteins_Hk2 = aux.get_n_proteins_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_n_proteins_BB = aux.get_n_proteins_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_proteins_Hk2 == 2
    assert all_n_proteins_BB ==  6
    assert list_n_proteins_Hk2 == 1
    assert list_n_proteins_BB == 1

def test_get_n_dnas_from_atom():

    all_n_dnas_Hk2 = aux.get_n_dnas_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_n_dnas_BB = aux.get_n_dnas_from_atom(molsys_BB.topology, skip_digestion=True)
    list_n_dnas_Hk2 = aux.get_n_dnas_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_n_dnas_BB = aux.get_n_dnas_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_dnas_Hk2 == 0
    assert all_n_dnas_BB ==  0
    assert list_n_dnas_Hk2 == 0
    assert list_n_dnas_BB == 0

def test_get_n_rnas_from_atom():

    all_n_rnas_Hk2 = aux.get_n_rnas_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_n_rnas_BB = aux.get_n_rnas_from_atom(molsys_BB.topology, skip_digestion=True)
    list_n_rnas_Hk2 = aux.get_n_rnas_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_n_rnas_BB = aux.get_n_rnas_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_rnas_Hk2 == 0
    assert all_n_rnas_BB ==  0
    assert list_n_rnas_Hk2 == 0
    assert list_n_rnas_BB == 0

def test_get_n_polysaccharides_from_atom():

    all_n_polysaccharides_Hk2 = aux.get_n_polysaccharides_from_atom(molsys_Hk2.topology, skip_digestion=True)
    all_n_polysaccharides_BB = aux.get_n_polysaccharides_from_atom(molsys_BB.topology, skip_digestion=True)
    list_n_polysaccharides_Hk2 = aux.get_n_polysaccharides_from_atom(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_n_polysaccharides_BB = aux.get_n_polysaccharides_from_atom(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_polysaccharides_Hk2 == 8
    assert all_n_polysaccharides_BB ==  0
    assert list_n_polysaccharides_Hk2 == 0
    assert list_n_polysaccharides_BB == 0


# From group


def test_get_atom_index_from_group():

    all_atom_index_Hk2 = aux.get_atom_index_from_group(molsys_Hk2.topology, skip_digestion=True)
    all_atom_index_BB = aux.get_atom_index_from_group(molsys_BB.topology, skip_digestion=True)
    list_atom_index_Hk2 = aux.get_atom_index_from_group(molsys_Hk2.topology, indices=[4,5,6], skip_digestion=True)
    list_atom_index_BB = aux.get_atom_index_from_group(molsys_BB.topology, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_atom_index_Hk2, list)
    assert len(all_atom_index_Hk2) == 1871
    assert len(all_atom_index_BB) == 1101
    assert all_atom_index_Hk2[344:347] == [[2678, 2679, 2680, 2681, 2682, 2683],
                                           [2684, 2685, 2686, 2687, 2688, 2689, 2690],
                                           [2691, 2692, 2693, 2694, 2695]]
    assert all_atom_index_Hk2[1750:1755] == [[13373], [13374], [13375], [13376],
                                             [13377, 13378, 13379, 13380, 13381, 13382, 13383,
                                              13384, 13385, 13386, 13387, 13388]]
    assert all_atom_index_Hk2[0] == [0, 1, 2, 3, 4, 5, 6, 7]
    assert all_atom_index_Hk2[-1] == [13545]
    assert all_atom_index_BB[385:388] == [[3070, 3071, 3072, 3073, 3074, 3075, 3076, 3077],
                                          [3078, 3079, 3080, 3081, 3082],
                                          [3083, 3084, 3085, 3086, 3087, 3088, 3089, 3090]] 
    assert all_atom_index_BB[586:592] == [[4624, 4625, 4626, 4627, 4628, 4629, 4630, 4631],
                                          [4632, 4633, 4634, 4635, 4636, 4637],
                                          [4638], [4639], [4640], [4641]]
    assert all_atom_index_BB[0] == [0, 1, 2, 3, 4, 5, 6]
    assert all_atom_index_BB[-1] == [5150]
    assert list_atom_index_Hk2 == [[33, 34, 35, 36, 37, 38, 39, 40, 41],
                                   [42, 43, 44, 45, 46, 47, 48],
                                   [49, 50, 51, 52, 53, 54, 55, 56]]
    assert list_atom_index_BB == [[73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84],
                                  [85, 86, 87, 88, 89, 90, 91, 92],
                                  [93, 94, 95, 96, 97, 98, 99, 100, 101],
                                  [102, 103, 104, 105, 106, 107, 108]]








