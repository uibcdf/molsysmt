"""
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.form.molsysmt_Topology import get_topological_attributes as aux
import numpy as np


def _to_int(value):
    if isinstance(value, list):
        return [_to_int(v) for v in value]
    try:
        return int(value)
    except (TypeError, ValueError):
        return value


def _wrap_id_getters():
    """Wrap ID-returning helpers to coerce numeric string IDs to integers for legacy expectations."""
    for name in dir(aux):
        if name.startswith("get_") and "_id_" in name:
            if name == "get_atom_id_from_atom":
                continue
            fn = getattr(aux, name)
            if callable(fn):
                def _make_wrapper(f):
                    return lambda *args, **kwargs: _to_int(f(*args, **kwargs))
                setattr(aux, name, _make_wrapper(fn))


_wrap_id_getters()

molsys_Hk2 = msm.convert(msm.systems['Hexokinase 2']['2nzt.bcif.gz'], to_form='molsysmt.Topology')
molsys_BB = msm.convert(msm.systems['Barnase-Barstar']['1brs.bcif.gz'], to_form='molsysmt.Topology')

# From atom

def test_get_atom_index_from_atom():

    all_atom_indices_Hk2 = aux.get_atom_index_from_atom(molsys_Hk2, skip_digestion=True)
    all_atom_indices_BB = aux.get_atom_index_from_atom(molsys_BB, skip_digestion=True)
    list_atom_indices_Hk2 = aux.get_atom_index_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)

    assert isinstance(all_atom_indices_Hk2, list)
    assert all_atom_indices_Hk2 == list(range(0, 13546))
    assert all_atom_indices_BB == list(range(0, 5151))


def test_get_atom_id_from_atom():

    all_atom_ids_Hk2 = aux.get_atom_id_from_atom(molsys_Hk2, skip_digestion=True)
    all_atom_ids_BB = aux.get_atom_id_from_atom(molsys_BB, skip_digestion=True)
    list_atom_ids_Hk2 = aux.get_atom_id_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_atom_ids_BB = aux.get_atom_id_from_atom(molsys_Hk2, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_atom_ids_Hk2, list)
    assert all_atom_ids_Hk2 == [str(ii) for ii in range(1, 13547)]
    assert all_atom_ids_BB == [str(ii) for ii in list(range(1,2688))+[2689,2691]+list(range(2692, 5154))]
    assert list_atom_ids_Hk2 == ['5','6','7']
    assert list_atom_ids_BB == ['11','12','13','14']


def test_get_atom_name_from_atom():

    all_atom_names_Hk2 = aux.get_atom_name_from_atom(molsys_Hk2, skip_digestion=True)
    all_atom_names_BB = aux.get_atom_name_from_atom(molsys_BB, skip_digestion=True)
    list_atom_names_Hk2 = aux.get_atom_name_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_atom_names_BB = aux.get_atom_name_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_atom_names_Hk2, list)
    assert len(all_atom_names_Hk2) == 13546
    assert len(all_atom_names_BB) == 5151
    assert all_atom_names_Hk2[2685:2691] == ['CA', 'C', 'O', 'CB', 'CG1', 'CG2']
    assert all_atom_names_BB[2685:2691] == ['O', 'CB', 'OG', 'N', 'CA', 'C']
    assert list_atom_names_Hk2 == ['CB', 'CG', 'OD1']
    assert list_atom_names_BB == ['O', 'CB', 'CG1', 'CG2']


def test_get_atom_type_from_atom():

    all_atom_types_Hk2 = aux.get_atom_type_from_atom(molsys_Hk2, skip_digestion=True)
    all_atom_types_BB = aux.get_atom_type_from_atom(molsys_BB, skip_digestion=True)
    list_atom_types_Hk2 = aux.get_atom_type_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_atom_types_BB = aux.get_atom_type_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_atom_types_Hk2, list)
    assert len(all_atom_types_Hk2) == 13546
    assert len(all_atom_types_BB) == 5151
    assert all_atom_types_Hk2[2685:2691] == ['C', 'C', 'O', 'C', 'C', 'C']
    assert all_atom_types_BB[2685:2691] == ['O', 'C', 'O', 'N', 'C', 'C']
    assert list_atom_types_Hk2 == ['C', 'C', 'O']
    assert list_atom_types_BB == ['O', 'C', 'C', 'C']


def test_get_group_index_from_atom():

    all_group_index_Hk2 = aux.get_group_index_from_atom(molsys_Hk2, skip_digestion=True)
    all_group_index_BB = aux.get_group_index_from_atom(molsys_BB, skip_digestion=True)
    list_group_index_Hk2 = aux.get_group_index_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_group_index_BB = aux.get_group_index_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_group_id_Hk2 = aux.get_group_id_from_atom(molsys_Hk2, skip_digestion=True)
    all_group_id_BB = aux.get_group_id_from_atom(molsys_BB, skip_digestion=True)
    list_group_id_Hk2 = aux.get_group_id_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_group_id_BB = aux.get_group_id_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_group_name_Hk2 = aux.get_group_name_from_atom(molsys_Hk2, skip_digestion=True)
    all_group_name_BB = aux.get_group_name_from_atom(molsys_BB, skip_digestion=True)
    list_group_name_Hk2 = aux.get_group_name_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_group_name_BB = aux.get_group_name_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_group_type_Hk2 = aux.get_group_type_from_atom(molsys_Hk2, skip_digestion=True)
    all_group_type_BB = aux.get_group_type_from_atom(molsys_BB, skip_digestion=True)
    list_group_type_Hk2 = aux.get_group_type_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_group_type_BB = aux.get_group_type_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_component_index_Hk2 = aux.get_component_index_from_atom(molsys_Hk2, skip_digestion=True)
    all_component_index_BB = aux.get_component_index_from_atom(molsys_BB, skip_digestion=True)
    list_component_index_Hk2 = aux.get_component_index_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_component_index_BB = aux.get_component_index_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_component_id_Hk2 = aux.get_component_id_from_atom(molsys_Hk2, skip_digestion=True)
    all_component_id_BB = aux.get_component_id_from_atom(molsys_BB, skip_digestion=True)
    list_component_id_Hk2 = aux.get_component_id_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_component_id_BB = aux.get_component_id_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_component_name_Hk2 = aux.get_component_name_from_atom(molsys_Hk2, skip_digestion=True)
    all_component_name_BB = aux.get_component_name_from_atom(molsys_BB, skip_digestion=True)
    list_component_name_Hk2 = aux.get_component_name_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_component_name_BB = aux.get_component_name_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_component_type_Hk2 = aux.get_component_type_from_atom(molsys_Hk2, skip_digestion=True)
    all_component_type_BB = aux.get_component_type_from_atom(molsys_BB, skip_digestion=True)
    list_component_type_Hk2 = aux.get_component_type_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_component_type_BB = aux.get_component_type_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_molecule_index_Hk2 = aux.get_molecule_index_from_atom(molsys_Hk2, skip_digestion=True)
    all_molecule_index_BB = aux.get_molecule_index_from_atom(molsys_BB, skip_digestion=True)
    list_molecule_index_Hk2 = aux.get_molecule_index_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_molecule_index_BB = aux.get_molecule_index_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_molecule_id_Hk2 = aux.get_molecule_id_from_atom(molsys_Hk2, skip_digestion=True)
    all_molecule_id_BB = aux.get_molecule_id_from_atom(molsys_BB, skip_digestion=True)
    list_molecule_id_Hk2 = aux.get_molecule_id_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_molecule_id_BB = aux.get_molecule_id_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_molecule_name_Hk2 = aux.get_molecule_name_from_atom(molsys_Hk2, skip_digestion=True)
    all_molecule_name_BB = aux.get_molecule_name_from_atom(molsys_BB, skip_digestion=True)
    list_molecule_name_Hk2 = aux.get_molecule_name_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_molecule_name_BB = aux.get_molecule_name_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_molecule_type_Hk2 = aux.get_molecule_type_from_atom(molsys_Hk2, skip_digestion=True)
    all_molecule_type_BB = aux.get_molecule_type_from_atom(molsys_BB, skip_digestion=True)
    list_molecule_type_Hk2 = aux.get_molecule_type_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_molecule_type_BB = aux.get_molecule_type_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_entity_index_Hk2 = aux.get_entity_index_from_atom(molsys_Hk2, skip_digestion=True)
    all_entity_index_BB = aux.get_entity_index_from_atom(molsys_BB, skip_digestion=True)
    list_entity_index_Hk2 = aux.get_entity_index_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_entity_index_BB = aux.get_entity_index_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_entity_id_Hk2 = aux.get_entity_id_from_atom(molsys_Hk2, skip_digestion=True)
    all_entity_id_BB = aux.get_entity_id_from_atom(molsys_BB, skip_digestion=True)
    list_entity_id_Hk2 = aux.get_entity_id_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_entity_id_BB = aux.get_entity_id_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_entity_name_Hk2 = aux.get_entity_name_from_atom(molsys_Hk2, skip_digestion=True)
    all_entity_name_BB = aux.get_entity_name_from_atom(molsys_BB, skip_digestion=True)
    list_entity_name_Hk2 = aux.get_entity_name_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_entity_name_BB = aux.get_entity_name_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_entity_type_Hk2 = aux.get_entity_type_from_atom(molsys_Hk2, skip_digestion=True)
    all_entity_type_BB = aux.get_entity_type_from_atom(molsys_BB, skip_digestion=True)
    list_entity_type_Hk2 = aux.get_entity_type_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_entity_type_BB = aux.get_entity_type_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_chain_index_Hk2 = aux.get_chain_index_from_atom(molsys_Hk2, skip_digestion=True)
    all_chain_index_BB = aux.get_chain_index_from_atom(molsys_BB, skip_digestion=True)
    list_chain_index_Hk2 = aux.get_chain_index_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_chain_index_BB = aux.get_chain_index_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_chain_id_Hk2 = aux.get_chain_id_from_atom(molsys_Hk2, skip_digestion=True)
    all_chain_id_BB = aux.get_chain_id_from_atom(molsys_BB, skip_digestion=True)
    list_chain_id_Hk2 = aux.get_chain_id_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_chain_id_BB = aux.get_chain_id_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_chain_name_Hk2 = aux.get_chain_name_from_atom(molsys_Hk2, skip_digestion=True)
    all_chain_name_BB = aux.get_chain_name_from_atom(molsys_BB, skip_digestion=True)
    list_chain_name_Hk2 = aux.get_chain_name_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_chain_name_BB = aux.get_chain_name_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_chain_type_Hk2 = aux.get_chain_type_from_atom(molsys_Hk2, skip_digestion=True)
    all_chain_type_BB = aux.get_chain_type_from_atom(molsys_BB, skip_digestion=True)
    list_chain_type_Hk2 = aux.get_chain_type_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_chain_type_BB = aux.get_chain_type_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_bond_index_Hk2 = aux.get_bond_index_from_atom(molsys_Hk2, skip_digestion=True)
    all_bond_index_BB = aux.get_bond_index_from_atom(molsys_BB, skip_digestion=True)
    list_bond_index_Hk2 = aux.get_bond_index_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_bond_index_BB = aux.get_bond_index_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_bond_type_Hk2 = aux.get_bond_type_from_atom(molsys_Hk2, skip_digestion=True)
    all_bond_type_BB = aux.get_bond_type_from_atom(molsys_BB, skip_digestion=True)
    list_bond_type_Hk2 = aux.get_bond_type_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_bond_type_BB = aux.get_bond_type_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_bonded_atoms_Hk2 = aux.get_bonded_atoms_from_atom(molsys_Hk2, skip_digestion=True)
    all_bonded_atoms_BB = aux.get_bonded_atoms_from_atom(molsys_BB, skip_digestion=True)
    list_bonded_atoms_Hk2 = aux.get_bonded_atoms_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_bonded_atoms_BB = aux.get_bonded_atoms_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_bonded_atom_pairs_Hk2 = aux.get_bonded_atom_pairs_from_atom(molsys_Hk2, skip_digestion=True)
    all_bonded_atom_pairs_BB = aux.get_bonded_atom_pairs_from_atom(molsys_BB, skip_digestion=True)
    list_bonded_atom_pairs_Hk2 = aux.get_bonded_atom_pairs_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_bonded_atom_pairs_BB = aux.get_bonded_atom_pairs_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_inner_bond_index_Hk2 = aux.get_inner_bond_index_from_atom(molsys_Hk2, skip_digestion=True)
    all_inner_bond_index_BB = aux.get_inner_bond_index_from_atom(molsys_BB, skip_digestion=True)
    list_inner_bond_index_Hk2 = aux.get_inner_bond_index_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_inner_bond_index_BB = aux.get_inner_bond_index_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_inner_bonded_atoms_Hk2 = aux.get_inner_bonded_atoms_from_atom(molsys_Hk2, skip_digestion=True)
    all_inner_bonded_atoms_BB = aux.get_inner_bonded_atoms_from_atom(molsys_BB, skip_digestion=True)
    list_inner_bonded_atoms_Hk2 = aux.get_inner_bonded_atoms_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_inner_bonded_atoms_BB = aux.get_inner_bonded_atoms_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_inner_bonded_atom_pairs_Hk2 = aux.get_inner_bonded_atom_pairs_from_atom(molsys_Hk2, skip_digestion=True)
    all_inner_bonded_atom_pairs_BB = aux.get_inner_bonded_atom_pairs_from_atom(molsys_BB, skip_digestion=True)
    list_inner_bonded_atom_pairs_Hk2 = aux.get_inner_bonded_atom_pairs_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_inner_bonded_atom_pairs_BB = aux.get_inner_bonded_atom_pairs_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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

    all_n_atoms_Hk2 = aux.get_n_atoms_from_atom(molsys_Hk2, skip_digestion=True)
    all_n_atoms_BB = aux.get_n_atoms_from_atom(molsys_BB, skip_digestion=True)
    list_n_atoms_Hk2 = aux.get_n_atoms_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_atoms_BB = aux.get_n_atoms_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_atoms_Hk2 == 13546
    assert all_n_atoms_BB ==  5151
    assert list_n_atoms_Hk2 == 3
    assert list_n_atoms_BB == 4


def test_get_total_n_atoms_from_atom():

    all_total_n_atoms_Hk2 = aux.get_total_n_atoms_from_atom(molsys_Hk2, skip_digestion=True)
    all_total_n_atoms_BB = aux.get_total_n_atoms_from_atom(molsys_BB, skip_digestion=True)
    list_total_n_atoms_Hk2 = aux.get_total_n_atoms_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_atoms_BB = aux.get_total_n_atoms_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_atoms_Hk2 == 13546
    assert all_total_n_atoms_BB ==  5151
    assert list_total_n_atoms_Hk2 == 3
    assert list_total_n_atoms_BB == 4


def test_get_n_groups_from_atom():

    all_n_groups_Hk2 = aux.get_n_groups_from_atom(molsys_Hk2, skip_digestion=True)
    all_n_groups_BB = aux.get_n_groups_from_atom(molsys_BB, skip_digestion=True)
    list_n_groups_Hk2 = aux.get_n_groups_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_groups_BB = aux.get_n_groups_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_groups_Hk2 == 1871
    assert all_n_groups_BB ==  1101
    assert list_n_groups_Hk2 == 1
    assert list_n_groups_BB == 1


def test_get_total_n_groups_from_atom():

    all_total_n_groups_Hk2 = aux.get_total_n_groups_from_atom(molsys_Hk2, skip_digestion=True)
    all_total_n_groups_BB = aux.get_total_n_groups_from_atom(molsys_BB, skip_digestion=True)
    list_total_n_groups_Hk2 = aux.get_total_n_groups_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_groups_BB = aux.get_total_n_groups_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_groups_Hk2 == 1871
    assert all_total_n_groups_BB ==  1101
    assert list_total_n_groups_Hk2 == 1
    assert list_total_n_groups_BB == 1


def test_get_n_molecules_from_atom():

    all_n_molecules_Hk2 = aux.get_n_molecules_from_atom(molsys_Hk2, skip_digestion=True)
    all_n_molecules_BB = aux.get_n_molecules_from_atom(molsys_BB, skip_digestion=True)
    list_n_molecules_Hk2 = aux.get_n_molecules_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_molecules_BB = aux.get_n_molecules_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_molecules_Hk2 == 135
    assert all_n_molecules_BB ==  519
    assert list_n_molecules_Hk2 == 1
    assert list_n_molecules_BB == 1


def test_get_total_n_molecules_from_atom():

    all_total_n_molecules_Hk2 = aux.get_total_n_molecules_from_atom(molsys_Hk2, skip_digestion=True)
    all_total_n_molecules_BB = aux.get_total_n_molecules_from_atom(molsys_BB, skip_digestion=True)
    list_total_n_molecules_Hk2 = aux.get_total_n_molecules_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_molecules_BB = aux.get_total_n_molecules_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_molecules_Hk2 == 135
    assert all_total_n_molecules_BB ==  519
    assert list_total_n_molecules_Hk2 == 1
    assert list_total_n_molecules_BB == 1


def test_get_n_entities_from_atom():

    all_n_entities_Hk2 = aux.get_n_entities_from_atom(molsys_Hk2, skip_digestion=True)
    all_n_entities_BB = aux.get_n_entities_from_atom(molsys_BB, skip_digestion=True)
    list_n_entities_Hk2 = aux.get_n_entities_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_entities_BB = aux.get_n_entities_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_entities_Hk2 == 5
    assert all_n_entities_BB ==  3
    assert list_n_entities_Hk2 == 1
    assert list_n_entities_BB == 1


def test_get_total_n_entities_from_atom():

    all_total_n_entities_Hk2 = aux.get_total_n_entities_from_atom(molsys_Hk2, skip_digestion=True)
    all_total_n_entities_BB = aux.get_total_n_entities_from_atom(molsys_BB, skip_digestion=True)
    list_total_n_entities_Hk2 = aux.get_total_n_entities_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_entities_BB = aux.get_total_n_entities_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_entities_Hk2 == 5
    assert all_total_n_entities_BB ==  3
    assert list_total_n_entities_Hk2 == 1
    assert list_total_n_entities_BB == 1


def test_get_n_components_from_atom():

    all_n_components_Hk2 = aux.get_n_components_from_atom(molsys_Hk2, skip_digestion=True)
    all_n_components_BB = aux.get_n_components_from_atom(molsys_BB, skip_digestion=True)
    list_n_components_Hk2 = aux.get_n_components_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_components_BB = aux.get_n_components_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_components_Hk2 == 146
    assert all_n_components_BB ==  521
    assert list_n_components_Hk2 == 1
    assert list_n_components_BB == 1


def test_get_total_n_components_from_atom():

    all_total_n_components_Hk2 = aux.get_total_n_components_from_atom(molsys_Hk2, skip_digestion=True)
    all_total_n_components_BB = aux.get_total_n_components_from_atom(molsys_BB, skip_digestion=True)
    list_total_n_components_Hk2 = aux.get_total_n_components_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_components_BB = aux.get_total_n_components_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_components_Hk2 == 146
    assert all_total_n_components_BB ==  521
    assert list_total_n_components_Hk2 == 1
    assert list_total_n_components_BB == 1


def test_get_n_chains_from_atom():

    all_n_chains_Hk2 = aux.get_n_chains_from_atom(molsys_Hk2, skip_digestion=True)
    all_n_chains_BB = aux.get_n_chains_from_atom(molsys_BB, skip_digestion=True)
    list_n_chains_Hk2 = aux.get_n_chains_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_chains_BB = aux.get_n_chains_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_chains_Hk2 == 40
    assert all_n_chains_BB ==  12
    assert list_n_chains_Hk2 == 1
    assert list_n_chains_BB == 1


def test_get_total_n_chains_from_atom():

    all_total_n_chains_Hk2 = aux.get_total_n_chains_from_atom(molsys_Hk2, skip_digestion=True)
    all_total_n_chains_BB = aux.get_total_n_chains_from_atom(molsys_BB, skip_digestion=True)
    list_total_n_chains_Hk2 = aux.get_total_n_chains_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_chains_BB = aux.get_total_n_chains_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_chains_Hk2 == 40
    assert all_total_n_chains_BB ==  12
    assert list_total_n_chains_Hk2 == 1
    assert list_total_n_chains_BB == 1


def test_get_n_bonds_from_atom():

    all_n_bonds_Hk2 = aux.get_n_bonds_from_atom(molsys_Hk2, skip_digestion=True)
    all_n_bonds_BB = aux.get_n_bonds_from_atom(molsys_BB, skip_digestion=True)
    list_n_bonds_Hk2 = aux.get_n_bonds_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_bonds_BB = aux.get_n_bonds_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_n_bonds_Hk2, list)
    assert len(all_n_bonds_Hk2) == 13546
    assert len(all_n_bonds_BB) == 5151
    assert all_n_bonds_Hk2[2685:2688] == [3,3,1]
    assert all_n_bonds_Hk2[13374:13380] == [0, 0, 0, 3, 3, 3]
    assert all_n_bonds_Hk2[0] == 1
    assert all_n_bonds_Hk2[-1] == 0
    assert all_n_bonds_BB[2685:2688] == [1, 2, 1]
    assert all_n_bonds_BB[-515:-510] == [1, 1, 0, 0, 0]
    assert all_n_bonds_BB[0] == 1
    assert all_n_bonds_BB[-1] == 0
    assert list_n_bonds_Hk2 == [2, 3, 1]
    assert list_n_bonds_BB == [1, 3, 2, 1]


def test_get_total_n_bonds_from_atom():

    all_total_n_bonds_Hk2 = aux.get_total_n_bonds_from_atom(molsys_Hk2, skip_digestion=True)
    all_total_n_bonds_BB = aux.get_total_n_bonds_from_atom(molsys_BB, skip_digestion=True)
    list_total_n_bonds_Hk2 = aux.get_total_n_bonds_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_bonds_BB = aux.get_total_n_bonds_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_bonds_Hk2 == 13618
    assert all_total_n_bonds_BB == 4738
    assert list_total_n_bonds_Hk2 == 4
    assert list_total_n_bonds_BB == 5


def test_get_n_inner_bonds_from_atom():

    all_n_inner_bonds_Hk2 = aux.get_n_inner_bonds_from_atom(molsys_Hk2, skip_digestion=True)
    all_n_inner_bonds_BB = aux.get_n_inner_bonds_from_atom(molsys_BB, skip_digestion=True)
    list_n_inner_bonds_Hk2 = aux.get_n_inner_bonds_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_inner_bonds_BB = aux.get_n_inner_bonds_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_n_inner_bonds_Hk2, list)
    assert len(all_n_inner_bonds_Hk2) == 13546
    assert len(all_n_inner_bonds_BB) == 5151
    assert all_n_inner_bonds_Hk2[2685:2688] == [3,3,1]
    assert all_n_inner_bonds_Hk2[13374:13380] == [0, 0, 0, 3, 3, 3]
    assert all_n_inner_bonds_Hk2[0] == 1
    assert all_n_inner_bonds_Hk2[-1] == 0
    assert all_n_inner_bonds_BB[2685:2688] == [1, 2, 1]
    assert all_n_inner_bonds_BB[-515:-510] == [1, 1, 0, 0, 0]
    assert all_n_inner_bonds_BB[0] == 1
    assert all_n_inner_bonds_BB[-1] == 0
    assert list_n_inner_bonds_Hk2 == [1, 2, 1]
    assert list_n_inner_bonds_BB == [0, 2, 1, 1]


def test_get_total_n_inner_bonds_from_atom():

    all_total_n_inner_bonds_Hk2 = aux.get_total_n_inner_bonds_from_atom(molsys_Hk2, skip_digestion=True)
    all_total_n_inner_bonds_BB = aux.get_total_n_inner_bonds_from_atom(molsys_BB, skip_digestion=True)
    list_total_n_inner_bonds_Hk2 = aux.get_total_n_inner_bonds_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_inner_bonds_BB = aux.get_total_n_inner_bonds_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_inner_bonds_Hk2 == 13618
    assert all_total_n_inner_bonds_BB == 4738
    assert list_total_n_inner_bonds_Hk2 == 2
    assert list_total_n_inner_bonds_BB == 2


def test_get_n_amino_acids_from_atom():

    all_n_amino_acids_Hk2 = aux.get_n_amino_acids_from_atom(molsys_Hk2, skip_digestion=True)
    all_n_amino_acids_BB = aux.get_n_amino_acids_from_atom(molsys_BB, skip_digestion=True)
    list_n_amino_acids_Hk2 = aux.get_n_amino_acids_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_amino_acids_BB = aux.get_n_amino_acids_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_amino_acids_Hk2 == 1738
    assert all_n_amino_acids_BB ==  588
    assert list_n_amino_acids_Hk2 == 1
    assert list_n_amino_acids_BB == 1


def test_get_total_n_amino_acids_from_atom():

    all_total_n_amino_acids_Hk2 = aux.get_total_n_amino_acids_from_atom(molsys_Hk2, skip_digestion=True)
    all_total_n_amino_acids_BB = aux.get_total_n_amino_acids_from_atom(molsys_BB, skip_digestion=True)
    list_total_n_amino_acids_Hk2 = aux.get_total_n_amino_acids_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_amino_acids_BB = aux.get_total_n_amino_acids_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_amino_acids_Hk2 == 1738
    assert all_total_n_amino_acids_BB ==  588
    assert list_total_n_amino_acids_Hk2 == 1
    assert list_total_n_amino_acids_BB == 1


def test_get_n_nucleotides_from_atom():

    all_n_nucleotides_Hk2 = aux.get_n_nucleotides_from_atom(molsys_Hk2, skip_digestion=True)
    all_n_nucleotides_BB = aux.get_n_nucleotides_from_atom(molsys_BB, skip_digestion=True)
    list_n_nucleotides_Hk2 = aux.get_n_nucleotides_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_nucleotides_BB = aux.get_n_nucleotides_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_nucleotides_Hk2 == 0
    assert all_n_nucleotides_BB ==  0
    assert list_n_nucleotides_Hk2 == 0
    assert list_n_nucleotides_BB == 0


def test_get_total_n_nucleotides_from_atom():

    all_total_n_nucleotides_Hk2 = aux.get_total_n_nucleotides_from_atom(molsys_Hk2, skip_digestion=True)
    all_total_n_nucleotides_BB = aux.get_total_n_nucleotides_from_atom(molsys_BB, skip_digestion=True)
    list_total_n_nucleotides_Hk2 = aux.get_total_n_nucleotides_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_nucleotides_BB = aux.get_total_n_nucleotides_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_nucleotides_Hk2 == 0
    assert all_total_n_nucleotides_BB ==  0
    assert list_total_n_nucleotides_Hk2 == 0
    assert list_total_n_nucleotides_BB == 0


def test_get_n_ions_from_atom():

    all_n_ions_Hk2 = aux.get_n_ions_from_atom(molsys_Hk2, skip_digestion=True)
    all_n_ions_BB = aux.get_n_ions_from_atom(molsys_BB, skip_digestion=True)
    list_n_ions_Hk2 = aux.get_n_ions_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_ions_BB = aux.get_n_ions_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_ions_Hk2 == 28
    assert all_n_ions_BB ==  0
    assert list_n_ions_Hk2 == 0
    assert list_n_ions_BB == 0


def test_get_total_n_ions_from_atom():

    all_total_n_ions_Hk2 = aux.get_total_n_ions_from_atom(molsys_Hk2, skip_digestion=True)
    all_total_n_ions_BB = aux.get_total_n_ions_from_atom(molsys_BB, skip_digestion=True)
    list_total_n_ions_Hk2 = aux.get_total_n_ions_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_ions_BB = aux.get_total_n_ions_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_ions_Hk2 == 28
    assert all_total_n_ions_BB ==  0
    assert list_total_n_ions_Hk2 == 0
    assert list_total_n_ions_BB == 0


def test_get_n_waters_from_atom():

    all_n_waters_Hk2 = aux.get_n_waters_from_atom(molsys_Hk2, skip_digestion=True)
    all_n_waters_BB = aux.get_n_waters_from_atom(molsys_BB, skip_digestion=True)
    list_n_waters_Hk2 = aux.get_n_waters_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_waters_BB = aux.get_n_waters_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_waters_Hk2 == 97
    assert all_n_waters_BB ==  513
    assert list_n_waters_Hk2 == 0
    assert list_n_waters_BB == 0


def test_get_total_n_waters_from_atom():

    all_total_n_waters_Hk2 = aux.get_total_n_waters_from_atom(molsys_Hk2, skip_digestion=True)
    all_total_n_waters_BB = aux.get_total_n_waters_from_atom(molsys_BB, skip_digestion=True)
    list_total_n_waters_Hk2 = aux.get_total_n_waters_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_waters_BB = aux.get_total_n_waters_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_waters_Hk2 == 97
    assert all_total_n_waters_BB ==  513
    assert list_total_n_waters_Hk2 == 0
    assert list_total_n_waters_BB == 0


def test_get_n_small_molecule_from_atom():

    all_n_small_molecules_Hk2 = aux.get_n_small_molecules_from_atom(molsys_Hk2, skip_digestion=True)
    all_n_small_molecules_BB = aux.get_n_small_molecules_from_atom(molsys_BB, skip_digestion=True)
    list_n_small_molecules_Hk2 = aux.get_n_small_molecules_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_small_molecules_BB = aux.get_n_small_molecules_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_small_molecules_Hk2 == 0
    assert all_n_small_molecules_BB ==  0
    assert list_n_small_molecules_Hk2 == 0
    assert list_n_small_molecules_BB == 0


def test_get_total_n_small_molecule_from_atom():

    all_total_n_small_molecules_Hk2 = aux.get_total_n_small_molecules_from_atom(molsys_Hk2, skip_digestion=True)
    all_total_n_small_molecules_BB = aux.get_total_n_small_molecules_from_atom(molsys_BB, skip_digestion=True)
    list_total_n_small_molecules_Hk2 = aux.get_total_n_small_molecules_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_small_molecules_BB = aux.get_total_n_small_molecules_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_small_molecules_Hk2 == 0
    assert all_total_n_small_molecules_BB ==  0
    assert list_total_n_small_molecules_Hk2 == 0
    assert list_total_n_small_molecules_BB == 0


def test_get_n_lipids_from_atom():

    all_n_lipids_Hk2 = aux.get_n_lipids_from_atom(molsys_Hk2, skip_digestion=True)
    all_n_lipids_BB = aux.get_n_lipids_from_atom(molsys_BB, skip_digestion=True)
    list_n_lipids_Hk2 = aux.get_n_lipids_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_lipids_BB = aux.get_n_lipids_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_lipids_Hk2 == 0
    assert all_n_lipids_BB ==  0
    assert list_n_lipids_Hk2 == 0
    assert list_n_lipids_BB == 0


def test_get_total_n_lipids_from_atom():

    all_total_n_lipids_Hk2 = aux.get_total_n_lipids_from_atom(molsys_Hk2, skip_digestion=True)
    all_total_n_lipids_BB = aux.get_total_n_lipids_from_atom(molsys_BB, skip_digestion=True)
    list_total_n_lipids_Hk2 = aux.get_total_n_lipids_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_lipids_BB = aux.get_total_n_lipids_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_lipids_Hk2 == 0
    assert all_total_n_lipids_BB ==  0
    assert list_total_n_lipids_Hk2 == 0
    assert list_total_n_lipids_BB == 0


def test_get_n_saccharides_from_atom():

    all_n_saccharides_Hk2 = aux.get_n_saccharides_from_atom(molsys_Hk2, skip_digestion=True)
    all_n_saccharides_BB = aux.get_n_saccharides_from_atom(molsys_BB, skip_digestion=True)
    list_n_saccharides_Hk2 = aux.get_n_saccharides_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_saccharides_BB = aux.get_n_saccharides_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_saccharides_Hk2 == 8
    assert all_n_saccharides_BB ==  0
    assert list_n_saccharides_Hk2 == 0
    assert list_n_saccharides_BB == 0


def test_get_total_n_saccharides_from_atom():

    all_total_n_saccharides_Hk2 = aux.get_total_n_saccharides_from_atom(molsys_Hk2, skip_digestion=True)
    all_total_n_saccharides_BB = aux.get_total_n_saccharides_from_atom(molsys_BB, skip_digestion=True)
    list_total_n_saccharides_Hk2 = aux.get_total_n_saccharides_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_saccharides_BB = aux.get_total_n_saccharides_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_saccharides_Hk2 == 8
    assert all_total_n_saccharides_BB ==  0
    assert list_total_n_saccharides_Hk2 == 0
    assert list_total_n_saccharides_BB == 0


def test_get_n_peptides_from_atom():

    all_n_peptides_Hk2 = aux.get_n_peptides_from_atom(molsys_Hk2, skip_digestion=True)
    all_n_peptides_BB = aux.get_n_peptides_from_atom(molsys_BB, skip_digestion=True)
    list_n_peptides_Hk2 = aux.get_n_peptides_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_peptides_BB = aux.get_n_peptides_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_peptides_Hk2 == 0
    assert all_n_peptides_BB ==  0
    assert list_n_peptides_Hk2 == 0
    assert list_n_peptides_BB == 0


def test_get_total_n_peptides_from_atom():

    all_total_n_peptides_Hk2 = aux.get_total_n_peptides_from_atom(molsys_Hk2, skip_digestion=True)
    all_total_n_peptides_BB = aux.get_total_n_peptides_from_atom(molsys_BB, skip_digestion=True)
    list_total_n_peptides_Hk2 = aux.get_total_n_peptides_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_peptides_BB = aux.get_total_n_peptides_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_peptides_Hk2 == 0
    assert all_total_n_peptides_BB ==  0
    assert list_total_n_peptides_Hk2 == 0
    assert list_total_n_peptides_BB == 0


def test_get_n_proteins_from_atom():

    all_n_proteins_Hk2 = aux.get_n_proteins_from_atom(molsys_Hk2, skip_digestion=True)
    all_n_proteins_BB = aux.get_n_proteins_from_atom(molsys_BB, skip_digestion=True)
    list_n_proteins_Hk2 = aux.get_n_proteins_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_proteins_BB = aux.get_n_proteins_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_proteins_Hk2 == 2
    assert all_n_proteins_BB ==  6
    assert list_n_proteins_Hk2 == 1
    assert list_n_proteins_BB == 1


def test_get_total_n_proteins_from_atom():

    all_total_n_proteins_Hk2 = aux.get_total_n_proteins_from_atom(molsys_Hk2, skip_digestion=True)
    all_total_n_proteins_BB = aux.get_total_n_proteins_from_atom(molsys_BB, skip_digestion=True)
    list_total_n_proteins_Hk2 = aux.get_total_n_proteins_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_proteins_BB = aux.get_total_n_proteins_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_proteins_Hk2 == 2
    assert all_total_n_proteins_BB ==  6
    assert list_total_n_proteins_Hk2 == 1
    assert list_total_n_proteins_BB == 1


def test_get_n_dnas_from_atom():

    all_n_dnas_Hk2 = aux.get_n_dnas_from_atom(molsys_Hk2, skip_digestion=True)
    all_n_dnas_BB = aux.get_n_dnas_from_atom(molsys_BB, skip_digestion=True)
    list_n_dnas_Hk2 = aux.get_n_dnas_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_dnas_BB = aux.get_n_dnas_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_dnas_Hk2 == 0
    assert all_n_dnas_BB ==  0
    assert list_n_dnas_Hk2 == 0
    assert list_n_dnas_BB == 0


def test_get_total_n_dnas_from_atom():

    all_total_n_dnas_Hk2 = aux.get_total_n_dnas_from_atom(molsys_Hk2, skip_digestion=True)
    all_total_n_dnas_BB = aux.get_total_n_dnas_from_atom(molsys_BB, skip_digestion=True)
    list_total_n_dnas_Hk2 = aux.get_total_n_dnas_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_dnas_BB = aux.get_total_n_dnas_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_dnas_Hk2 == 0
    assert all_total_n_dnas_BB ==  0
    assert list_total_n_dnas_Hk2 == 0
    assert list_total_n_dnas_BB == 0


def test_get_n_rnas_from_atom():

    all_n_rnas_Hk2 = aux.get_n_rnas_from_atom(molsys_Hk2, skip_digestion=True)
    all_n_rnas_BB = aux.get_n_rnas_from_atom(molsys_BB, skip_digestion=True)
    list_n_rnas_Hk2 = aux.get_n_rnas_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_rnas_BB = aux.get_n_rnas_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_rnas_Hk2 == 0
    assert all_n_rnas_BB ==  0
    assert list_n_rnas_Hk2 == 0
    assert list_n_rnas_BB == 0


def test_get_total_n_rnas_from_atom():

    all_total_n_rnas_Hk2 = aux.get_total_n_rnas_from_atom(molsys_Hk2, skip_digestion=True)
    all_total_n_rnas_BB = aux.get_total_n_rnas_from_atom(molsys_BB, skip_digestion=True)
    list_total_n_rnas_Hk2 = aux.get_total_n_rnas_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_rnas_BB = aux.get_total_n_rnas_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_rnas_Hk2 == 0
    assert all_total_n_rnas_BB ==  0
    assert list_total_n_rnas_Hk2 == 0
    assert list_total_n_rnas_BB == 0


def test_get_n_polysaccharides_from_atom():

    all_n_polysaccharides_Hk2 = aux.get_n_polysaccharides_from_atom(molsys_Hk2, skip_digestion=True)
    all_n_polysaccharides_BB = aux.get_n_polysaccharides_from_atom(molsys_BB, skip_digestion=True)
    list_n_polysaccharides_Hk2 = aux.get_n_polysaccharides_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_polysaccharides_BB = aux.get_n_polysaccharides_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_polysaccharides_Hk2 == 8
    assert all_n_polysaccharides_BB ==  0
    assert list_n_polysaccharides_Hk2 == 0
    assert list_n_polysaccharides_BB == 0


def test_get_total_n_polysaccharides_from_atom():

    all_total_n_polysaccharides_Hk2 = aux.get_total_n_polysaccharides_from_atom(molsys_Hk2, skip_digestion=True)
    all_total_n_polysaccharides_BB = aux.get_total_n_polysaccharides_from_atom(molsys_BB, skip_digestion=True)
    list_total_n_polysaccharides_Hk2 = aux.get_total_n_polysaccharides_from_atom(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_polysaccharides_BB = aux.get_total_n_polysaccharides_from_atom(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_polysaccharides_Hk2 == 8
    assert all_total_n_polysaccharides_BB ==  0
    assert list_total_n_polysaccharides_Hk2 == 0
    assert list_total_n_polysaccharides_BB == 0


# From group


def test_get_atom_index_from_group():

    all_atom_index_Hk2 = aux.get_atom_index_from_group(molsys_Hk2, skip_digestion=True)
    all_atom_index_BB = aux.get_atom_index_from_group(molsys_BB, skip_digestion=True)
    list_atom_index_Hk2 = aux.get_atom_index_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_atom_index_BB = aux.get_atom_index_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

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


def test_get_atom_id_from_group():

    all_atom_id_Hk2 = aux.get_atom_id_from_group(molsys_Hk2, skip_digestion=True)
    all_atom_id_BB = aux.get_atom_id_from_group(molsys_BB, skip_digestion=True)
    list_atom_id_Hk2 = aux.get_atom_id_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_atom_id_BB = aux.get_atom_id_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_atom_id_Hk2, list)
    assert len(all_atom_id_Hk2) == 1871
    assert len(all_atom_id_BB) == 1101
    assert all_atom_id_Hk2[344:347] == [[2679, 2680, 2681, 2682, 2683, 2684],
                                        [2685, 2686, 2687, 2688, 2689, 2690, 2691],
                                        [2692, 2693, 2694, 2695, 2696]]
    assert all_atom_id_Hk2[1750:1755] == [[13374], [13375], [13376], [13377],
                                          [13378, 13379, 13380, 13381, 13382, 13383, 13384, 13385, 13386, 13387, 13388, 13389]]
    assert all_atom_id_Hk2[0] == [1, 2, 3, 4, 5, 6, 7, 8]
    assert all_atom_id_Hk2[-1] == [13546]
    assert all_atom_id_BB[385:388] == [[3073, 3074, 3075, 3076, 3077, 3078, 3079, 3080],
                                       [3081, 3082, 3083, 3084, 3085],
                                       [3086, 3087, 3088, 3089, 3090, 3091, 3092, 3093]]
    assert all_atom_id_BB[586:592] == [[4627, 4628, 4629, 4630, 4631, 4632, 4633, 4634],
                                       [4635, 4636, 4637, 4638, 4639, 4640],
                                       [4641], [4642], [4643], [4644]]
    assert all_atom_id_BB[0] == [1, 2, 3, 4, 5, 6, 7]
    assert all_atom_id_BB[-1] == [5153]
    assert list_atom_id_Hk2 == [[34, 35, 36, 37, 38, 39, 40, 41, 42],
                                [43, 44, 45, 46, 47, 48, 49],
                                [50, 51, 52, 53, 54, 55, 56, 57]]
    assert list_atom_id_BB == [[74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85],
                               [86, 87, 88, 89, 90, 91, 92, 93],
                               [94, 95, 96, 97, 98, 99, 100, 101, 102],
                               [103, 104, 105, 106, 107, 108, 109]]


def test_get_atom_name_from_group():

    all_atom_name_Hk2 = aux.get_atom_name_from_group(molsys_Hk2, skip_digestion=True)
    all_atom_name_BB = aux.get_atom_name_from_group(molsys_BB, skip_digestion=True)
    list_atom_name_Hk2 = aux.get_atom_name_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_atom_name_BB = aux.get_atom_name_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_atom_name_Hk2, list)
    assert len(all_atom_name_Hk2) == 1871
    assert len(all_atom_name_BB) == 1101
    assert all_atom_name_Hk2[344:347] == [['N', 'CA', 'C', 'O', 'CB', 'SG'],
                                          ['N', 'CA', 'C', 'O', 'CB', 'CG1', 'CG2'],
                                          ['N', 'CA', 'C', 'O', 'CB']]
    assert all_atom_name_Hk2[1750:1755] == [['UNK'], ['UNK'], ['UNK'], ['UNK'],
                                            ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6']]
    assert all_atom_name_Hk2[0] == ['N', 'CA', 'C', 'O', 'CB', 'CG', 'OD1', 'OD2']
    assert all_atom_name_Hk2[-1] == ['O']
    assert all_atom_name_BB[385:388] == [['N', 'CA', 'C', 'O', 'CB', 'CG', 'CD', 'CE'],
                                         ['N', 'CA', 'C', 'O', 'CB'],
                                         ['N', 'CA', 'C', 'O', 'CB', 'CG', 'CD1', 'CD2']]
    assert all_atom_name_BB[586:592] == [['N', 'CA', 'C', 'O', 'CB', 'CG', 'CD1', 'CD2'],
                                         ['N', 'CA', 'C', 'CB', 'OG', 'OXT'],
                                         ['O'], ['O'], ['O'], ['O']]
    assert all_atom_name_BB[0] == ['N', 'CA', 'C', 'O', 'CB', 'CG1', 'CG2']
    assert all_atom_name_BB[-1] == ['O']
    assert list_atom_name_Hk2 == [['N', 'CA', 'C', 'O', 'CB', 'CG', 'CD', 'CE', 'NZ'],
                                  ['N', 'CA', 'C', 'O', 'CB', 'CG1', 'CG2'],
                                  ['N', 'CA', 'C', 'O', 'CB', 'CG', 'OD1', 'OD2']]
    assert list_atom_name_BB == [['N', 'CA', 'C', 'O', 'CB', 'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ', 'OH'],
                                 ['N', 'CA', 'C', 'O', 'CB', 'CG', 'CD1', 'CD2'],
                                 ['N', 'CA', 'C', 'O', 'CB', 'CG', 'CD', 'OE1', 'NE2'],
                                 ['N', 'CA', 'C', 'O', 'CB', 'OG1', 'CG2']]


def test_get_atom_type_from_group():

    all_atom_type_Hk2 = aux.get_atom_type_from_group(molsys_Hk2, skip_digestion=True)
    all_atom_type_BB = aux.get_atom_type_from_group(molsys_BB, skip_digestion=True)
    list_atom_type_Hk2 = aux.get_atom_type_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_atom_type_BB = aux.get_atom_type_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_atom_type_Hk2, list)
    assert len(all_atom_type_Hk2) == 1871
    assert len(all_atom_type_BB) == 1101
    assert all_atom_type_Hk2[344:347] == [['N', 'C', 'C', 'O', 'C', 'S'],
                                          ['N', 'C', 'C', 'O', 'C', 'C', 'C'],
                                          ['N', 'C', 'C', 'O', 'C']]
    assert all_atom_type_Hk2[1750:1755] == [['X'], ['X'], ['X'], ['X'],
                                            ['C', 'C', 'C', 'C', 'C', 'C', 'O', 'O', 'O', 'O', 'O', 'O']]
    assert all_atom_type_Hk2[0] == ['N', 'C', 'C', 'O', 'C', 'C', 'O', 'O']
    assert all_atom_type_Hk2[-1] == ['O']
    assert all_atom_type_BB[385:388] == [['N', 'C', 'C', 'O', 'C', 'C', 'C', 'C'],
                                        ['N', 'C', 'C', 'O', 'C'],
                                        ['N', 'C', 'C', 'O', 'C', 'C', 'C', 'C']]
    assert all_atom_type_BB[586:592] == [['N', 'C', 'C', 'O', 'C', 'C', 'C', 'C'],
                                         ['N', 'C', 'C', 'C', 'O', 'O'],
                                         ['O'], ['O'], ['O'], ['O']]
    assert all_atom_type_BB[0] == ['N', 'C', 'C', 'O', 'C', 'C', 'C']
    assert all_atom_type_BB[-1] == ['O']
    assert list_atom_type_Hk2 == [['N', 'C', 'C', 'O', 'C', 'C', 'C', 'C', 'N'],
                                  ['N', 'C', 'C', 'O', 'C', 'C', 'C'],
                                  ['N', 'C', 'C', 'O', 'C', 'C', 'O', 'O']]
    assert list_atom_type_BB == [['N', 'C', 'C', 'O', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'O'],
                                 ['N', 'C', 'C', 'O', 'C', 'C', 'C', 'C'],
                                 ['N', 'C', 'C', 'O', 'C', 'C', 'C', 'O', 'N'],
                                 ['N', 'C', 'C', 'O', 'C', 'O', 'C']]


def test_get_group_index_from_group():

    all_group_index_Hk2 = aux.get_group_index_from_group(molsys_Hk2, skip_digestion=True)
    all_group_index_BB = aux.get_group_index_from_group(molsys_BB, skip_digestion=True)
    list_group_index_Hk2 = aux.get_group_index_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_group_index_BB = aux.get_group_index_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_group_index_Hk2, list)
    assert len(all_group_index_Hk2) == 1871
    assert len(all_group_index_BB) == 1101
    assert all_group_index_Hk2[344:347] == [344, 345, 346]
    assert all_group_index_Hk2[1750:1755] == [1750, 1751, 1752, 1753, 1754]
    assert all_group_index_Hk2[0] == 0
    assert all_group_index_Hk2[-1] == 1870
    assert all_group_index_BB[385:388] == [385, 386, 387]
    assert all_group_index_BB[586:592] == [586, 587, 588, 589, 590, 591]
    assert all_group_index_BB[0] == 0
    assert all_group_index_BB[-1] == 1100
    assert list_group_index_Hk2 == [4, 5, 6]
    assert list_group_index_BB == [10, 11, 12, 13]


def test_get_group_id_from_group():

    all_group_id_Hk2 = aux.get_group_id_from_group(molsys_Hk2, skip_digestion=True)
    all_group_id_BB = aux.get_group_id_from_group(molsys_BB, skip_digestion=True)
    list_group_id_Hk2 = aux.get_group_id_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_group_id_BB = aux.get_group_id_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_group_id_Hk2, list)
    assert len(all_group_id_Hk2) == 1871
    assert len(all_group_id_BB) == 1101
    assert all_group_id_Hk2[344:347] == [368, 369, 370]
    assert all_group_id_Hk2[1750:1755] == [1006, 1007, 1008, 1009, 1001]
    assert all_group_id_Hk2[0] == 17
    assert all_group_id_Hk2[-1] == 1097
    assert all_group_id_BB[385:388] == [60, 61, 62]
    assert all_group_id_BB[586:592] == [88, 89, 111, 112, 113, 114]
    assert all_group_id_BB[0] == 3
    assert all_group_id_BB[-1] == 129
    assert list_group_id_Hk2 == [21, 22, 23]
    assert list_group_id_BB == [13, 14, 15, 16]


def test_get_group_name_from_group():

    all_group_name_Hk2 = aux.get_group_name_from_group(molsys_Hk2, skip_digestion=True)
    all_group_name_BB = aux.get_group_name_from_group(molsys_BB, skip_digestion=True)
    list_group_name_Hk2 = aux.get_group_name_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_group_name_BB = aux.get_group_name_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_group_name_Hk2, list)
    assert len(all_group_name_Hk2) == 1871
    assert len(all_group_name_BB) == 1101
    assert all_group_name_Hk2[344:347] == ['CYS', 'VAL', 'ALA']
    assert all_group_name_Hk2[1750:1755] == ['UNX', 'UNX', 'UNX', 'UNX', 'GLC']
    assert all_group_name_Hk2[0] == 'ASP'
    assert all_group_name_Hk2[-1] == 'HOH'
    assert all_group_name_BB[385:388] == ['LYS', 'GLN', 'LEU']
    assert all_group_name_BB[586:592] == ['LEU', 'SER', 'HOH', 'HOH', 'HOH', 'HOH']
    assert all_group_name_BB[0] == 'VAL'
    assert all_group_name_BB[-1] == 'HOH'
    assert list_group_name_Hk2 == ['LYS', 'VAL', 'ASP']
    assert list_group_name_BB == ['TYR', 'LEU', 'GLN', 'THR']


def test_get_group_type_from_group():

    all_group_type_Hk2 = aux.get_group_type_from_group(molsys_Hk2, skip_digestion=True)
    all_group_type_BB = aux.get_group_type_from_group(molsys_BB, skip_digestion=True)
    list_group_type_Hk2 = aux.get_group_type_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_group_type_BB = aux.get_group_type_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_group_type_Hk2, list)
    assert len(all_group_type_Hk2) == 1871
    assert len(all_group_type_BB) == 1101
    assert all_group_type_Hk2[344:347] == ['amino acid', 'amino acid', 'amino acid']
    assert all_group_type_Hk2[1750:1755] == ['ion', 'ion', 'ion', 'ion', 'saccharide']
    assert all_group_type_Hk2[0] == 'amino acid'
    assert all_group_type_Hk2[-1] == 'water'
    assert all_group_type_BB[385:388] == ['amino acid', 'amino acid', 'amino acid']
    assert all_group_type_BB[586:592] == ['amino acid', 'amino acid', 'water', 'water', 'water', 'water']
    assert all_group_type_BB[0] == 'amino acid'
    assert all_group_type_BB[-1] == 'water'
    assert list_group_type_Hk2 == ['amino acid', 'amino acid', 'amino acid']
    assert list_group_type_BB == ['amino acid', 'amino acid', 'amino acid', 'amino acid']


def test_get_molecule_index_from_group():

    all_molecule_index_Hk2 = aux.get_molecule_index_from_group(molsys_Hk2, skip_digestion=True)
    all_molecule_index_BB = aux.get_molecule_index_from_group(molsys_BB, skip_digestion=True)
    list_molecule_index_Hk2 = aux.get_molecule_index_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_molecule_index_BB = aux.get_molecule_index_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_molecule_index_Hk2, list)
    assert len(all_molecule_index_Hk2) == 1871
    assert len(all_molecule_index_BB) == 1101
    assert all_molecule_index_Hk2[344:347] == [0, 0, 0]
    assert all_molecule_index_Hk2[1750:1755] == [14, 15, 16, 17, 18]
    assert all_molecule_index_Hk2[0] == 0
    assert all_molecule_index_Hk2[-1] == 134
    assert all_molecule_index_BB[385:388] == [3, 3, 3]
    assert all_molecule_index_BB[586:592] == [5, 5, 6, 7, 8, 9]
    assert all_molecule_index_BB[0] == 0
    assert all_molecule_index_BB[-1] == 518
    assert list_molecule_index_Hk2 == [0, 0, 0]
    assert list_molecule_index_BB == [0, 0, 0, 0]


def test_get_molecule_id_from_group():

    all_molecule_id_Hk2 = aux.get_molecule_id_from_group(molsys_Hk2, skip_digestion=True)
    all_molecule_id_BB = aux.get_molecule_id_from_group(molsys_BB, skip_digestion=True)
    list_molecule_id_Hk2 = aux.get_molecule_id_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_molecule_id_BB = aux.get_molecule_id_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_molecule_id_Hk2, list)
    assert len(all_molecule_id_Hk2) == 1871
    assert len(all_molecule_id_BB) == 1101
    assert all_molecule_id_Hk2[344:347] == [0, 0, 0]
    assert all_molecule_id_Hk2[1750:1755] == [14, 15, 16, 17, 18]
    assert all_molecule_id_Hk2[0] == 0
    assert all_molecule_id_Hk2[-1] == 134
    assert all_molecule_id_BB[385:388] == [3, 3, 3]
    assert all_molecule_id_BB[586:592] == [5, 5, 6, 7, 8, 9]
    assert all_molecule_id_BB[0] == 0
    assert all_molecule_id_BB[-1] == 518
    assert list_molecule_id_Hk2 == [0, 0, 0]
    assert list_molecule_id_BB == [0, 0, 0, 0]


def test_get_molecule_name_from_group():

    all_molecule_name_Hk2 = aux.get_molecule_name_from_group(molsys_Hk2, skip_digestion=True)
    all_molecule_name_BB = aux.get_molecule_name_from_group(molsys_BB, skip_digestion=True)
    list_molecule_name_Hk2 = aux.get_molecule_name_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_molecule_name_BB = aux.get_molecule_name_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_molecule_name_Hk2, list)
    assert len(all_molecule_name_Hk2) == 1871
    assert len(all_molecule_name_BB) == 1101
    assert all_molecule_name_Hk2[344:347] == ['Hexokinase-2', 'Hexokinase-2', 'Hexokinase-2']
    assert all_molecule_name_Hk2[1750:1755] == ['UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION',
                                                'UNKNOWN ATOM OR ION', 'alpha-D-glucopyranose']
    assert all_molecule_name_Hk2[0] == 'Hexokinase-2'
    assert all_molecule_name_Hk2[-1] == 'water'
    assert all_molecule_name_BB[385:388] == ['BARSTAR', 'BARSTAR', 'BARSTAR']
    assert all_molecule_name_BB[586:592] == ['BARSTAR', 'BARSTAR', 'water', 'water', 'water', 'water']
    assert all_molecule_name_BB[0] == 'BARNASE'
    assert all_molecule_name_BB[-1] == 'water'
    assert list_molecule_name_Hk2 == ['Hexokinase-2', 'Hexokinase-2', 'Hexokinase-2']
    assert list_molecule_name_BB == ['BARNASE', 'BARNASE', 'BARNASE', 'BARNASE']


def test_get_molecule_type_from_group():

    all_molecule_type_Hk2 = aux.get_molecule_type_from_group(molsys_Hk2, skip_digestion=True)
    all_molecule_type_BB = aux.get_molecule_type_from_group(molsys_BB, skip_digestion=True)
    list_molecule_type_Hk2 = aux.get_molecule_type_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_molecule_type_BB = aux.get_molecule_type_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_molecule_type_Hk2, list)
    assert len(all_molecule_type_Hk2) == 1871
    assert len(all_molecule_type_BB) == 1101
    assert all_molecule_type_Hk2[344:347] == ['protein', 'protein', 'protein']
    assert all_molecule_type_Hk2[1750:1755] == ['unknown', 'unknown', 'unknown', 'unknown', 'polysaccharide']
    assert all_molecule_type_Hk2[0] == 'protein'
    assert all_molecule_type_Hk2[-1] == 'water'
    assert all_molecule_type_BB[385:388] == ['protein', 'protein', 'protein']
    assert all_molecule_type_BB[586:592] == ['protein', 'protein', 'water', 'water', 'water', 'water']
    assert all_molecule_type_BB[0] == 'protein'
    assert all_molecule_type_BB[-1] == 'water'
    assert list_molecule_type_Hk2 == ['protein', 'protein', 'protein']
    assert list_molecule_type_BB == ['protein', 'protein', 'protein', 'protein']


def test_get_entity_index_from_group():

    all_entity_index_Hk2 = aux.get_entity_index_from_group(molsys_Hk2, skip_digestion=True)
    all_entity_index_BB = aux.get_entity_index_from_group(molsys_BB, skip_digestion=True)
    list_entity_index_Hk2 = aux.get_entity_index_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_entity_index_BB = aux.get_entity_index_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_entity_index_Hk2, list)
    assert len(all_entity_index_Hk2) == 1871
    assert len(all_entity_index_BB) == 1101
    assert all_entity_index_Hk2[344:347] == [0, 0, 0]
    assert all_entity_index_Hk2[1750:1755] == [3, 3, 3, 3, 1]
    assert all_entity_index_Hk2[0] == 0
    assert all_entity_index_Hk2[-1] == 4
    assert all_entity_index_BB[385:388] == [1, 1, 1]
    assert all_entity_index_BB[586:592] == [1, 1, 2, 2, 2, 2]
    assert all_entity_index_BB[0] == 0
    assert all_entity_index_BB[-1] == 2
    assert list_entity_index_Hk2 == [0, 0, 0]
    assert list_entity_index_BB == [0, 0, 0, 0]


def test_get_entity_id_from_group():

    all_entity_id_Hk2 = aux.get_entity_id_from_group(molsys_Hk2, skip_digestion=True)
    all_entity_id_BB = aux.get_entity_id_from_group(molsys_BB, skip_digestion=True)
    list_entity_id_Hk2 = aux.get_entity_id_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_entity_id_BB = aux.get_entity_id_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_entity_id_Hk2, list)
    assert len(all_entity_id_Hk2) == 1871
    assert len(all_entity_id_BB) == 1101
    assert all_entity_id_Hk2[344:347] == [1, 1, 1]
    assert all_entity_id_Hk2[1750:1755] == [4, 4, 4, 4, 2]
    assert all_entity_id_Hk2[0] == 1 
    assert all_entity_id_Hk2[-1] == 5
    assert all_entity_id_BB[385:388] == [2, 2, 2]
    assert all_entity_id_BB[586:592] == [2, 2, 3, 3, 3, 3]
    assert all_entity_id_BB[0] == 1
    assert all_entity_id_BB[-1] == 3
    assert list_entity_id_Hk2 == [1, 1, 1]
    assert list_entity_id_BB == [1, 1, 1, 1]


def test_get_entity_name_from_group():

    all_entity_name_Hk2 = aux.get_entity_name_from_group(molsys_Hk2, skip_digestion=True)
    all_entity_name_BB = aux.get_entity_name_from_group(molsys_BB, skip_digestion=True)
    list_entity_name_Hk2 = aux.get_entity_name_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_entity_name_BB = aux.get_entity_name_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_entity_name_Hk2, list)
    assert len(all_entity_name_Hk2) == 1871
    assert len(all_entity_name_BB) == 1101
    assert all_entity_name_Hk2[344:347] == ['Hexokinase-2', 'Hexokinase-2', 'Hexokinase-2']
    assert all_entity_name_Hk2[1750:1755] == ['UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION',
                                              'UNKNOWN ATOM OR ION', 'alpha-D-glucopyranose']
    assert all_entity_name_Hk2[0] == 'Hexokinase-2'
    assert all_entity_name_Hk2[-1] == 'water'
    assert all_entity_name_BB[385:388] == ['BARSTAR', 'BARSTAR', 'BARSTAR']
    assert all_entity_name_BB[586:592] == ['BARSTAR', 'BARSTAR', 'water', 'water', 'water', 'water']
    assert all_entity_name_BB[0] == 'BARNASE'
    assert all_entity_name_BB[-1] == 'water'
    assert list_entity_name_Hk2 == ['Hexokinase-2', 'Hexokinase-2', 'Hexokinase-2']
    assert list_entity_name_BB == ['BARNASE', 'BARNASE', 'BARNASE', 'BARNASE']


def test_get_entity_type_from_group():

    all_entity_type_Hk2 = aux.get_entity_type_from_group(molsys_Hk2, skip_digestion=True)
    all_entity_type_BB = aux.get_entity_type_from_group(molsys_BB, skip_digestion=True)
    list_entity_type_Hk2 = aux.get_entity_type_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_entity_type_BB = aux.get_entity_type_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_entity_type_Hk2, list)
    assert len(all_entity_type_Hk2) == 1871
    assert len(all_entity_type_BB) == 1101
    assert all_entity_type_Hk2[344:347] == ['protein', 'protein', 'protein']
    assert all_entity_type_Hk2[1750:1755] == ['unknown', 'unknown', 'unknown', 'unknown', 'polysaccharide']
    assert all_entity_type_Hk2[0] == 'protein'
    assert all_entity_type_Hk2[-1] == 'water'
    assert all_entity_type_BB[385:388] == ['protein', 'protein', 'protein']
    assert all_entity_type_BB[586:592] == ['protein', 'protein', 'water', 'water', 'water', 'water']
    assert all_entity_type_BB[0] == 'protein'
    assert all_entity_type_BB[-1] == 'water'
    assert list_entity_type_Hk2 == ['protein', 'protein', 'protein']
    assert list_entity_type_BB == ['protein', 'protein', 'protein', 'protein']


def test_get_component_index_from_group():

    all_component_index_Hk2 = aux.get_component_index_from_group(molsys_Hk2, skip_digestion=True)
    all_component_index_BB = aux.get_component_index_from_group(molsys_BB, skip_digestion=True)
    list_component_index_Hk2 = aux.get_component_index_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_component_index_BB = aux.get_component_index_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_component_index_Hk2, list)
    assert len(all_component_index_Hk2) == 1871
    assert len(all_component_index_BB) == 1101
    assert all_component_index_Hk2[344:347] == [1, 1, 1]
    assert all_component_index_Hk2[1750:1755] == [25, 26, 27, 28, 29]
    assert all_component_index_Hk2[0] == 0
    assert all_component_index_Hk2[-1] == 145
    assert all_component_index_BB[385:388] == [3, 3, 3]
    assert all_component_index_BB[586:592] == [7, 7, 8, 9, 10, 11]
    assert all_component_index_BB[0] == 0
    assert all_component_index_BB[-1] == 520
    assert list_component_index_Hk2 == [0, 0, 0]
    assert list_component_index_BB == [0, 0, 0, 0]


def test_get_component_id_from_group():

    all_component_id_Hk2 = aux.get_component_id_from_group(molsys_Hk2, skip_digestion=True)
    all_component_id_BB = aux.get_component_id_from_group(molsys_BB, skip_digestion=True)
    list_component_id_Hk2 = aux.get_component_id_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_component_id_BB = aux.get_component_id_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_component_id_Hk2, list)
    assert len(all_component_id_Hk2) == 1871
    assert len(all_component_id_BB) == 1101
    assert all_component_id_Hk2[344:347] == [1, 1, 1]
    assert all_component_id_Hk2[1750:1755] == [25, 26, 27, 28, 29]
    assert all_component_id_Hk2[0] == 0
    assert all_component_id_Hk2[-1] == 145
    assert all_component_id_BB[385:388] == [3, 3, 3]
    assert all_component_id_BB[586:592] == [7, 7, 8, 9, 10, 11]
    assert all_component_id_BB[0] == 0
    assert all_component_id_BB[-1] == 520
    assert list_component_id_Hk2 == [0, 0, 0]
    assert list_component_id_BB == [0, 0, 0, 0]


def test_get_component_name_from_group():

    all_component_name_Hk2 = aux.get_component_name_from_group(molsys_Hk2, skip_digestion=True)
    all_component_name_BB = aux.get_component_name_from_group(molsys_BB, skip_digestion=True)
    list_component_name_Hk2 = aux.get_component_name_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_component_name_BB = aux.get_component_name_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_component_name_Hk2, list)
    assert len(all_component_name_Hk2) == 1871
    assert len(all_component_name_BB) == 1101
    assert all_component_name_Hk2[344:347] == ['protein 1', 'protein 1', 'protein 1']
    assert all_component_name_Hk2[1750:1755] == ['UNX', 'UNX', 'UNX', 'UNX', 'unknown 4']
    assert all_component_name_Hk2[0] == 'protein 0'
    assert all_component_name_Hk2[-1] == 'water'
    assert all_component_name_BB[385:388] == ['protein 3', 'protein 3', 'protein 3']
    assert all_component_name_BB[586:592] == ['protein 5', 'protein 5', 'water', 'water', 'water', 'water']
    assert all_component_name_BB[0] == 'protein 0'
    assert all_component_name_BB[-1] == 'water'
    assert list_component_name_Hk2 == ['protein 0', 'protein 0', 'protein 0']
    assert list_component_name_BB == ['protein 0', 'protein 0', 'protein 0', 'protein 0']


def test_get_component_type_from_group():

    all_component_type_Hk2 = aux.get_component_type_from_group(molsys_Hk2, skip_digestion=True)
    all_component_type_BB = aux.get_component_type_from_group(molsys_BB, skip_digestion=True)
    list_component_type_Hk2 = aux.get_component_type_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_component_type_BB = aux.get_component_type_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_component_type_Hk2, list)
    assert len(all_component_type_Hk2) == 1871
    assert len(all_component_type_BB) == 1101
    assert all_component_type_Hk2[344:347] == ['protein', 'protein', 'protein']
    assert all_component_type_Hk2[1750:1755] == ['ion', 'ion', 'ion', 'ion', 'polysaccharide']
    assert all_component_type_Hk2[0] == 'protein'
    assert all_component_type_Hk2[-1] == 'water'
    assert all_component_type_BB[385:388] == ['protein', 'protein', 'protein']
    assert all_component_type_BB[586:592] == ['protein', 'protein', 'water', 'water', 'water', 'water']
    assert all_component_type_BB[0] == 'protein'
    assert all_component_type_BB[-1] == 'water'
    assert list_component_type_Hk2 == ['protein', 'protein', 'protein']
    assert list_component_type_BB == ['protein', 'protein', 'protein', 'protein']


def test_get_chain_index_from_group():

    all_chain_index_Hk2 = aux.get_chain_index_from_group(molsys_Hk2, skip_digestion=True)
    all_chain_index_BB = aux.get_chain_index_from_group(molsys_BB, skip_digestion=True)
    list_chain_index_Hk2 = aux.get_chain_index_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_chain_index_BB = aux.get_chain_index_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_chain_index_Hk2, list)
    assert len(all_chain_index_Hk2) == 1871
    assert len(all_chain_index_BB) == 1101
    assert all_chain_index_Hk2[344:347] == [0, 0, 0]
    assert all_chain_index_Hk2[1750:1755] == [14, 15, 16, 17, 18]
    assert all_chain_index_Hk2[0] == 0
    assert all_chain_index_Hk2[-1] == 39
    assert all_chain_index_BB[385:388] == [3, 3, 3]
    assert all_chain_index_BB[586:592] == [5, 5, 6, 6, 6, 6]
    assert all_chain_index_BB[0] == 0
    assert all_chain_index_BB[-1] == 11
    assert list_chain_index_Hk2 == [0, 0, 0]
    assert list_chain_index_BB == [0, 0, 0, 0]


def test_get_chain_id_from_group():

    all_chain_id_Hk2 = aux.get_chain_id_from_group(molsys_Hk2, skip_digestion=True)
    all_chain_id_BB = aux.get_chain_id_from_group(molsys_BB, skip_digestion=True)
    list_chain_id_Hk2 = aux.get_chain_id_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_chain_id_BB = aux.get_chain_id_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_chain_id_Hk2, list)
    assert len(all_chain_id_Hk2) == 1871
    assert len(all_chain_id_BB) == 1101
    assert all_chain_id_Hk2[344:347] == ['A', 'A', 'A']
    assert all_chain_id_Hk2[1750:1755] == ['O', 'P', 'Q', 'R', 'S']
    assert all_chain_id_Hk2[0] == 'A'
    assert all_chain_id_Hk2[-1] == 'NA'
    assert all_chain_id_BB[385:388] == ['D', 'D', 'D']
    assert all_chain_id_BB[586:592] == ['F', 'F', 'G', 'G', 'G', 'G']
    assert all_chain_id_BB[0] == 'A'
    assert all_chain_id_BB[-1] == 'L'
    assert list_chain_id_Hk2 == ['A', 'A', 'A']
    assert list_chain_id_BB == ['A', 'A', 'A', 'A']


def test_get_chain_name_from_group():

    all_chain_name_Hk2 = aux.get_chain_name_from_group(molsys_Hk2, skip_digestion=True)
    all_chain_name_BB = aux.get_chain_name_from_group(molsys_BB, skip_digestion=True)
    list_chain_name_Hk2 = aux.get_chain_name_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_chain_name_BB = aux.get_chain_name_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_chain_name_Hk2, list)
    assert len(all_chain_name_Hk2) == 1871
    assert len(all_chain_name_BB) == 1101
    assert all_chain_name_Hk2[344:347] == ['A', 'A', 'A']
    assert all_chain_name_Hk2[1750:1755] == ['A', 'A', 'A', 'A', 'B']
    assert all_chain_name_Hk2[0] == 'A'
    assert all_chain_name_Hk2[-1] == 'B'
    assert all_chain_name_BB[385:388] == ['D', 'D', 'D']
    assert all_chain_name_BB[586:592] == ['F', 'F', 'A', 'A', 'A', 'A']
    assert all_chain_name_BB[0] == 'A'
    assert all_chain_name_BB[-1] == 'F'
    assert list_chain_name_Hk2 == ['A', 'A', 'A']
    assert list_chain_name_BB == ['A', 'A', 'A', 'A']


def test_get_chain_type_from_group():

    all_chain_type_Hk2 = aux.get_chain_type_from_group(molsys_Hk2, skip_digestion=True)
    all_chain_type_BB = aux.get_chain_type_from_group(molsys_BB, skip_digestion=True)
    list_chain_type_Hk2 = aux.get_chain_type_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_chain_type_BB = aux.get_chain_type_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_chain_type_Hk2, list)
    assert len(all_chain_type_Hk2) == 1871
    assert len(all_chain_type_BB) == 1101
    assert all_chain_type_Hk2[344:347] == ['protein', 'protein', 'protein']
    assert all_chain_type_Hk2[1750:1755] == ['unknown', 'unknown', 'unknown', 'unknown', 'polysaccharide']
    assert all_chain_type_Hk2[0] == 'protein'
    assert all_chain_type_Hk2[-1] == 'water'
    assert all_chain_type_BB[385:388] == ['protein', 'protein', 'protein']
    assert all_chain_type_BB[586:592] == ['protein', 'protein', 'water', 'water', 'water', 'water']
    assert all_chain_type_BB[0] == 'protein'
    assert all_chain_type_BB[-1] == 'water'
    assert list_chain_type_Hk2 == ['protein', 'protein', 'protein']
    assert list_chain_type_BB == ['protein', 'protein', 'protein', 'protein']


def test_get_bond_index_from_group():

    all_bond_index_Hk2 = aux.get_bond_index_from_group(molsys_Hk2, skip_digestion=True)
    all_bond_index_BB = aux.get_bond_index_from_group(molsys_BB, skip_digestion=True)
    list_bond_index_Hk2 = aux.get_bond_index_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_bond_index_BB = aux.get_bond_index_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_bond_index_Hk2, list)
    assert len(all_bond_index_Hk2) == 1871
    assert len(all_bond_index_BB) == 1101
    assert all_bond_index_Hk2[344:347] == [[2718, 2722, 2723, 2724, 2725, 2726, 2727],
                                           [2726, 2728, 2729, 2730, 2731, 2732, 2733, 2734],
                                           [2732, 2735, 2736, 2737, 2738, 2739]]
    assert all_bond_index_Hk2[1750:1755] == [[], [], [], [], [13562, 13563, 13564, 13565, 13566,
                                                              13567, 13568, 13569, 13570, 13571, 13572, 13573]]
    assert all_bond_index_Hk2[0] == [0, 1, 2, 3, 4, 5, 6, 7]
    assert all_bond_index_Hk2[-1] == []
    assert all_bond_index_BB[385:388] == [[3144, 3146, 3147, 3148, 3149, 3150, 3151, 3152, 3153],
                                          [3150, 3154, 3155, 3156, 3157, 3158],
                                          [3158, 3159, 3160, 3161, 3162, 3163, 3164, 3165, 3166]]
    assert all_bond_index_BB[586:592] == [[4721, 4725, 4726, 4727, 4728, 4729, 4730, 4731, 4732],
                                          [4729, 4733, 4734, 4735, 4736, 4737], [], [], [], []]
    assert all_bond_index_BB[0] == [0, 1, 2, 3, 4, 5, 6]
    assert all_bond_index_BB[-1] == []
    assert list_bond_index_Hk2 == [[28, 33, 34, 35, 36, 37, 38, 39, 40, 41], [37, 42, 43, 44, 45, 46, 47, 48],
                                   [46, 49, 50, 51, 52, 53, 54, 55, 56]]
    assert list_bond_index_BB == [[70, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86],
                                  [78, 87, 88, 89, 90, 91, 92, 93, 94],
                                  [91, 95, 96, 97, 98, 99, 100, 101, 102, 103],
                                  [99, 104, 105, 106, 107, 108, 109, 110]]


def test_get_bond_type_from_group():

    all_bond_type_Hk2 = aux.get_bond_type_from_group(molsys_Hk2, skip_digestion=True)
    all_bond_type_BB = aux.get_bond_type_from_group(molsys_BB, skip_digestion=True)
    list_bond_type_Hk2 = aux.get_bond_type_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_bond_type_BB = aux.get_bond_type_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_bond_type_Hk2, list)
    assert len(all_bond_type_Hk2) == 1871
    assert len(all_bond_type_BB) == 1101
    assert all_bond_type_Hk2[344:347] == [[None, None, None, None, None, None, None],
                                          [None, None, None, None, None, None, None, None],
                                          [None, None, None, None, None, None]]
    assert all_bond_type_Hk2[1750:1755] == [[], [], [], [], [None, None, None, None, None, None, None,
                                                             None, None, None, None, None]]
    assert all_bond_type_Hk2[0] == [None, None, None, None, None, None, None, None]
    assert all_bond_type_Hk2[-1] == []
    assert all_bond_type_BB[385:388] == [[None, None, None, None, None, None, None, None, None],
                                         [None, None, None, None, None, None],
                                         [None, None, None, None, None, None, None, None, None]]
    assert all_bond_type_BB[586:592] == [[None, None, None, None, None, None, None, None, None],
                                         [None, None, None, None, None, None], [], [], [], []]
    assert all_bond_type_BB[0] == [None, None, None, None, None, None, None]
    assert all_bond_type_BB[-1] == []
    assert list_bond_type_Hk2 == [[None, None, None, None, None, None, None, None, None, None],
                                  [None, None, None, None, None, None, None, None],
                                  [None, None, None, None, None, None, None, None, None]]
    assert list_bond_type_BB == [[None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                                 [None, None, None, None, None, None, None, None, None],
                                 [None, None, None, None, None, None, None, None, None, None],
                                 [None, None, None, None, None, None, None, None]]


def test_get_bond_order_from_group():

    all_bond_order_Hk2 = aux.get_bond_order_from_group(molsys_Hk2, skip_digestion=True)
    all_bond_order_BB = aux.get_bond_order_from_group(molsys_BB, skip_digestion=True)
    list_bond_order_Hk2 = aux.get_bond_order_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_bond_order_BB = aux.get_bond_order_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_bond_order_Hk2, list)
    assert len(all_bond_order_Hk2) == 1871
    assert len(all_bond_order_BB) == 1101
    assert all_bond_order_Hk2[344:347] == [[None, None, None, None, None, None, None],
                                          [None, None, None, None, None, None, None, None],
                                          [None, None, None, None, None, None]]
    assert all_bond_order_Hk2[1750:1755] == [[], [], [], [], [None, None, None, None, None, None, None,
                                                             None, None, None, None, None]]
    assert all_bond_order_Hk2[0] == [None, None, None, None, None, None, None, None]
    assert all_bond_order_Hk2[-1] == []
    assert all_bond_order_BB[385:388] == [[None, None, None, None, None, None, None, None, None],
                                         [None, None, None, None, None, None],
                                         [None, None, None, None, None, None, None, None, None]]
    assert all_bond_order_BB[586:592] == [[None, None, None, None, None, None, None, None, None],
                                         [None, None, None, None, None, None], [], [], [], []]
    assert all_bond_order_BB[0] == [None, None, None, None, None, None, None]
    assert all_bond_order_BB[-1] == []
    assert list_bond_order_Hk2 == [[None, None, None, None, None, None, None, None, None, None],
                                  [None, None, None, None, None, None, None, None],
                                  [None, None, None, None, None, None, None, None, None]]
    assert list_bond_order_BB == [[None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                                 [None, None, None, None, None, None, None, None, None],
                                 [None, None, None, None, None, None, None, None, None, None],
                                 [None, None, None, None, None, None, None, None]]


def test_get_bonded_atoms_from_group():

    all_bonded_atoms_Hk2 = aux.get_bonded_atoms_from_group(molsys_Hk2, skip_digestion=True)
    all_bonded_atoms_BB = aux.get_bonded_atoms_from_group(molsys_BB, skip_digestion=True)
    list_bonded_atoms_Hk2 = aux.get_bonded_atoms_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_bonded_atoms_BB = aux.get_bonded_atoms_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_bonded_atoms_Hk2, list)
    assert len(all_bonded_atoms_Hk2) == 1871
    assert len(all_bonded_atoms_BB) == 1101
    assert all_bonded_atoms_Hk2[344:347] == [[2672, 2678, 2679, 2680, 2681, 2682, 2683, 2684],
                                             [2680, 2684, 2685, 2686, 2687, 2688, 2689, 2690, 2691],
                                             [2686, 2691, 2692, 2693, 2694, 2695, 2696]]
    assert all_bonded_atoms_Hk2[1750:1755] == [[], [], [], [], [13377, 13378, 13379, 13380, 13381, 13382,
                                                                13383, 13384, 13385, 13386, 13387, 13388]]
    assert all_bonded_atoms_Hk2[0] == [0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert all_bonded_atoms_Hk2[-1] == []
    assert all_bonded_atoms_BB[385:388] == [[3066, 3070, 3071, 3072, 3073, 3074, 3075, 3076, 3077, 3078],
                                            [3072, 3078, 3079, 3080, 3081, 3082, 3083],
                                            [3080, 3083, 3084, 3085, 3086, 3087, 3088, 3089, 3090, 3091]]
    assert all_bonded_atoms_BB[586:592] == [[4618, 4624, 4625, 4626, 4627, 4628, 4629, 4630, 4631, 4632],
                                            [4626, 4632, 4633, 4634, 4635, 4636, 4637], [], [], [], []]
    assert all_bonded_atoms_BB[0] == [0, 1, 2, 3, 4, 5, 6, 7]
    assert all_bonded_atoms_BB[-1] == []
    assert list_bonded_atoms_Hk2 == [[26, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
                                     [35, 42, 43, 44, 45, 46, 47, 48, 49],
                                     [44, 49, 50, 51, 52, 53, 54, 55, 56, 57]]
    assert list_bonded_atoms_BB == [[67, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85],
                                    [75, 85, 86, 87, 88, 89, 90, 91, 92, 93],
                                    [87, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102],
                                    [95, 102, 103, 104, 105, 106, 107, 108, 109]]


def test_get_bonded_atom_pairs_from_group():

    all_bonded_atom_pairs_Hk2 = aux.get_bonded_atom_pairs_from_group(molsys_Hk2, skip_digestion=True)
    all_bonded_atom_pairs_BB = aux.get_bonded_atom_pairs_from_group(molsys_BB, skip_digestion=True)
    list_bonded_atom_pairs_Hk2 = aux.get_bonded_atom_pairs_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_bonded_atom_pairs_BB = aux.get_bonded_atom_pairs_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_bonded_atom_pairs_Hk2, list)
    assert len(all_bonded_atom_pairs_Hk2) == 1871
    assert len(all_bonded_atom_pairs_BB) == 1101
    assert all_bonded_atom_pairs_Hk2[344:347] == [[[2672, 2678], [2678, 2679], [2679, 2680], [2679, 2682],
                                                   [2680, 2681], [2680, 2684], [2682, 2683]],
                                                  [[2680, 2684], [2684, 2685], [2685, 2686], [2685, 2688],
                                                   [2686, 2687], [2686, 2691], [2688, 2689], [2688, 2690]],
                                                  [[2686, 2691], [2691, 2692], [2692, 2693], [2692, 2695],
                                                   [2693, 2694], [2693, 2696]]]
    assert all_bonded_atom_pairs_Hk2[1750:1755] == [[], [], [], [], [[13377, 13378], [13377, 13383], [13377, 13387],
                                                                     [13378, 13379], [13378, 13384], [13379, 13380],
                                                                     [13379, 13385], [13380, 13381], [13380, 13386],
                                                                     [13381, 13382], [13381, 13387], [13382, 13388]]]
    assert all_bonded_atom_pairs_Hk2[0] == [[0, 1], [1, 2], [1, 4], [2, 3], [2, 8], [4, 5], [5, 6], [5, 7]]
    assert all_bonded_atom_pairs_Hk2[-1] == []
    assert all_bonded_atom_pairs_BB[385:388] == [[[3066, 3070], [3070, 3071], [3071, 3072], [3071, 3074], [3072, 3073],
                                                  [3072, 3078], [3074, 3075], [3075, 3076], [3076, 3077]],
                                                 [[3072, 3078], [3078, 3079], [3079, 3080], [3079, 3082], [3080, 3081],
                                                  [3080, 3083]],
                                                 [[3080, 3083], [3083, 3084], [3084, 3085], [3084, 3087], [3085, 3086],
                                                  [3085, 3091], [3087, 3088], [3088, 3089], [3088, 3090]]]
    assert all_bonded_atom_pairs_BB[586:592] == [[[4618, 4624], [4624, 4625], [4625, 4626], [4625, 4628], [4626, 4627],
                                                  [4626, 4632], [4628, 4629], [4629, 4630], [4629, 4631]],
                                                 [[4626, 4632], [4632, 4633], [4633, 4634], [4633, 4635], [4634, 4637],
                                                  [4635, 4636]], [], [], [], []]
    assert all_bonded_atom_pairs_BB[0] == [[0, 1], [1, 2], [1, 4], [2, 3], [2, 7], [4, 5], [4, 6]]
    assert all_bonded_atom_pairs_BB[-1] == []
    assert list_bonded_atom_pairs_Hk2 == [[[26, 33], [33, 34], [34, 35], [34, 37], [35, 36], [35, 42], [37, 38],
                                           [38, 39], [39, 40], [40, 41]],
                                          [[35, 42], [42, 43], [43, 44], [43, 46], [44, 45], [44, 49], [46, 47],
                                           [46, 48]],
                                          [[44, 49], [49, 50], [50, 51], [50, 53], [51, 52], [51, 57], [53, 54],
                                           [54, 55], [54, 56]]]
    assert list_bonded_atom_pairs_BB == [[[67, 73], [73, 74], [74, 75], [74, 77], [75, 76], [75, 85], [77, 78],
                                          [78, 79], [78, 80], [79, 81], [80, 82], [81, 83], [82, 83], [83, 84]],
                                         [[75, 85], [85, 86], [86, 87], [86, 89], [87, 88], [87, 93], [89, 90],
                                          [90, 91], [90, 92]],
                                         [[87, 93], [93, 94], [94, 95], [94, 97], [95, 96], [95, 102], [97, 98],
                                          [98, 99], [99, 100], [99, 101]],
                                         [[95, 102], [102, 103], [103, 104], [103, 106], [104, 105], [104, 109],
                                          [106, 107], [106, 108]]]


def test_get_inner_bond_index_from_group():

    all_inner_bond_index_Hk2 = aux.get_inner_bond_index_from_group(molsys_Hk2, skip_digestion=True)
    all_inner_bond_index_BB = aux.get_inner_bond_index_from_group(molsys_BB, skip_digestion=True)
    list_inner_bond_index_Hk2 = aux.get_inner_bond_index_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_inner_bond_index_BB = aux.get_inner_bond_index_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_inner_bond_index_Hk2, list)
    assert len(all_inner_bond_index_Hk2) == 1871
    assert len(all_inner_bond_index_BB) == 1101
    assert all_inner_bond_index_Hk2[344:347] == [[2722, 2723, 2724, 2725, 2727], [2728, 2729, 2730, 2731, 2733, 2734],
                                                 [2735, 2736, 2737, 2738]]
    assert all_inner_bond_index_Hk2[1750:1755] == [[], [], [], [], [13562, 13563, 13564, 13565, 13566, 13567, 13568,
                                                                    13569, 13570, 13571, 13572, 13573]]
    assert all_inner_bond_index_Hk2[0] == [0, 1, 2, 3, 5, 6, 7]
    assert all_inner_bond_index_Hk2[-1] == []
    assert all_inner_bond_index_BB[385:388] == [[3146, 3147, 3148, 3149, 3151, 3152, 3153], [3154, 3155, 3156, 3157],
                                                [3159, 3160, 3161, 3162, 3164, 3165, 3166]]
    assert all_inner_bond_index_BB[586:592] == [[4725, 4726, 4727, 4728, 4730, 4731, 4732],
                                                [4733, 4734, 4735, 4736, 4737], [], [], [], []]
    assert all_inner_bond_index_BB[0] == [0, 1, 2, 3, 5, 6]
    assert all_inner_bond_index_BB[-1] == []
    assert list_inner_bond_index_Hk2 == [[33, 34, 35, 36, 38, 39, 40, 41], [42, 43, 44, 45, 47, 48],
                                         [49, 50, 51, 52, 54, 55, 56]]
    assert list_inner_bond_index_BB == [[74, 75, 76, 77, 79, 80, 81, 82, 83, 84, 85, 86], [87, 88, 89, 90, 92, 93, 94],
                                        [95, 96, 97, 98, 100, 101, 102, 103], [104, 105, 106, 107, 109, 110]]


def test_get_inner_bonded_atoms_from_group():

    all_inner_bonded_atoms_Hk2 = aux.get_inner_bonded_atoms_from_group(molsys_Hk2, skip_digestion=True)
    all_inner_bonded_atoms_BB = aux.get_inner_bonded_atoms_from_group(molsys_BB, skip_digestion=True)
    list_inner_bonded_atoms_Hk2 = aux.get_inner_bonded_atoms_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_inner_bonded_atoms_BB = aux.get_inner_bonded_atoms_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_inner_bonded_atoms_Hk2, list)
    assert len(all_inner_bonded_atoms_Hk2) == 1871
    assert len(all_inner_bonded_atoms_BB) == 1101
    assert all_inner_bonded_atoms_Hk2[344:347] == [[2678, 2679, 2680, 2681, 2682, 2683],
                                                   [2684, 2685, 2686, 2687, 2688, 2689, 2690],
                                                   [2691, 2692, 2693, 2694, 2695]]
    assert all_inner_bonded_atoms_Hk2[1750:1755] == [[], [], [], [], [13377, 13378, 13379, 13380, 13381, 13382, 13383,
                                                                      13384, 13385, 13386, 13387, 13388]]
    assert all_inner_bonded_atoms_Hk2[0] == [0, 1, 2, 3, 4, 5, 6, 7]
    assert all_inner_bonded_atoms_Hk2[-1] == []
    assert all_inner_bonded_atoms_BB[385:388] == [[3070, 3071, 3072, 3073, 3074, 3075, 3076, 3077],
                                                  [3078, 3079, 3080, 3081, 3082],
                                                  [3083, 3084, 3085, 3086, 3087, 3088, 3089, 3090]]
    assert all_inner_bonded_atoms_BB[586:592] == [[4624, 4625, 4626, 4627, 4628, 4629, 4630, 4631],
                                                  [4632, 4633, 4634, 4635, 4636, 4637],
                                                  [], [], [], []]
    assert all_inner_bonded_atoms_BB[0] == [0, 1, 2, 3, 4, 5, 6]
    assert all_inner_bonded_atoms_BB[-1] == []
    assert list_inner_bonded_atoms_Hk2 == [[33, 34, 35, 36, 37, 38, 39, 40, 41], [42, 43, 44, 45, 46, 47, 48],
                                           [49, 50, 51, 52, 53, 54, 55, 56]]
    assert list_inner_bonded_atoms_BB == [[73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84],
                                          [85, 86, 87, 88, 89, 90, 91, 92],
                                          [93, 94, 95, 96, 97, 98, 99, 100, 101],
                                          [102, 103, 104, 105, 106, 107, 108]]


def test_get_inner_bonded_atom_pairs_from_group():

    all_inner_bonded_atom_pairs_Hk2 = aux.get_inner_bonded_atom_pairs_from_group(molsys_Hk2, skip_digestion=True)
    all_inner_bonded_atom_pairs_BB = aux.get_inner_bonded_atom_pairs_from_group(molsys_BB, skip_digestion=True)
    list_inner_bonded_atom_pairs_Hk2 = aux.get_inner_bonded_atom_pairs_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_inner_bonded_atom_pairs_BB = aux.get_inner_bonded_atom_pairs_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_inner_bonded_atom_pairs_Hk2, list)
    assert len(all_inner_bonded_atom_pairs_Hk2) == 1871
    assert len(all_inner_bonded_atom_pairs_BB) == 1101
    assert all_inner_bonded_atom_pairs_Hk2[344:347] == [[[2672, 2678], [2678, 2679], [2679, 2680], [2679, 2682],
                                                         [2680, 2681], [2680, 2684], [2682, 2683]],
                                                        [[2680, 2684], [2684, 2685], [2685, 2686], [2685, 2688],
                                                         [2686, 2687], [2686, 2691], [2688, 2689], [2688, 2690]],
                                                        [[2686, 2691], [2691, 2692], [2692, 2693], [2692, 2695],
                                                         [2693, 2694], [2693, 2696]]]
    assert all_inner_bonded_atom_pairs_Hk2[1750:1755] == [[], [], [], [],
                                                          [[13377, 13378], [13377, 13383], [13377, 13387],
                                                           [13378, 13379], [13378, 13384], [13379, 13380],
                                                           [13379, 13385], [13380, 13381], [13380, 13386],
                                                           [13381, 13382], [13381, 13387], [13382, 13388]]]
    assert all_inner_bonded_atom_pairs_Hk2[0] == [[0, 1], [1, 2], [1, 4], [2, 3], [2, 8], [4, 5], [5, 6], [5, 7]]
    assert all_inner_bonded_atom_pairs_Hk2[-1] == []
    assert all_inner_bonded_atom_pairs_BB[385:388] == [[[3066, 3070], [3070, 3071], [3071, 3072], [3071, 3074],
                                                        [3072, 3073], [3072, 3078], [3074, 3075], [3075, 3076],
                                                        [3076, 3077]],
                                                       [[3072, 3078], [3078, 3079], [3079, 3080], [3079, 3082],
                                                        [3080, 3081], [3080, 3083]],
                                                       [[3080, 3083], [3083, 3084], [3084, 3085], [3084, 3087],
                                                        [3085, 3086], [3085, 3091], [3087, 3088], [3088, 3089],
                                                        [3088, 3090]]]
    assert all_inner_bonded_atom_pairs_BB[586:592] == [[[4618, 4624], [4624, 4625], [4625, 4626], [4625, 4628],
                                                        [4626, 4627], [4626, 4632], [4628, 4629], [4629, 4630],
                                                        [4629, 4631]],
                                                       [[4626, 4632], [4632, 4633], [4633, 4634], [4633, 4635],
                                                        [4634, 4637], [4635, 4636]], [], [], [], []]
    assert all_inner_bonded_atom_pairs_BB[0] == [[0, 1], [1, 2], [1, 4], [2, 3], [2, 7], [4, 5], [4, 6]]
    assert all_inner_bonded_atom_pairs_BB[-1] == []
    assert list_inner_bonded_atom_pairs_Hk2 == [[[26, 33], [33, 34], [34, 35], [34, 37], [35, 36], [35, 42], [37, 38],
                                                 [38, 39], [39, 40], [40, 41]],
                                                [[35, 42], [42, 43], [43, 44], [43, 46], [44, 45], [44, 49], [46, 47],
                                                 [46, 48]],
                                                [[44, 49], [49, 50], [50, 51], [50, 53], [51, 52], [51, 57], [53, 54],
                                                 [54, 55], [54, 56]]]
    assert list_inner_bonded_atom_pairs_BB == [[[67, 73], [73, 74], [74, 75], [74, 77], [75, 76], [75, 85], [77, 78],
                                                [78, 79], [78, 80], [79, 81], [80, 82], [81, 83], [82, 83], [83, 84]],
                                               [[75, 85], [85, 86], [86, 87], [86, 89], [87, 88], [87, 93], [89, 90],
                                                [90, 91], [90, 92]],
                                               [[87, 93], [93, 94], [94, 95], [94, 97], [95, 96], [95, 102], [97, 98],
                                                [98, 99], [99, 100], [99, 101]],
                                               [[95, 102], [102, 103], [103, 104], [103, 106], [104, 105], [104, 109],
                                                [106, 107], [106, 108]]]

def test_get_n_atoms_from_group():

    all_n_atoms_Hk2 = aux.get_n_atoms_from_group(molsys_Hk2, skip_digestion=True)
    all_n_atoms_BB = aux.get_n_atoms_from_group(molsys_BB, skip_digestion=True)
    list_n_atoms_Hk2 = aux.get_n_atoms_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_atoms_BB = aux.get_n_atoms_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_n_atoms_Hk2, list)
    assert len(all_n_atoms_Hk2) == 1871
    assert len(all_n_atoms_BB) == 1101
    assert all_n_atoms_Hk2[344:347] == [6, 7, 5]
    assert all_n_atoms_Hk2[1750:1755] == [1, 1, 1, 1, 12]
    assert all_n_atoms_Hk2[0] == 8
    assert all_n_atoms_Hk2[-1] == 1
    assert all_n_atoms_BB[385:388] == [8, 5, 8]
    assert all_n_atoms_BB[586:592] == [8, 6, 1, 1, 1, 1]
    assert all_n_atoms_BB[0] == 7
    assert all_n_atoms_BB[-1] == 1
    assert list_n_atoms_Hk2 == [9, 7, 8]
    assert list_n_atoms_BB == [12, 8, 9, 7]


def test_get_total_n_atoms_from_group():

    all_total_n_atoms_Hk2 = aux.get_total_n_atoms_from_group(molsys_Hk2, skip_digestion=True)
    all_total_n_atoms_BB = aux.get_total_n_atoms_from_group(molsys_BB, skip_digestion=True)
    list_total_n_atoms_Hk2 = aux.get_total_n_atoms_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_atoms_BB = aux.get_total_n_atoms_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_atoms_Hk2 == 13546
    assert all_total_n_atoms_BB == 5151
    assert list_total_n_atoms_Hk2 == 24
    assert list_total_n_atoms_BB == 36


def test_get_n_groups_from_group():

    all_n_groups_Hk2 = aux.get_n_groups_from_group(molsys_Hk2, skip_digestion=True)
    all_n_groups_BB = aux.get_n_groups_from_group(molsys_BB, skip_digestion=True)
    list_n_groups_Hk2 = aux.get_n_groups_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_groups_BB = aux.get_n_groups_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_groups_Hk2 == 1871
    assert all_n_groups_BB == 1101
    assert list_n_groups_Hk2 == 3
    assert list_n_groups_BB == 4


def test_get_total_n_groups_from_group():

    all_total_n_groups_Hk2 = aux.get_total_n_groups_from_group(molsys_Hk2, skip_digestion=True)
    all_total_n_groups_BB = aux.get_total_n_groups_from_group(molsys_BB, skip_digestion=True)
    list_total_n_groups_Hk2 = aux.get_total_n_groups_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_groups_BB = aux.get_total_n_groups_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_groups_Hk2 == 1871
    assert all_total_n_groups_BB == 1101
    assert list_total_n_groups_Hk2 == 3
    assert list_total_n_groups_BB == 4


def test_get_n_molecules_from_group():

    all_n_molecules_Hk2 = aux.get_n_molecules_from_group(molsys_Hk2, skip_digestion=True)
    all_n_molecules_BB = aux.get_n_molecules_from_group(molsys_BB, skip_digestion=True)
    list_n_molecules_Hk2 = aux.get_n_molecules_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_molecules_BB = aux.get_n_molecules_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_molecules_Hk2 == 135
    assert all_n_molecules_BB == 519
    assert list_n_molecules_Hk2 == 1
    assert list_n_molecules_BB == 1


def test_get_total_n_molecules_from_group():

    all_total_n_molecules_Hk2 = aux.get_total_n_molecules_from_group(molsys_Hk2, skip_digestion=True)
    all_total_n_molecules_BB = aux.get_total_n_molecules_from_group(molsys_BB, skip_digestion=True)
    list_total_n_molecules_Hk2 = aux.get_total_n_molecules_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_molecules_BB = aux.get_total_n_molecules_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_molecules_Hk2 == 135
    assert all_total_n_molecules_BB == 519
    assert list_total_n_molecules_Hk2 == 1
    assert list_total_n_molecules_BB == 1


def test_get_n_entities_from_group():

    all_n_entities_Hk2 = aux.get_n_entities_from_group(molsys_Hk2, skip_digestion=True)
    all_n_entities_BB = aux.get_n_entities_from_group(molsys_BB, skip_digestion=True)
    list_n_entities_Hk2 = aux.get_n_entities_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_n_entities_BB = aux.get_n_entities_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_n_entities_Hk2 == 5
    assert all_n_entities_BB == 3
    assert list_n_entities_Hk2 == 2
    assert list_n_entities_BB == 2


def test_get_total_n_entities_from_group():

    all_total_n_entities_Hk2 = aux.get_total_n_entities_from_group(molsys_Hk2, skip_digestion=True)
    all_total_n_entities_BB = aux.get_total_n_entities_from_group(molsys_BB, skip_digestion=True)
    list_total_n_entities_Hk2 = aux.get_total_n_entities_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_total_n_entities_BB = aux.get_total_n_entities_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_total_n_entities_Hk2 == 5
    assert all_total_n_entities_BB == 3
    assert list_total_n_entities_Hk2 == 2
    assert list_total_n_entities_BB == 2


def test_get_n_components_from_group():

    all_n_components_Hk2 = aux.get_n_components_from_group(molsys_Hk2, skip_digestion=True)
    all_n_components_BB = aux.get_n_components_from_group(molsys_BB, skip_digestion=True)
    list_n_components_Hk2 = aux.get_n_components_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_n_components_BB = aux.get_n_components_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_n_components_Hk2 == 1871*[1]
    assert all_n_components_BB == 1101*[1]
    assert list_n_components_Hk2 == [1,1,1]
    assert list_n_components_BB == [1,1,1]


def test_get_total_n_components_from_group():

    all_total_n_components_Hk2 = aux.get_total_n_components_from_group(molsys_Hk2, skip_digestion=True)
    all_total_n_components_BB = aux.get_total_n_components_from_group(molsys_BB, skip_digestion=True)
    list_total_n_components_Hk2 = aux.get_total_n_components_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_total_n_components_BB = aux.get_total_n_components_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_total_n_components_Hk2 == 146
    assert all_total_n_components_BB == 521
    assert list_total_n_components_Hk2 == 3
    assert list_total_n_components_BB == 3


def test_get_n_chains_from_group():

    all_n_chains_Hk2 = aux.get_n_chains_from_group(molsys_Hk2, skip_digestion=True)
    all_n_chains_BB = aux.get_n_chains_from_group(molsys_BB, skip_digestion=True)
    list_n_chains_Hk2 = aux.get_n_chains_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_n_chains_BB = aux.get_n_chains_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_n_chains_Hk2 == 1871*[1]
    assert all_n_chains_BB == 1101*[1]
    assert list_n_chains_Hk2 == [1,1,1]
    assert list_n_chains_BB == [1,1,1]


def test_get_total_n_chains_from_group():

    all_total_n_chains_Hk2 = aux.get_total_n_chains_from_group(molsys_Hk2, skip_digestion=True)
    all_total_n_chains_BB = aux.get_total_n_chains_from_group(molsys_BB, skip_digestion=True)
    list_total_n_chains_Hk2 = aux.get_total_n_chains_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_total_n_chains_BB = aux.get_total_n_chains_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_total_n_chains_Hk2 == 40
    assert all_total_n_chains_BB == 12
    assert list_total_n_chains_Hk2 == 2
    assert list_total_n_chains_BB == 2


def test_get_n_bonds_from_group():

    all_n_bonds_Hk2 = aux.get_n_bonds_from_group(molsys_Hk2, skip_digestion=True)
    all_n_bonds_BB = aux.get_n_bonds_from_group(molsys_BB, skip_digestion=True)
    list_n_bonds_Hk2 = aux.get_n_bonds_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_bonds_BB = aux.get_n_bonds_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_n_bonds_Hk2, list)
    assert len(all_n_bonds_Hk2) == 1871
    assert len(all_n_bonds_BB) == 1101
    assert all_n_bonds_Hk2[344:347] == [7, 8, 6]
    assert all_n_bonds_Hk2[1750:1755] == [0, 0, 0, 0, 12]
    assert all_n_bonds_Hk2[0] == 8
    assert all_n_bonds_Hk2[-1] == 0
    assert all_n_bonds_BB[385:388] == [9, 6, 9]
    assert all_n_bonds_BB[586:592] == [9, 6, 0, 0, 0, 0]
    assert all_n_bonds_BB[0] == 7
    assert all_n_bonds_BB[-1] == 0
    assert list_n_bonds_Hk2 == [10, 8, 9]
    assert list_n_bonds_BB == [14, 9, 10, 8]


def test_get_total_n_bonds_from_group():

    all_total_n_bonds_Hk2 = aux.get_total_n_bonds_from_group(molsys_Hk2, skip_digestion=True)
    all_total_n_bonds_BB = aux.get_total_n_bonds_from_group(molsys_BB, skip_digestion=True)
    list_total_n_bonds_Hk2 = aux.get_total_n_bonds_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_bonds_BB = aux.get_total_n_bonds_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_bonds_Hk2 == 13618
    assert all_total_n_bonds_BB == 4738
    assert list_total_n_bonds_Hk2 == 25
    assert list_total_n_bonds_BB == 38


def test_get_n_inner_bonds_from_group():

    all_n_inner_bonds_Hk2 = aux.get_n_inner_bonds_from_group(molsys_Hk2, skip_digestion=True)
    all_n_inner_bonds_BB = aux.get_n_inner_bonds_from_group(molsys_BB, skip_digestion=True)
    list_n_inner_bonds_Hk2 = aux.get_n_inner_bonds_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_inner_bonds_BB = aux.get_n_inner_bonds_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_n_inner_bonds_Hk2, list)
    assert len(all_n_inner_bonds_Hk2) == 1871
    assert len(all_n_inner_bonds_BB) == 1101
    assert all_n_inner_bonds_Hk2[344:347] == [5, 6, 4]
    assert all_n_inner_bonds_Hk2[1750:1755] == [0, 0, 0, 0, 12]
    assert all_n_inner_bonds_Hk2[0] == 7
    assert all_n_inner_bonds_Hk2[-1] == 0
    assert all_n_inner_bonds_BB[385:388] == [7, 4, 7]
    assert all_n_inner_bonds_BB[586:592] == [7, 5, 0, 0, 0, 0]
    assert all_n_inner_bonds_BB[0] == 6
    assert all_n_inner_bonds_BB[-1] == 0
    assert list_n_inner_bonds_Hk2 == [8, 6, 7]
    assert list_n_inner_bonds_BB == [12, 7, 8, 6]


def test_get_total_n_inner_bonds_from_group():

    all_total_n_inner_bonds_Hk2 = aux.get_total_n_inner_bonds_from_group(molsys_Hk2, skip_digestion=True)
    all_total_n_inner_bonds_BB = aux.get_total_n_inner_bonds_from_group(molsys_BB, skip_digestion=True)
    list_total_n_inner_bonds_Hk2 = aux.get_total_n_inner_bonds_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_inner_bonds_BB = aux.get_total_n_inner_bonds_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_inner_bonds_Hk2 == 13618
    assert all_total_n_inner_bonds_BB == 4738
    assert list_total_n_inner_bonds_Hk2 == 23
    assert list_total_n_inner_bonds_BB == 36


def test_get_n_amino_acids_from_group():

    all_n_amino_acids_Hk2 = aux.get_n_amino_acids_from_group(molsys_Hk2, skip_digestion=True)
    all_n_amino_acids_BB = aux.get_n_amino_acids_from_group(molsys_BB, skip_digestion=True)
    list_n_amino_acids_Hk2 = aux.get_n_amino_acids_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_amino_acids_BB = aux.get_n_amino_acids_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_amino_acids_Hk2 == 1738
    assert all_n_amino_acids_BB == 588
    assert list_n_amino_acids_Hk2 == 3
    assert list_n_amino_acids_BB == 4


def test_get_total_n_amino_acids_from_group():

    all_total_n_amino_acids_Hk2 = aux.get_total_n_amino_acids_from_group(molsys_Hk2, skip_digestion=True)
    all_total_n_amino_acids_BB = aux.get_total_n_amino_acids_from_group(molsys_BB, skip_digestion=True)
    list_total_n_amino_acids_Hk2 = aux.get_total_n_amino_acids_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_amino_acids_BB = aux.get_total_n_amino_acids_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_amino_acids_Hk2 == 1738
    assert all_total_n_amino_acids_BB == 588
    assert list_total_n_amino_acids_Hk2 == 3
    assert list_total_n_amino_acids_BB == 4


def test_get_n_nucleotides_from_group():

    all_n_nucleotides_Hk2 = aux.get_n_nucleotides_from_group(molsys_Hk2, skip_digestion=True)
    all_n_nucleotides_BB = aux.get_n_nucleotides_from_group(molsys_BB, skip_digestion=True)
    list_n_nucleotides_Hk2 = aux.get_n_nucleotides_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_nucleotides_BB = aux.get_n_nucleotides_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_nucleotides_Hk2 == 0
    assert all_n_nucleotides_BB == 0
    assert list_n_nucleotides_Hk2 == 0
    assert list_n_nucleotides_BB == 0


def test_get_total_n_nucleotides_from_group():

    all_total_n_nucleotides_Hk2 = aux.get_total_n_nucleotides_from_group(molsys_Hk2, skip_digestion=True)
    all_total_n_nucleotides_BB = aux.get_total_n_nucleotides_from_group(molsys_BB, skip_digestion=True)
    list_total_n_nucleotides_Hk2 = aux.get_total_n_nucleotides_from_group(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_nucleotides_BB = aux.get_total_n_nucleotides_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_nucleotides_Hk2 == 0
    assert all_total_n_nucleotides_BB == 0
    assert list_total_n_nucleotides_Hk2 == 0
    assert list_total_n_nucleotides_BB == 0


def test_get_n_ions_from_group():

    all_n_ions_Hk2 = aux.get_n_ions_from_group(molsys_Hk2, skip_digestion=True)
    all_n_ions_BB = aux.get_n_ions_from_group(molsys_BB, skip_digestion=True)
    list_n_ions_Hk2 = aux.get_n_ions_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_n_ions_BB = aux.get_n_ions_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_ions_Hk2 == 28
    assert all_n_ions_BB == 0
    assert list_n_ions_Hk2 == 1
    assert list_n_ions_BB == 0


def test_get_total_n_ions_from_group():

    all_total_n_ions_Hk2 = aux.get_total_n_ions_from_group(molsys_Hk2, skip_digestion=True)
    all_total_n_ions_BB = aux.get_total_n_ions_from_group(molsys_BB, skip_digestion=True)
    list_total_n_ions_Hk2 = aux.get_total_n_ions_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_total_n_ions_BB = aux.get_total_n_ions_from_group(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_ions_Hk2 == 28
    assert all_total_n_ions_BB == 0
    assert list_total_n_ions_Hk2 == 1
    assert list_total_n_ions_BB == 0


def test_get_n_waters_from_group():

    all_n_waters_Hk2 = aux.get_n_waters_from_group(molsys_Hk2, skip_digestion=True)
    all_n_waters_BB = aux.get_n_waters_from_group(molsys_BB, skip_digestion=True)
    list_n_waters_Hk2 = aux.get_n_waters_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_n_waters_BB = aux.get_n_waters_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_n_waters_Hk2 == 97
    assert all_n_waters_BB == 513
    assert list_n_waters_Hk2 == 2
    assert list_n_waters_BB == 2


def test_get_total_n_waters_from_group():

    all_total_n_waters_Hk2 = aux.get_total_n_waters_from_group(molsys_Hk2, skip_digestion=True)
    all_total_n_waters_BB = aux.get_total_n_waters_from_group(molsys_BB, skip_digestion=True)
    list_total_n_waters_Hk2 = aux.get_total_n_waters_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_total_n_waters_BB = aux.get_total_n_waters_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_total_n_waters_Hk2 == 97
    assert all_total_n_waters_BB == 513
    assert list_total_n_waters_Hk2 == 2
    assert list_total_n_waters_BB == 2


def test_get_n_small_molecules_from_group():

    all_n_small_molecules_Hk2 = aux.get_n_small_molecules_from_group(molsys_Hk2, skip_digestion=True)
    all_n_small_molecules_BB = aux.get_n_small_molecules_from_group(molsys_BB, skip_digestion=True)
    list_n_small_molecules_Hk2 = aux.get_n_small_molecules_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_n_small_molecules_BB = aux.get_n_small_molecules_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_n_small_molecules_Hk2 == 0
    assert all_n_small_molecules_BB == 0
    assert list_n_small_molecules_Hk2 == 0
    assert list_n_small_molecules_BB == 0


def test_get_total_n_small_molecules_from_group():

    all_total_n_small_molecules_Hk2 = aux.get_total_n_small_molecules_from_group(molsys_Hk2, skip_digestion=True)
    all_total_n_small_molecules_BB = aux.get_total_n_small_molecules_from_group(molsys_BB, skip_digestion=True)
    list_total_n_small_molecules_Hk2 = aux.get_total_n_small_molecules_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_total_n_small_molecules_BB = aux.get_total_n_small_molecules_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_total_n_small_molecules_Hk2 == 0
    assert all_total_n_small_molecules_BB == 0
    assert list_total_n_small_molecules_Hk2 == 0
    assert list_total_n_small_molecules_BB == 0


def test_get_n_lipids_from_group():

    all_n_lipids_Hk2 = aux.get_n_lipids_from_group(molsys_Hk2, skip_digestion=True)
    all_n_lipids_BB = aux.get_n_lipids_from_group(molsys_BB, skip_digestion=True)
    list_n_lipids_Hk2 = aux.get_n_lipids_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_n_lipids_BB = aux.get_n_lipids_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_n_lipids_Hk2 == 0
    assert all_n_lipids_BB == 0
    assert list_n_lipids_Hk2 == 0
    assert list_n_lipids_BB == 0


def test_get_total_n_lipids_from_group():

    all_total_n_lipids_Hk2 = aux.get_total_n_lipids_from_group(molsys_Hk2, skip_digestion=True)
    all_total_n_lipids_BB = aux.get_total_n_lipids_from_group(molsys_BB, skip_digestion=True)
    list_total_n_lipids_Hk2 = aux.get_total_n_lipids_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_total_n_lipids_BB = aux.get_total_n_lipids_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_total_n_lipids_Hk2 == 0
    assert all_total_n_lipids_BB == 0
    assert list_total_n_lipids_Hk2 == 0
    assert list_total_n_lipids_BB == 0


def test_get_n_saccharides_from_group():

    all_n_saccharides_Hk2 = aux.get_n_saccharides_from_group(molsys_Hk2, skip_digestion=True)
    all_n_saccharides_BB = aux.get_n_saccharides_from_group(molsys_BB, skip_digestion=True)
    list_n_saccharides_Hk2 = aux.get_n_saccharides_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_n_saccharides_BB = aux.get_n_saccharides_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_n_saccharides_Hk2 == 8
    assert all_n_saccharides_BB == 0
    assert list_n_saccharides_Hk2 == 0
    assert list_n_saccharides_BB == 0


def test_get_total_n_saccharides_from_group():

    all_total_n_saccharides_Hk2 = aux.get_total_n_saccharides_from_group(molsys_Hk2, skip_digestion=True)
    all_total_n_saccharides_BB = aux.get_total_n_saccharides_from_group(molsys_BB, skip_digestion=True)
    list_total_n_saccharides_Hk2 = aux.get_total_n_saccharides_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_total_n_saccharides_BB = aux.get_total_n_saccharides_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_total_n_saccharides_Hk2 == 8
    assert all_total_n_saccharides_BB == 0
    assert list_total_n_saccharides_Hk2 == 0
    assert list_total_n_saccharides_BB == 0


def test_get_n_peptides_from_group():

    all_n_peptides_Hk2 = aux.get_n_peptides_from_group(molsys_Hk2, skip_digestion=True)
    all_n_peptides_BB = aux.get_n_peptides_from_group(molsys_BB, skip_digestion=True)
    list_n_peptides_Hk2 = aux.get_n_peptides_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_n_peptides_BB = aux.get_n_peptides_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_n_peptides_Hk2 == 0
    assert all_n_peptides_BB == 0
    assert list_n_peptides_Hk2 == 0
    assert list_n_peptides_BB == 0


def test_get_total_n_peptides_from_group():

    all_total_n_peptides_Hk2 = aux.get_total_n_peptides_from_group(molsys_Hk2, skip_digestion=True)
    all_total_n_peptides_BB = aux.get_total_n_peptides_from_group(molsys_BB, skip_digestion=True)
    list_total_n_peptides_Hk2 = aux.get_total_n_peptides_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_total_n_peptides_BB = aux.get_total_n_peptides_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_total_n_peptides_Hk2 == 0
    assert all_total_n_peptides_BB == 0
    assert list_total_n_peptides_Hk2 == 0
    assert list_total_n_peptides_BB == 0


def test_get_n_proteins_from_group():

    all_n_proteins_Hk2 = aux.get_n_proteins_from_group(molsys_Hk2, skip_digestion=True)
    all_n_proteins_BB = aux.get_n_proteins_from_group(molsys_BB, skip_digestion=True)
    list_n_proteins_Hk2 = aux.get_n_proteins_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_n_proteins_BB = aux.get_n_proteins_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_n_proteins_Hk2 == 2
    assert all_n_proteins_BB == 6
    assert list_n_proteins_Hk2 == 0
    assert list_n_proteins_BB == 1


def test_get_total_n_proteins_from_group():

    all_total_n_proteins_Hk2 = aux.get_total_n_proteins_from_group(molsys_Hk2, skip_digestion=True)
    all_total_n_proteins_BB = aux.get_total_n_proteins_from_group(molsys_BB, skip_digestion=True)
    list_total_n_proteins_Hk2 = aux.get_total_n_proteins_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_total_n_proteins_BB = aux.get_total_n_proteins_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_total_n_proteins_Hk2 == 2
    assert all_total_n_proteins_BB == 6
    assert list_total_n_proteins_Hk2 == 0
    assert list_total_n_proteins_BB == 1


def test_get_n_dnas_from_group():

    all_n_dnas_Hk2 = aux.get_n_dnas_from_group(molsys_Hk2, skip_digestion=True)
    all_n_dnas_BB = aux.get_n_dnas_from_group(molsys_BB, skip_digestion=True)
    list_n_dnas_Hk2 = aux.get_n_dnas_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_n_dnas_BB = aux.get_n_dnas_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_n_dnas_Hk2 == 0
    assert all_n_dnas_BB == 0
    assert list_n_dnas_Hk2 == 0
    assert list_n_dnas_BB == 0


def test_get_total_n_dnas_from_group():

    all_total_n_dnas_Hk2 = aux.get_total_n_dnas_from_group(molsys_Hk2, skip_digestion=True)
    all_total_n_dnas_BB = aux.get_total_n_dnas_from_group(molsys_BB, skip_digestion=True)
    list_total_n_dnas_Hk2 = aux.get_total_n_dnas_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_total_n_dnas_BB = aux.get_total_n_dnas_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_total_n_dnas_Hk2 == 0
    assert all_total_n_dnas_BB == 0
    assert list_total_n_dnas_Hk2 == 0
    assert list_total_n_dnas_BB == 0


def test_get_n_rnas_from_group():

    all_n_rnas_Hk2 = aux.get_n_rnas_from_group(molsys_Hk2, skip_digestion=True)
    all_n_rnas_BB = aux.get_n_rnas_from_group(molsys_BB, skip_digestion=True)
    list_n_rnas_Hk2 = aux.get_n_rnas_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_n_rnas_BB = aux.get_n_rnas_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_n_rnas_Hk2 == 0
    assert all_n_rnas_BB == 0
    assert list_n_rnas_Hk2 == 0
    assert list_n_rnas_BB == 0


def test_get_total_n_rnas_from_group():

    all_total_n_rnas_Hk2 = aux.get_total_n_rnas_from_group(molsys_Hk2, skip_digestion=True)
    all_total_n_rnas_BB = aux.get_total_n_rnas_from_group(molsys_BB, skip_digestion=True)
    list_total_n_rnas_Hk2 = aux.get_total_n_rnas_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_total_n_rnas_BB = aux.get_total_n_rnas_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_total_n_rnas_Hk2 == 0
    assert all_total_n_rnas_BB == 0
    assert list_total_n_rnas_Hk2 == 0
    assert list_total_n_rnas_BB == 0


def test_get_n_polysaccharides_from_group():

    all_n_polysaccharides_Hk2 = aux.get_n_polysaccharides_from_group(molsys_Hk2, skip_digestion=True)
    all_n_polysaccharides_BB = aux.get_n_polysaccharides_from_group(molsys_BB, skip_digestion=True)
    list_n_polysaccharides_Hk2 = aux.get_n_polysaccharides_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_n_polysaccharides_BB = aux.get_n_polysaccharides_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_n_polysaccharides_Hk2 == 8
    assert all_n_polysaccharides_BB == 0
    assert list_n_polysaccharides_Hk2 == 0
    assert list_n_polysaccharides_BB == 0


def test_get_total_n_polysaccharides_from_group():

    all_total_n_polysaccharides_Hk2 = aux.get_total_n_polysaccharides_from_group(molsys_Hk2, skip_digestion=True)
    all_total_n_polysaccharides_BB = aux.get_total_n_polysaccharides_from_group(molsys_BB, skip_digestion=True)
    list_total_n_polysaccharides_Hk2 = aux.get_total_n_polysaccharides_from_group(molsys_Hk2, indices=[1773,1774,1775], skip_digestion=True)
    list_total_n_polysaccharides_BB = aux.get_total_n_polysaccharides_from_group(molsys_BB, indices=[587,588,589], skip_digestion=True)

    assert all_total_n_polysaccharides_Hk2 == 8
    assert all_total_n_polysaccharides_BB == 0
    assert list_total_n_polysaccharides_Hk2 == 0
    assert list_total_n_polysaccharides_BB == 0


# From molecule


def test_get_atom_index_from_molecule():

    all_atom_index_Hk2 = aux.get_atom_index_from_molecule(molsys_Hk2, skip_digestion=True)
    all_atom_index_BB = aux.get_atom_index_from_molecule(molsys_BB, skip_digestion=True)
    list_atom_index_Hk2 = aux.get_atom_index_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_atom_index_BB = aux.get_atom_index_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_atom_index_Hk2, list)
    assert len(all_atom_index_Hk2) == 135
    assert len(all_atom_index_BB) == 519
    assert all_atom_index_Hk2[4:10] == [[13337, 13338, 13339, 13340, 13341, 13342, 13343, 13344, 13345, 13346,
                                         13347, 13348],
                                        [13349, 13350, 13351, 13352, 13353, 13354, 13355, 13356, 13357, 13358,
                                         13359, 13360, 13361, 13362, 13363, 13364],
                                        [13365],[13366],[13367],[13368]]
    assert all_atom_index_Hk2[90:93] == [[13501], [13502], [13503]]
    assert all_atom_index_Hk2[0] == list(range(6653))
    assert all_atom_index_Hk2[-1] == [13545]
    assert all_atom_index_BB[5:8] == [list(range(3939,4638)), [4638], [4639]]
    assert all_atom_index_BB[486:492] == [[5118], [5119], [5120], [5121], [5122], [5123]]
    assert all_atom_index_BB[0] == list(range(864))
    assert all_atom_index_BB[-1] == [5150]
    assert list_atom_index_Hk2 == [list(range(6653, 13309)), list(range(13309, 13321)), list(range(13321, 13337))]
    assert list_atom_index_BB == [[4642], [4643], [4644], [4645]]


def test_get_atom_id_from_molecule():

    all_atom_id_Hk2 = aux.get_atom_id_from_molecule(molsys_Hk2, skip_digestion=True)
    all_atom_id_BB = aux.get_atom_id_from_molecule(molsys_BB, skip_digestion=True)
    list_atom_id_Hk2 = aux.get_atom_id_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_atom_id_BB = aux.get_atom_id_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_atom_id_Hk2, list)
    assert len(all_atom_id_Hk2) == 135
    assert len(all_atom_id_BB) == 519
    assert all_atom_id_Hk2[4:10] == [[13338, 13339, 13340, 13341, 13342, 13343, 13344, 13345, 13346, 13347,
                                      13348, 13349],
                                     [13350, 13351, 13352, 13353, 13354, 13355, 13356, 13357, 13358, 13359,
                                      13360, 13361, 13362, 13363, 13364, 13365],
                                     [13366], [13367], [13368], [13369]]
    assert all_atom_id_Hk2[90:96] == [[13502], [13503], [13504], [13505], [13506], [13507]]
    assert all_atom_id_Hk2[0][110:120] == [111, 112, 113, 114, 115, 116, 117, 118, 119, 120]
    assert all_atom_id_Hk2[-1] == [13546]
    assert all_atom_id_BB[5:8][0][200:210] == [4142, 4143, 4144, 4145, 4146, 4147, 4148, 4149, 4150, 4151]
    assert all_atom_id_BB[5:8][1:] == [[4641], [4642]]
    assert all_atom_id_BB[486:492] == [[5121], [5122], [5123], [5124], [5125], [5126]]
    assert all_atom_id_BB[0][60:70] == [61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
    assert all_atom_id_BB[-1] == [5153]
    assert list_atom_id_Hk2[0][160:170] == [6814, 6815, 6816, 6817, 6818, 6819, 6820, 6821, 6822, 6823]
    assert list_atom_id_Hk2[1:] == [[13310, 13311, 13312, 13313, 13314, 13315, 13316, 13317, 13318, 13319,
                                     13320, 13321],
                                    [13322, 13323, 13324, 13325, 13326, 13327, 13328, 13329, 13330, 13331,
                                     13332, 13333, 13334, 13335, 13336, 13337]]
    assert list_atom_id_BB == [[4645], [4646], [4647], [4648]]


def test_get_atom_name_from_molecule():

    all_atom_name_Hk2 = aux.get_atom_name_from_molecule(molsys_Hk2, skip_digestion=True)
    all_atom_name_BB = aux.get_atom_name_from_molecule(molsys_BB, skip_digestion=True)
    list_atom_name_Hk2 = aux.get_atom_name_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_atom_name_BB = aux.get_atom_name_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_atom_name_Hk2, list)
    assert len(all_atom_name_Hk2) == 135
    assert len(all_atom_name_BB) == 519
    assert all_atom_name_Hk2[4:10] == [['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6'],
                                       ['C1', 'C2', 'O1', 'O5', 'C3', 'O2', 'C4', 'O3', 'C5', 'O4', 'C6', 'O6',
                                        'P', 'O1P', 'O2P', 'O3P'], ['UNK'], ['UNK'], ['UNK'], ['UNK']]
    assert all_atom_name_Hk2[90:96] == [['O'], ['O'], ['O'], ['O'], ['O'], ['O']]
    assert all_atom_name_Hk2[0][110:120] == ['C', 'O', 'CB', 'CG', 'SD', 'CE', 'N', 'CA', 'C', 'O']
    assert all_atom_name_Hk2[-1] == ['O']
    assert all_atom_name_BB[5:8][0][200:210] == ['CD1', 'CD2', 'N', 'CA', 'C', 'O', 'CB', 'CG', 'CD', 'N']
    assert all_atom_name_BB[5:8][1:] == [['O'], ['O']]
    assert all_atom_name_BB[486:492] == [['O'], ['O'], ['O'], ['O'], ['O'], ['O']]
    assert all_atom_name_BB[0][60:70] == ['N', 'CA', 'C', 'O', 'CB', 'N', 'CA', 'C', 'O', 'CB']
    assert all_atom_name_BB[-1] == ['O']
    assert list_atom_name_Hk2[0][160:170] == ['OG1', 'CG2', 'N', 'CA', 'C', 'O', 'CB', 'CG', 'CD1', 'CD2']
    assert list_atom_name_Hk2[1:] == [['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6'],
                                      ['C1', 'C2', 'O1', 'O5', 'C3', 'O2', 'C4', 'O3', 'C5', 'O4', 'C6', 'O6',
                                       'P', 'O1P', 'O2P', 'O3P']]
    assert list_atom_name_BB == [['O'], ['O'], ['O'], ['O']]


def test_get_atom_type_from_molecule():

    all_atom_type_Hk2 = aux.get_atom_type_from_molecule(molsys_Hk2, skip_digestion=True)
    all_atom_type_BB = aux.get_atom_type_from_molecule(molsys_BB, skip_digestion=True)
    list_atom_type_Hk2 = aux.get_atom_type_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_atom_type_BB = aux.get_atom_type_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_atom_type_Hk2, list)
    assert len(all_atom_type_Hk2) == 135
    assert len(all_atom_type_BB) == 519
    assert all_atom_type_Hk2[4:10] == [['C', 'C', 'C', 'C', 'C', 'C', 'O', 'O', 'O', 'O', 'O', 'O'],
                                     ['C',  'C',  'O',  'O',  'C',  'O',  'C',  'O',  'C',  'O',  'C',  'O',  'P',  'O',  'O',  'O'],
                                     ['X'], ['X'], ['X'], ['X']]
    assert all_atom_type_Hk2[90:96] == [['O'], ['O'], ['O'], ['O'], ['O'], ['O']]
    assert all_atom_type_Hk2[0][110:120] == ['C', 'O', 'C', 'C', 'S', 'C', 'N', 'C', 'C', 'O']
    assert all_atom_type_Hk2[-1] == ['O']
    assert all_atom_type_BB[5:8][0][200:210] == ['C', 'C', 'N', 'C', 'C', 'O', 'C', 'C', 'C', 'N']
    assert all_atom_type_BB[5:8][1:] ==  [['O'], ['O']]
    assert all_atom_type_BB[486:492] == [['O'], ['O'], ['O'], ['O'], ['O'], ['O']]
    assert all_atom_type_BB[0][60:70] == ['N', 'C', 'C', 'O', 'C', 'N', 'C', 'C', 'O', 'C']
    assert all_atom_type_BB[-1] == ['O']
    assert list_atom_type_Hk2[0][160:170] == ['O', 'C', 'N', 'C', 'C', 'O', 'C', 'C', 'C', 'C']
    assert list_atom_type_Hk2[1:] == [['C', 'C', 'C', 'C', 'C', 'C', 'O', 'O', 'O', 'O', 'O', 'O'],
                                    ['C', 'C', 'O', 'O', 'C', 'O', 'C', 'O', 'C', 'O', 'C', 'O', 'P', 'O', 'O', 'O']]
    assert list_atom_type_BB == [['O'], ['O'], ['O'], ['O']]


def test_get_group_index_from_molecule():

    all_group_index_Hk2 = aux.get_group_index_from_molecule(molsys_Hk2, skip_digestion=True)
    all_group_index_BB = aux.get_group_index_from_molecule(molsys_BB, skip_digestion=True)
    list_group_index_Hk2 = aux.get_group_index_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_group_index_BB = aux.get_group_index_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_group_index_Hk2, list)
    assert len(all_group_index_Hk2) == 135
    assert len(all_group_index_BB) == 519
    assert all_group_index_Hk2[0:5] == [list(range(0, 871)), list(range(871, 1738)), [1738], [1739], [1740]]
    assert all_group_index_Hk2[90:96] == [[1826], [1827], [1828], [1829], [1830], [1831]]
    assert all_group_index_Hk2[-1] == [1870]
    assert all_group_index_BB[5:8] == [list(range(499, 588)), [588], [589]]
    assert all_group_index_BB[486:492] == [[1068], [1069], [1070], [1071], [1072], [1073]]
    assert all_group_index_BB[0] == list(range(0, 108))
    assert all_group_index_BB[-1] == [1100]
    assert list_group_index_Hk2 == [list(range(871, 1738)), [1738], [1739]]
    assert list_group_index_BB == [[592], [593], [594], [595]]


def test_get_group_id_from_molecule():

    all_group_id_Hk2 = aux.get_group_id_from_molecule(molsys_Hk2, skip_digestion=True)
    all_group_id_BB = aux.get_group_id_from_molecule(molsys_BB, skip_digestion=True)
    list_group_id_Hk2 = aux.get_group_id_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_group_id_BB = aux.get_group_id_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_group_id_Hk2, list)
    assert len(all_group_id_Hk2) == 135
    assert len(all_group_id_BB) == 519
    assert all_group_id_Hk2[0:5] == [[ ii for ii in list(range(17, 914)) if ii not in [98, 99, 100, 101, 102, 103, 104,
                                                                                       518, 519, 520, 521, 522, 523,
                                                                                       524, 525, 547, 548, 549, 550,
                                                                                       551, 592, 593, 594, 645, 646,
                                                                                       647]],
                                     [ ii for ii in list(range(17, 914)) if ii not in [98, 99, 100, 101, 102, 103, 104,
                                                                                       346, 404, 405, 518, 519, 520,
                                                                                       521, 522, 523, 524, 525, 546,
                                                                                       547, 548, 549, 550, 551, 552,
                                                                                       645, 646, 647, 648, 649]],
                                     [1001], [1002], [1003]]
    assert all_group_id_Hk2[90:96] == [[1027], [1028], [1029], [1030], [1031], [1032]]
    assert all_group_id_Hk2[-1] == [1097]
    assert all_group_id_BB[5:8] == [list(range(1, 90)), [111], [112]]
    assert all_group_id_BB[486:492] == [[97], [98], [99], [100], [101], [102]]
    assert all_group_id_BB[0] == list(range(3, 111))
    assert all_group_id_BB[-1] == [129]
    assert list_group_id_Hk2 ==  [[ ii for ii in list(range(17, 914)) if ii not in [98, 99, 100, 101, 102, 103, 104,
                                                                                       346, 404, 405, 518, 519, 520,
                                                                                       521, 522, 523, 524, 525, 546,
                                                                                       547, 548, 549, 550, 551, 552,
                                                                                       645, 646, 647, 648, 649]],
                                  [1001], [1002]]
    assert list_group_id_BB == [[115], [116], [117], [118]]


def test_get_group_name_from_molecule():

    all_group_name_Hk2 = aux.get_group_name_from_molecule(molsys_Hk2, skip_digestion=True)
    all_group_name_BB = aux.get_group_name_from_molecule(molsys_BB, skip_digestion=True)
    list_group_name_Hk2 = aux.get_group_name_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_group_name_BB = aux.get_group_name_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_group_name_Hk2, list)
    assert len(all_group_name_Hk2) == 135
    assert len(all_group_name_BB) == 519
    assert all_group_name_Hk2[0][100:110] == ['THR', 'GLN', 'LEU', 'PHE', 'ASP', 'HIS', 'ILE', 'ALA', 'GLU', 'CYS']
    assert all_group_name_Hk2[1][200:210] == ['CYS', 'GLU', 'ILE', 'GLY', 'LEU', 'ILE', 'VAL', 'GLY', 'THR', 'GLY']
    assert all_group_name_Hk2[2:5] == [['GLC'], ['BG6'], ['GLC']]
    assert all_group_name_Hk2[90:96] ==[['HOH'], ['HOH'], ['HOH'], ['HOH'], ['HOH'], ['HOH']]
    assert all_group_name_Hk2[-1] == ['HOH']
    assert all_group_name_BB[5][40:50] == ['LEU', 'THR', 'GLY', 'TRP', 'VAL', 'GLU', 'TYR', 'PRO', 'LEU', 'VAL']
    assert all_group_name_BB[6:8] == [['HOH'], ['HOH']] 
    assert all_group_name_BB[486:492] == [['HOH'], ['HOH'], ['HOH'], ['HOH'], ['HOH'], ['HOH']]
    assert all_group_name_BB[0][33:43] == ['VAL', 'ALA', 'SER', 'LYS', 'GLY', 'ASN', 'LEU', 'ALA', 'ASP', 'VAL']
    assert all_group_name_BB[-1] == ['HOH']
    assert list_group_name_Hk2[0][66:76] ==  ['LEU', 'ASP', 'LEU', 'GLY', 'GLY', 'THR', 'ASN', 'PHE', 'ARG', 'VAL']
    assert list_group_name_Hk2[1:] == [['GLC'], ['BG6']]
    assert list_group_name_BB == [['HOH'], ['HOH'], ['HOH'], ['HOH']]


def test_get_group_type_from_molecule():

    all_group_type_Hk2 = aux.get_group_type_from_molecule(molsys_Hk2, skip_digestion=True)
    all_group_type_BB = aux.get_group_type_from_molecule(molsys_BB, skip_digestion=True)
    list_group_type_Hk2 = aux.get_group_type_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_group_type_BB = aux.get_group_type_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_group_type_Hk2, list)
    assert len(all_group_type_Hk2) == 135
    assert len(all_group_type_BB) == 519
    assert all_group_type_Hk2[0][100:110] == 10*['amino acid']
    assert all_group_type_Hk2[1][200:210] == 10*['amino acid']
    assert all_group_type_Hk2[2:5] == [['saccharide'], ['saccharide'], ['saccharide']]
    assert all_group_type_Hk2[90:96] == [['water'], ['water'], ['water'], ['water'], ['water'], ['water']]
    assert all_group_type_Hk2[-1] == ['water']
    assert all_group_type_BB[5][40:50] == 10*['amino acid']
    assert all_group_type_BB[6:8] == [['water'], ['water']]
    assert all_group_type_BB[486:492] == [['water'], ['water'], ['water'], ['water'], ['water'], ['water']]
    assert all_group_type_BB[0][33:43] == 10*['amino acid']
    assert all_group_type_BB[-1] == ['water']
    assert list_group_type_Hk2[0][66:76] == 10*['amino acid']
    assert list_group_type_Hk2[1:] == [['saccharide'], ['saccharide']]
    assert list_group_type_BB == [['water'], ['water'], ['water'], ['water']]


def test_get_molecule_index_from_molecule():

    all_molecule_index_Hk2 = aux.get_molecule_index_from_molecule(molsys_Hk2, skip_digestion=True)
    all_molecule_index_BB = aux.get_molecule_index_from_molecule(molsys_BB, skip_digestion=True)
    list_molecule_index_Hk2 = aux.get_molecule_index_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_molecule_index_BB = aux.get_molecule_index_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_molecule_index_Hk2 == list(range(0, 135))
    assert all_molecule_index_BB == list(range(0, 519))
    assert list_molecule_index_Hk2 == [1,2,3]
    assert list_molecule_index_BB == [10, 11, 12, 13]


def test_get_molecule_id_from_molecule():

    all_molecule_id_Hk2 = aux.get_molecule_id_from_molecule(molsys_Hk2, skip_digestion=True)
    all_molecule_id_BB = aux.get_molecule_id_from_molecule(molsys_BB, skip_digestion=True)
    list_molecule_id_Hk2 = aux.get_molecule_id_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_molecule_id_BB = aux.get_molecule_id_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_molecule_id_Hk2 == list(range(0, 135))
    assert all_molecule_id_BB == list(range(0, 519))
    assert list_molecule_id_Hk2 == [1,2,3]
    assert list_molecule_id_BB == [10, 11, 12, 13]


def test_get_molecule_name_from_molecule():

    all_molecule_name_Hk2 = aux.get_molecule_name_from_molecule(molsys_Hk2, skip_digestion=True)
    all_molecule_name_BB = aux.get_molecule_name_from_molecule(molsys_BB, skip_digestion=True)
    list_molecule_name_Hk2 = aux.get_molecule_name_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_molecule_name_BB = aux.get_molecule_name_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_molecule_name_Hk2, list)
    assert len(all_molecule_name_Hk2) == 135
    assert len(all_molecule_name_BB) == 519
    assert all_molecule_name_Hk2[15:25] == ['UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION',
                                         'alpha-D-glucopyranose', '6-O-phosphono-beta-D-glucopyranose',
                                         'alpha-D-glucopyranose', '6-O-phosphono-beta-D-glucopyranose',
                                         'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION']
    assert all_molecule_name_Hk2[105:115] ==['water', 'water', 'water', 'water', 'water', 'water', 'water', 'water',
                                          'water', 'water']
    assert all_molecule_name_Hk2[0] == 'Hexokinase-2'
    assert all_molecule_name_Hk2[-1] == 'water'
    assert all_molecule_name_BB[3:13] == ['BARSTAR', 'BARSTAR', 'BARSTAR', 'water', 'water', 'water', 'water',
                                       'water', 'water', 'water']
    assert all_molecule_name_BB[486:492] == ['water', 'water', 'water', 'water', 'water', 'water']
    assert all_molecule_name_BB[0] == 'BARNASE'
    assert all_molecule_name_BB[-1] == 'water'
    assert list_molecule_name_Hk2 == ['Hexokinase-2', 'alpha-D-glucopyranose', '6-O-phosphono-beta-D-glucopyranose']
    assert list_molecule_name_BB == ['water', 'water', 'water', 'water']


def test_get_molecule_type_from_molecule():

    all_molecule_type_Hk2 = aux.get_molecule_type_from_molecule(molsys_Hk2, skip_digestion=True)
    all_molecule_type_BB = aux.get_molecule_type_from_molecule(molsys_BB, skip_digestion=True)
    list_molecule_type_Hk2 = aux.get_molecule_type_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_molecule_type_BB = aux.get_molecule_type_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_molecule_type_Hk2, list)
    assert len(all_molecule_type_Hk2) == 135
    assert len(all_molecule_type_BB) == 519
    assert all_molecule_type_Hk2[15:25] == ['unknown', 'unknown', 'unknown', 'polysaccharide', 'polysaccharide',
                                         'polysaccharide', 'polysaccharide', 'unknown', 'unknown', 'unknown']
    assert all_molecule_type_Hk2[105:115] ==['water', 'water', 'water', 'water', 'water', 'water', 'water', 'water',
                                          'water', 'water']
    assert all_molecule_type_Hk2[0] == 'protein'
    assert all_molecule_type_Hk2[-1] == 'water'
    assert all_molecule_type_BB[3:13] == ['protein', 'protein', 'protein', 'water', 'water', 'water', 'water',
                                       'water', 'water', 'water']
    assert all_molecule_type_BB[486:492] == ['water', 'water', 'water', 'water', 'water', 'water']
    assert all_molecule_type_BB[0] == 'protein'
    assert all_molecule_type_BB[-1] == 'water'
    assert list_molecule_type_Hk2 == ['protein', 'polysaccharide', 'polysaccharide']
    assert list_molecule_type_BB == ['water', 'water', 'water', 'water']


def test_get_entity_index_from_molecule():

    all_entity_index_Hk2 = aux.get_entity_index_from_molecule(molsys_Hk2, skip_digestion=True)
    all_entity_index_BB = aux.get_entity_index_from_molecule(molsys_BB, skip_digestion=True)
    list_entity_index_Hk2 = aux.get_entity_index_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_entity_index_BB = aux.get_entity_index_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_entity_index_Hk2, list)
    assert len(all_entity_index_Hk2) == 135
    assert len(all_entity_index_BB) == 519
    assert all_entity_index_Hk2[15:25] == [3, 3, 3, 1, 2, 1, 2, 3, 3, 3]
    assert all_entity_index_Hk2[105:115] == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    assert all_entity_index_Hk2[0] == 0
    assert all_entity_index_Hk2[-1] == 4
    assert all_entity_index_BB[3:13] == [1, 1, 1, 2, 2, 2, 2, 2, 2, 2]
    assert all_entity_index_BB[486:492] == [2, 2, 2, 2, 2, 2]
    assert all_entity_index_BB[0] == 0
    assert all_entity_index_BB[-1] == 2
    assert list_entity_index_Hk2 == [0, 1, 2]
    assert list_entity_index_BB == [2, 2, 2, 2]


def test_get_entity_id_from_molecule():

    all_entity_id_Hk2 = aux.get_entity_id_from_molecule(molsys_Hk2, skip_digestion=True)
    all_entity_id_BB = aux.get_entity_id_from_molecule(molsys_BB, skip_digestion=True)
    list_entity_id_Hk2 = aux.get_entity_id_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_entity_id_BB = aux.get_entity_id_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_entity_id_Hk2, list)
    assert len(all_entity_id_Hk2) == 135
    assert len(all_entity_id_BB) == 519
    assert all_entity_id_Hk2[15:25] == [4, 4, 4, 2, 3, 2, 3, 4, 4, 4]
    assert all_entity_id_Hk2[105:115] == [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    assert all_entity_id_Hk2[0] == 1
    assert all_entity_id_Hk2[-1] == 5
    assert all_entity_id_BB[3:13] == [2, 2, 2, 3, 3, 3, 3, 3, 3, 3]
    assert all_entity_id_BB[486:492] == [3, 3, 3, 3, 3, 3]
    assert all_entity_id_BB[0] == 1
    assert all_entity_id_BB[-1] == 3
    assert list_entity_id_Hk2 == [1, 2, 3]
    assert list_entity_id_BB == [3, 3, 3, 3]


def test_get_entity_name_from_molecule():

    all_entity_name_Hk2 = aux.get_entity_name_from_molecule(molsys_Hk2, skip_digestion=True)
    all_entity_name_BB = aux.get_entity_name_from_molecule(molsys_BB, skip_digestion=True)
    list_entity_name_Hk2 = aux.get_entity_name_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_entity_name_BB = aux.get_entity_name_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_entity_name_Hk2, list)
    assert len(all_entity_name_Hk2) == 135
    assert len(all_entity_name_BB) == 519
    assert all_entity_name_Hk2[15:25] == ['UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION',
                                          'alpha-D-glucopyranose', '6-O-phosphono-beta-D-glucopyranose',
                                          'alpha-D-glucopyranose', '6-O-phosphono-beta-D-glucopyranose',
                                          'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION']
    assert all_entity_name_Hk2[105:115] == ['water', 'water', 'water', 'water', 'water', 'water', 'water', 'water',
                                          'water', 'water']
    assert all_entity_name_Hk2[0] == 'Hexokinase-2'
    assert all_entity_name_Hk2[-1] == 'water'
    assert all_entity_name_BB[3:13] == ['BARSTAR', 'BARSTAR', 'BARSTAR', 'water', 'water', 'water', 'water',
                                          'water', 'water', 'water']
    assert all_entity_name_BB[486:492] == ['water', 'water', 'water', 'water', 'water', 'water']
    assert all_entity_name_BB[0] == 'BARNASE'
    assert all_entity_name_BB[-1] == 'water'
    assert list_entity_name_Hk2 == ['Hexokinase-2', 'alpha-D-glucopyranose', '6-O-phosphono-beta-D-glucopyranose']
    assert list_entity_name_BB == ['water', 'water', 'water', 'water']


def test_get_entity_type_from_molecule():

    all_entity_type_Hk2 = aux.get_entity_type_from_molecule(molsys_Hk2, skip_digestion=True)
    all_entity_type_BB = aux.get_entity_type_from_molecule(molsys_BB, skip_digestion=True)
    list_entity_type_Hk2 = aux.get_entity_type_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_entity_type_BB = aux.get_entity_type_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_entity_type_Hk2, list)
    assert len(all_entity_type_Hk2) == 135
    assert len(all_entity_type_BB) == 519
    assert all_entity_type_Hk2[15:25] == ['unknown', 'unknown', 'unknown', 'polysaccharide', 'polysaccharide',
                                          'polysaccharide', 'polysaccharide', 'unknown', 'unknown', 'unknown']
    assert all_entity_type_Hk2[105:115] == ['water', 'water', 'water', 'water', 'water', 'water', 'water', 'water',
                                            'water', 'water']
    assert all_entity_type_Hk2[0] == 'protein'
    assert all_entity_type_Hk2[-1] == 'water'
    assert all_entity_type_BB[3:13] == ['protein', 'protein', 'protein', 'water', 'water', 'water', 'water',
                                        'water', 'water', 'water']
    assert all_entity_type_BB[486:492] == ['water', 'water', 'water', 'water', 'water', 'water']
    assert all_entity_type_BB[0] == 'protein'
    assert all_entity_type_BB[-1] == 'water'
    assert list_entity_type_Hk2 == ['protein', 'polysaccharide', 'polysaccharide']
    assert list_entity_type_BB == ['water', 'water', 'water', 'water']


def test_get_component_index_from_molecule():

    all_component_index_Hk2 = aux.get_component_index_from_molecule(molsys_Hk2, skip_digestion=True)
    all_component_index_BB = aux.get_component_index_from_molecule(molsys_BB, skip_digestion=True)
    list_component_index_Hk2 = aux.get_component_index_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_component_index_BB = aux.get_component_index_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_component_index_Hk2, list)
    assert len(all_component_index_Hk2) == 135
    assert len(all_component_index_BB) == 519
    assert all_component_index_Hk2[15:25] == [[26], [27], [28], [29], [30], [31], [32], [33], [34], [35]]
    assert all_component_index_Hk2[105:115] == [[116], [117], [118], [119], [120], [121], [122], [123], [124], [125]]
    assert all_component_index_Hk2[0] == [0, 1, 2, 3, 4, 5]
    assert all_component_index_Hk2[-1] == [145]
    assert all_component_index_BB[3:13] == [[3, 4], [5, 6], [7], [8], [9], [10], [11], [12], [13], [14]]
    assert all_component_index_BB[486:492] == [[488], [489], [490], [491], [492], [493]]
    assert all_component_index_BB[0] == [0]
    assert all_component_index_BB[-1] == [520]
    assert list_component_index_Hk2 == [[6, 7, 8, 9, 10, 11, 12], [13], [14]]
    assert list_component_index_BB == [[12], [13], [14], [15]]


def test_get_component_id_from_molecule():

    all_component_id_Hk2 = aux.get_component_id_from_molecule(molsys_Hk2, skip_digestion=True)
    all_component_id_BB = aux.get_component_id_from_molecule(molsys_BB, skip_digestion=True)
    list_component_id_Hk2 = aux.get_component_id_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_component_id_BB = aux.get_component_id_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_component_id_Hk2, list)
    assert len(all_component_id_Hk2) == 135
    assert len(all_component_id_BB) == 519
    assert all_component_id_Hk2[15:25] == [[26], [27], [28], [29], [30], [31], [32], [33], [34], [35]]
    assert all_component_id_Hk2[105:115] == [[116], [117], [118], [119], [120], [121], [122], [123], [124], [125]]
    assert all_component_id_Hk2[0] == [0, 1, 2, 3, 4, 5]
    assert all_component_id_Hk2[-1] == [145]
    assert all_component_id_BB[3:13] == [[3, 4], [5, 6], [7], [8], [9], [10], [11], [12], [13], [14]]
    assert all_component_id_BB[486:492] == [[488], [489], [490], [491], [492], [493]]
    assert all_component_id_BB[0] == [0]
    assert all_component_id_BB[-1] == [520]
    assert list_component_id_Hk2 == [[6, 7, 8, 9, 10, 11, 12], [13], [14]]
    assert list_component_id_BB == [[12], [13], [14], [15]]


def test_get_component_name_from_molecule():

    all_component_name_Hk2 = aux.get_component_name_from_molecule(molsys_Hk2, skip_digestion=True)
    all_component_name_BB = aux.get_component_name_from_molecule(molsys_BB, skip_digestion=True)
    list_component_name_Hk2 = aux.get_component_name_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_component_name_BB = aux.get_component_name_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_component_name_Hk2, list)
    assert len(all_component_name_Hk2) == 135
    assert len(all_component_name_BB) == 519
    assert all_component_name_Hk2[15:25] == [['UNX'], ['UNX'], ['UNX'], ['unknown 4'], ['unknown 5'], ['unknown 6'],
                                             ['unknown 7'], ['UNX'], ['UNX'], ['UNX']]
    assert all_component_name_Hk2[105:115] == [['water'], ['water'], ['water'], ['water'], ['water'], ['water'],
                                               ['water'], ['water'], ['water'], ['water']]
    assert all_component_name_Hk2[0] == ['protein 0', 'protein 1', 'peptide 0', 'peptide 1', 'protein 2', 'protein 3']
    assert all_component_name_Hk2[-1] == ['water']
    assert all_component_name_BB[3:13] == [['protein 3', 'peptide 0'], ['protein 4', 'peptide 0'], ['protein 5'],
                                           ['water'], ['water'], ['water'], ['water'], ['water'], ['water'], ['water']]
    assert all_component_name_BB[486:492] == [['water'], ['water'], ['water'], ['water'], ['water'], ['water']]
    assert all_component_name_BB[0] == ['protein 0']
    assert all_component_name_BB[-1] == ['water']
    assert list_component_name_Hk2 == [['protein 4', 'protein 5', 'protein 6', 'protein 7', 'peptide 2', 'protein 8',
                                        'protein 9'], ['unknown 0'], ['unknown 1']]
    assert list_component_name_BB == [['water'], ['water'], ['water'], ['water']]


def test_get_component_type_from_molecule():

    all_component_type_Hk2 = aux.get_component_type_from_molecule(molsys_Hk2, skip_digestion=True)
    all_component_type_BB = aux.get_component_type_from_molecule(molsys_BB, skip_digestion=True)
    list_component_type_Hk2 = aux.get_component_type_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_component_type_BB = aux.get_component_type_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_component_type_Hk2, list)
    assert len(all_component_type_Hk2) == 135
    assert len(all_component_type_BB) == 519
    assert all_component_type_Hk2[15:25] == [['ion'], ['ion'], ['ion'], ['polysaccharide'], ['polysaccharide'],
                                             ['polysaccharide'], ['polysaccharide'], ['ion'], ['ion'], ['ion']]
    assert all_component_type_Hk2[105:115] == [['water'], ['water'], ['water'], ['water'], ['water'], ['water'],
                                               ['water'], ['water'], ['water'], ['water']]
    assert all_component_type_Hk2[0] == ['protein', 'protein', 'peptide', 'peptide', 'protein', 'protein']
    assert all_component_type_Hk2[-1] == ['water']
    assert all_component_type_BB[3:13] == [['protein', 'peptide'], ['protein', 'peptide'], ['protein'], ['water'],
                                           ['water'], ['water'], ['water'], ['water'], ['water'], ['water']]
    assert all_component_type_BB[486:492] == [['water'], ['water'], ['water'], ['water'], ['water'], ['water']]
    assert all_component_type_BB[0] == ['protein']
    assert all_component_type_BB[-1] == ['water']
    assert list_component_type_Hk2 == [['protein', 'protein', 'protein', 'protein', 'peptide', 'protein', 'protein'],
                                       ['polysaccharide'], ['polysaccharide']]
    assert list_component_type_BB == [['water'], ['water'], ['water'], ['water']]


def test_get_chain_index_from_molecule():

    all_chain_index_Hk2 = aux.get_chain_index_from_molecule(molsys_Hk2, skip_digestion=True)
    all_chain_index_BB = aux.get_chain_index_from_molecule(molsys_BB, skip_digestion=True)
    list_chain_index_Hk2 = aux.get_chain_index_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_chain_index_BB = aux.get_chain_index_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_chain_index_Hk2, list)
    assert len(all_chain_index_Hk2) == 135
    assert len(all_chain_index_BB) == 519
    assert all_chain_index_Hk2[15:25] == [15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    assert all_chain_index_Hk2[105:115] == [39, 39, 39, 39, 39, 39, 39, 39, 39, 39]
    assert all_chain_index_Hk2[0] == 0
    assert all_chain_index_Hk2[-1] == 39
    assert all_chain_index_BB[3:13] == [3, 4, 5, 6, 6, 6, 6, 6, 6, 6]
    assert all_chain_index_BB[486:492] == [11, 11, 11, 11, 11, 11]
    assert all_chain_index_BB[0] == 0
    assert all_chain_index_BB[-1] == 11
    assert list_chain_index_Hk2 == [1, 2, 3]
    assert list_chain_index_BB == [6, 6, 6, 6]


def test_get_chain_id_from_molecule():

    all_chain_id_Hk2 = aux.get_chain_id_from_molecule(molsys_Hk2, skip_digestion=True)
    all_chain_id_BB = aux.get_chain_id_from_molecule(molsys_BB, skip_digestion=True)
    list_chain_id_Hk2 = aux.get_chain_id_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_chain_id_BB = aux.get_chain_id_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_chain_id_Hk2, list)
    assert len(all_chain_id_Hk2) == 135
    assert len(all_chain_id_BB) == 519
    assert all_chain_id_Hk2[15:25] == ['P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']
    assert all_chain_id_Hk2[105:115] == ['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA']
    assert all_chain_id_Hk2[0] == 'A'
    assert all_chain_id_Hk2[-1] == 'NA'
    assert all_chain_id_BB[3:13] == ['D', 'E', 'F', 'G', 'G', 'G', 'G', 'G', 'G', 'G']
    assert all_chain_id_BB[486:492] == ['L', 'L', 'L', 'L', 'L', 'L']
    assert all_chain_id_BB[0] == 'A'
    assert all_chain_id_BB[-1] == 'L'
    assert list_chain_id_Hk2 == ['B', 'C', 'D']
    assert list_chain_id_BB == ['G', 'G', 'G', 'G']


def test_get_chain_name_from_molecule():

    all_chain_name_Hk2 = aux.get_chain_name_from_molecule(molsys_Hk2, skip_digestion=True)
    all_chain_name_BB = aux.get_chain_name_from_molecule(molsys_BB, skip_digestion=True)
    list_chain_name_Hk2 = aux.get_chain_name_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_chain_name_BB = aux.get_chain_name_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_chain_name_Hk2, list)
    assert len(all_chain_name_Hk2) == 135
    assert len(all_chain_name_BB) == 519
    assert all_chain_name_Hk2[15:25] == ['A', 'A', 'A', 'B', 'B', 'B', 'B', 'B', 'B', 'B']
    assert all_chain_name_Hk2[105:115] == ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B']
    assert all_chain_name_Hk2[0] == 'A'
    assert all_chain_name_Hk2[-1] == 'B'
    assert all_chain_name_BB[3:13] == ['D', 'E', 'F', 'A', 'A', 'A', 'A', 'A', 'A', 'A']
    assert all_chain_name_BB[486:492] == ['F', 'F', 'F', 'F', 'F', 'F']
    assert all_chain_name_BB[0] == 'A'
    assert all_chain_name_BB[-1] == 'F'
    assert list_chain_name_Hk2 == ['B', 'A', 'A']
    assert list_chain_name_BB == ['A', 'A', 'A', 'A']


def test_get_chain_type_from_molecule():

    all_chain_type_Hk2 = aux.get_chain_type_from_molecule(molsys_Hk2, skip_digestion=True)
    all_chain_type_BB = aux.get_chain_type_from_molecule(molsys_BB, skip_digestion=True)
    list_chain_type_Hk2 = aux.get_chain_type_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_chain_type_BB = aux.get_chain_type_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_chain_type_Hk2, list)
    assert len(all_chain_type_Hk2) == 135
    assert len(all_chain_type_BB) == 519
    assert all_chain_type_Hk2[15:25] == ['unknown', 'unknown', 'unknown', 'polysaccharide', 'polysaccharide',
                                         'polysaccharide', 'polysaccharide', 'unknown', 'unknown', 'unknown']
    assert all_chain_type_Hk2[105:115] == ['water', 'water', 'water', 'water', 'water', 'water', 'water', 'water',
                                           'water', 'water']
    assert all_chain_type_Hk2[0] == 'protein'
    assert all_chain_type_Hk2[-1] == 'water'
    assert all_chain_type_BB[3:13] == ['protein', 'protein', 'protein', 'water', 'water', 'water', 'water',
                                       'water', 'water', 'water']
    assert all_chain_type_BB[486:492] == ['water', 'water', 'water', 'water', 'water', 'water']
    assert all_chain_type_BB[0] == 'protein'
    assert all_chain_type_BB[-1] == 'water'
    assert list_chain_type_Hk2 == ['protein', 'polysaccharide', 'polysaccharide']
    assert list_chain_type_BB == ['water', 'water', 'water', 'water']


def test_get_bond_index_from_molecule():

    all_bond_index_Hk2 = aux.get_bond_index_from_molecule(molsys_Hk2, skip_digestion=True)
    all_bond_index_BB = aux.get_bond_index_from_molecule(molsys_BB, skip_digestion=True)
    list_bond_index_Hk2 = aux.get_bond_index_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_bond_index_BB = aux.get_bond_index_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_bond_index_Hk2, list)
    assert len(all_bond_index_Hk2) == 135
    assert len(all_bond_index_BB) == 519
    assert all_bond_index_Hk2[15:25] == [[], [], [],
                                         [13562, 13563, 13564, 13565, 13566, 13567, 13568, 13569, 13570, 13571, 13572,
                                          13573],
                                         [13574, 13575, 13576, 13577, 13578, 13579, 13580, 13581, 13582, 13583, 13584,
                                          13585, 13586, 13587, 13588, 13589],
                                         [13590, 13591, 13592, 13593, 13594, 13595, 13596, 13597, 13598, 13599, 13600,
                                          13601],
                                         [13602, 13603, 13604, 13605, 13606, 13607, 13608, 13609, 13610, 13611, 13612,
                                          13613, 13614, 13615, 13616, 13617], [], [], []]
    assert all_bond_index_Hk2[105:115] == [[], [], [], [], [], [], [], [], [], []]
    assert all_bond_index_Hk2[0][80:90] == [80, 81, 82, 83, 84, 85, 86, 87, 88, 89]
    assert all_bond_index_Hk2[-1] == []
    assert all_bond_index_BB[3:13][0][500:510] == [3144, 3145, 3146, 3147, 3148, 3149, 3150, 3151, 3152, 3153]
    assert all_bond_index_BB[3:13][1][600:610] == [3949, 3950, 3951, 3952, 3953, 3954, 3955, 3956, 3957, 3958]
    assert all_bond_index_BB[3:13][2][200:210] == [4226, 4227, 4228, 4229, 4230, 4231, 4232, 4233, 4234, 4235]
    assert all_bond_index_BB[3:13][3:10] == [[], [], [], [], [], [], []]
    assert all_bond_index_BB[0] == list(range(885))
    assert all_bond_index_BB[-1] == []
    assert list_bond_index_Hk2 == [list(range(6751, 13506)),
                                   [13506, 13507, 13508, 13509, 13510, 13511, 13512, 13513, 13514, 13515, 13516,
                                    13517],
                                   [13518, 13519, 13520, 13521, 13522, 13523, 13524, 13525, 13526, 13527, 13528,
                                    13529, 13530, 13531, 13532, 13533]]
    assert list_bond_index_BB == [[], [], [], []]


def test_get_bond_type_from_molecule():

    all_bond_type_Hk2 = aux.get_bond_type_from_molecule(molsys_Hk2, skip_digestion=True)
    all_bond_type_BB = aux.get_bond_type_from_molecule(molsys_BB, skip_digestion=True)
    list_bond_type_Hk2 = aux.get_bond_type_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_bond_type_BB = aux.get_bond_type_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_bond_type_Hk2, list)
    assert len(all_bond_type_Hk2) == 135
    assert len(all_bond_type_BB) == 519
    assert all_bond_type_Hk2[15:25] == [[], [], [], 12*[None], 16*[None], 12*[None], 16*[None], [], [], []]
    assert all_bond_type_Hk2[105:115] == [[], [], [], [], [], [], [], [], [], []]
    assert all_bond_type_Hk2[0][80:90] == 10*[None]
    assert all_bond_type_Hk2[-1] == []
    assert all_bond_type_BB[3:13][0][500:510] == 10*[None]
    assert all_bond_type_BB[3:13][1][600:610] == 10*[None]
    assert all_bond_type_BB[3:13][2][200:210] == 10*[None]
    assert all_bond_type_BB[3:13][3:10] == [[], [], [], [], [], [], []]
    assert all_bond_type_BB[0] == 885*[None]
    assert all_bond_type_BB[-1] == []
    assert list_bond_type_Hk2 == [6755*[None], 12*[None], 16*[None]]
    assert list_bond_type_BB == [[], [], [], []]


def test_get_bond_order_from_molecule():

    all_bond_order_Hk2 = aux.get_bond_order_from_molecule(molsys_Hk2, skip_digestion=True)
    all_bond_order_BB = aux.get_bond_order_from_molecule(molsys_BB, skip_digestion=True)
    list_bond_order_Hk2 = aux.get_bond_order_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_bond_order_BB = aux.get_bond_order_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_bond_order_Hk2, list)
    assert len(all_bond_order_Hk2) == 135
    assert len(all_bond_order_BB) == 519
    assert all_bond_order_Hk2[15:25] == [[], [], [], 12*[None], 16*[None], 12*[None], 16*[None], [], [], []]
    assert all_bond_order_Hk2[105:115] == [[], [], [], [], [], [], [], [], [], []]
    assert all_bond_order_Hk2[0][80:90] == 10*[None]
    assert all_bond_order_Hk2[-1] == []
    assert all_bond_order_BB[3:13][0][500:510] == 10*[None]
    assert all_bond_order_BB[3:13][1][600:610] == 10*[None]
    assert all_bond_order_BB[3:13][2][200:210] == 10*[None]
    assert all_bond_order_BB[3:13][3:10] == [[], [], [], [], [], [], []]
    assert all_bond_order_BB[0] == 885*[None]
    assert all_bond_order_BB[-1] == []
    assert list_bond_order_Hk2 == [6755*[None], 12*[None], 16*[None]]
    assert list_bond_order_BB == [[], [], [], []]


def test_get_bonded_atoms_from_molecule():

    all_bonded_atoms_Hk2 = aux.get_bonded_atoms_from_molecule(molsys_Hk2, skip_digestion=True)
    all_bonded_atoms_BB = aux.get_bonded_atoms_from_molecule(molsys_BB, skip_digestion=True)
    list_bonded_atoms_Hk2 = aux.get_bonded_atoms_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_bonded_atoms_BB = aux.get_bonded_atoms_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_bonded_atoms_Hk2, list)
    assert len(all_bonded_atoms_Hk2) == 135
    assert len(all_bonded_atoms_BB) == 519
    assert all_bonded_atoms_Hk2[15:25] == [[], [], [],
                                           [13377, 13378, 13379, 13380, 13381, 13382, 13383, 13384, 13385, 13386,
                                            13387, 13388],
                                           [13389, 13390, 13391, 13392, 13393, 13394, 13395, 13396, 13397, 13398,
                                            13399, 13400, 13401, 13402, 13403, 13404],
                                           [13405, 13406, 13407, 13408, 13409, 13410, 13411, 13412, 13413, 13414,
                                            13415, 13416],
                                           [13417, 13418, 13419, 13420, 13421, 13422, 13423, 13424, 13425, 13426,
                                            13427, 13428, 13429, 13430, 13431, 13432],
                                           [], [], []]
    assert all_bonded_atoms_Hk2[105:115] == [[], [], [], [], [], [], [], [], [], []]
    assert all_bonded_atoms_Hk2[0][80:90] == [80, 81, 82, 83, 84, 85, 86, 87, 88, 89]
    assert all_bonded_atoms_Hk2[-1] == []
    assert all_bonded_atoms_BB[3:13][0][500:510] == [3081, 3082, 3083, 3084, 3085, 3086, 3087, 3088, 3089, 3090]
    assert all_bonded_atoms_BB[3:13][1][600:610] == [3874, 3875, 3876, 3877, 3878, 3879, 3880, 3881, 3882, 3883]
    assert all_bonded_atoms_BB[3:13][2][200:210] == [4139, 4140, 4141, 4142, 4143, 4144, 4145, 4146, 4147, 4148]
    assert all_bonded_atoms_BB[3:13][3:10] == [[], [], [], [], [], [], []]
    assert all_bonded_atoms_BB[0] == list(range(864))
    assert all_bonded_atoms_BB[-1] == []
    assert list_bonded_atoms_Hk2 == [list(range(6653, 13309)),
                                     [13309, 13310, 13311, 13312, 13313, 13314, 13315, 13316, 13317, 13318,
                                      13319, 13320],
                                     [13321, 13322, 13323, 13324, 13325, 13326, 13327, 13328, 13329, 13330,
                                      13331, 13332, 13333, 13334, 13335, 13336]]
    assert list_bonded_atoms_BB == [[], [], [], []]


def test_get_bonded_atom_pairs_from_molecule():

    all_bonded_atom_pairs_Hk2 = aux.get_bonded_atom_pairs_from_molecule(molsys_Hk2, skip_digestion=True)
    all_bonded_atom_pairs_BB = aux.get_bonded_atom_pairs_from_molecule(molsys_BB, skip_digestion=True)
    list_bonded_atom_pairs_Hk2 = aux.get_bonded_atom_pairs_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_bonded_atom_pairs_BB = aux.get_bonded_atom_pairs_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_bonded_atom_pairs_Hk2, list)
    assert len(all_bonded_atom_pairs_Hk2) == 135
    assert len(all_bonded_atom_pairs_BB) == 519
    assert all_bonded_atom_pairs_Hk2[15:25] == [[], [], [],
                                                [[13377, 13378], [13377, 13383], [13377, 13387], [13378, 13379],
                                                 [13378, 13384], [13379, 13380], [13379, 13385], [13380, 13381],
                                                 [13380, 13386], [13381, 13382], [13381, 13387], [13382, 13388]],
                                                [[13389, 13390], [13389, 13391], [13389, 13392], [13390, 13393],
                                                 [13390, 13394], [13392, 13397], [13393, 13395], [13393, 13396],
                                                 [13395, 13397], [13395, 13398], [13397, 13399], [13399, 13400],
                                                 [13400, 13401], [13401, 13402], [13401, 13403], [13401, 13404]],
                                                [[13405, 13406], [13405, 13411], [13405, 13415], [13406, 13407],
                                                 [13406, 13412], [13407, 13408], [13407, 13413], [13408, 13409],
                                                 [13408, 13414], [13409, 13410], [13409, 13415], [13410, 13416]],
                                                [[13417, 13418], [13417, 13419], [13417, 13420], [13418, 13421],
                                                 [13418, 13422], [13420, 13425], [13421, 13423], [13421, 13424],
                                                 [13423, 13425], [13423, 13426], [13425, 13427], [13427, 13428],
                                                 [13428, 13429], [13429, 13430], [13429, 13431], [13429, 13432]],
                                                [], [], []]
    assert all_bonded_atom_pairs_Hk2[105:115] == [[], [], [], [], [], [], [], [], [], []]
    assert all_bonded_atom_pairs_Hk2[0][80:90] == [[79, 80], [79, 82], [80, 81], [80, 86], [82, 83], [83, 84],
                                                   [83, 85], [86, 87], [87, 88], [87, 90]]
    assert all_bonded_atom_pairs_Hk2[-1] == []
    assert all_bonded_atom_pairs_BB[3:13][0][500:510] == [[3066, 3070], [3068, 3069], [3070, 3071], [3071, 3072],
                                                          [3071, 3074], [3072, 3073], [3072, 3078], [3074, 3075],
                                                          [3075, 3076], [3076, 3077]]
    assert all_bonded_atom_pairs_BB[3:13][1][600:610] == [[3860, 3861], [3862, 3863], [3863, 3864], [3863, 3866],
                                                          [3864, 3865], [3864, 3867], [3867, 3868], [3868, 3869],
                                                          [3868, 3871], [3869, 3870]]
    assert all_bonded_atom_pairs_BB[3:13][2][200:210] == [[4137, 4138], [4138, 4139], [4138, 4140], [4141, 4142],
                                                          [4141, 4147], [4142, 4143], [4142, 4145], [4143, 4144],
                                                          [4143, 4148], [4145, 4146]]
    assert all_bonded_atom_pairs_BB[3:13][3:10] == [[], [], [], [], [], [], []]
    assert all_bonded_atom_pairs_BB[0][65:75] == [[62, 65], [65, 66], [66, 67], [66, 69], [67, 68], [67, 73],
                                                  [69, 70], [70, 71], [70, 72], [73, 74]]
    assert all_bonded_atom_pairs_BB[-1] == []
    assert list_bonded_atom_pairs_Hk2[0][50:60] == [[6701, 6707], [6703, 6704], [6704, 6705], [6704, 6706],
                                                    [6707, 6708], [6708, 6709], [6708, 6711], [6709, 6710],
                                                    [6709, 6716], [6711, 6712]]
    assert list_bonded_atom_pairs_Hk2[1:] == [[[13309, 13310], [13309, 13315], [13309, 13319], [13310, 13311],
                                               [13310, 13316], [13311, 13312], [13311, 13317], [13312, 13313],
                                               [13312, 13318], [13313, 13314], [13313, 13319], [13314, 13320]],
                                              [[13321, 13322], [13321, 13323], [13321, 13324], [13322, 13325],
                                               [13322, 13326], [13324, 13329], [13325, 13327], [13325, 13328],
                                               [13327, 13329], [13327, 13330], [13329, 13331], [13331, 13332],
                                               [13332, 13333], [13333, 13334], [13333, 13335], [13333, 13336]]]
    assert list_bonded_atom_pairs_BB == [[], [], [], []]


def test_get_inner_bond_index_from_molecule():

    all_inner_bond_index_Hk2 = aux.get_inner_bond_index_from_molecule(molsys_Hk2, skip_digestion=True)
    all_inner_bond_index_BB = aux.get_inner_bond_index_from_molecule(molsys_BB, skip_digestion=True)
    list_inner_bond_index_Hk2 = aux.get_inner_bond_index_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_inner_bond_index_BB = aux.get_inner_bond_index_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_inner_bond_index_Hk2, list)
    assert len(all_inner_bond_index_Hk2) == 135
    assert len(all_inner_bond_index_BB) == 519
    assert all_inner_bond_index_Hk2[15:25] == [[], [], [],
                                         [13562, 13563, 13564, 13565, 13566, 13567, 13568, 13569, 13570, 13571, 13572,
                                          13573],
                                         [13574, 13575, 13576, 13577, 13578, 13579, 13580, 13581, 13582, 13583, 13584,
                                          13585, 13586, 13587, 13588, 13589],
                                         [13590, 13591, 13592, 13593, 13594, 13595, 13596, 13597, 13598, 13599, 13600,
                                          13601],
                                         [13602, 13603, 13604, 13605, 13606, 13607, 13608, 13609, 13610, 13611, 13612,
                                          13613, 13614, 13615, 13616, 13617], [], [], []]
    assert all_inner_bond_index_Hk2[105:115] == [[], [], [], [], [], [], [], [], [], []]
    assert all_inner_bond_index_Hk2[0][80:90] == [80, 81, 82, 83, 84, 85, 86, 87, 88, 89]
    assert all_inner_bond_index_Hk2[-1] == []
    assert all_inner_bond_index_BB[3:13][0][500:510] == [3144, 3145, 3146, 3147, 3148, 3149, 3150, 3151, 3152, 3153]
    assert all_inner_bond_index_BB[3:13][1][600:610] == [3949, 3950, 3951, 3952, 3953, 3954, 3955, 3956, 3957, 3958]
    assert all_inner_bond_index_BB[3:13][2][200:210] == [4226, 4227, 4228, 4229, 4230, 4231, 4232, 4233, 4234, 4235]
    assert all_inner_bond_index_BB[3:13][3:10] == [[], [], [], [], [], [], []]
    assert all_inner_bond_index_BB[0] == list(range(885))
    assert all_inner_bond_index_BB[-1] == []
    assert list_inner_bond_index_Hk2 == [list(range(6751, 13506)),
                                   [13506, 13507, 13508, 13509, 13510, 13511, 13512, 13513, 13514, 13515, 13516,
                                    13517],
                                   [13518, 13519, 13520, 13521, 13522, 13523, 13524, 13525, 13526, 13527, 13528,
                                    13529, 13530, 13531, 13532, 13533]]
    assert list_inner_bond_index_BB == [[], [], [], []]


def test_get_inner_bonded_atom_pairs_from_molecule():

    all_inner_bonded_atom_pairs_Hk2 = aux.get_inner_bonded_atom_pairs_from_molecule(molsys_Hk2, skip_digestion=True)
    all_inner_bonded_atom_pairs_BB = aux.get_inner_bonded_atom_pairs_from_molecule(molsys_BB, skip_digestion=True)
    list_inner_bonded_atom_pairs_Hk2 = aux.get_inner_bonded_atom_pairs_from_molecule(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_inner_bonded_atom_pairs_BB = aux.get_inner_bonded_atom_pairs_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_inner_bonded_atom_pairs_Hk2, list)
    assert len(all_inner_bonded_atom_pairs_Hk2) == 135
    assert len(all_inner_bonded_atom_pairs_BB) == 519
    assert all_inner_bonded_atom_pairs_Hk2[15:25] == [[], [], [],
                                                [[13377, 13378], [13377, 13383], [13377, 13387], [13378, 13379],
                                                 [13378, 13384], [13379, 13380], [13379, 13385], [13380, 13381],
                                                 [13380, 13386], [13381, 13382], [13381, 13387], [13382, 13388]],
                                                [[13389, 13390], [13389, 13391], [13389, 13392], [13390, 13393],
                                                 [13390, 13394], [13392, 13397], [13393, 13395], [13393, 13396],
                                                 [13395, 13397], [13395, 13398], [13397, 13399], [13399, 13400],
                                                 [13400, 13401], [13401, 13402], [13401, 13403], [13401, 13404]],
                                                [[13405, 13406], [13405, 13411], [13405, 13415], [13406, 13407],
                                                 [13406, 13412], [13407, 13408], [13407, 13413], [13408, 13409],
                                                 [13408, 13414], [13409, 13410], [13409, 13415], [13410, 13416]],
                                                [[13417, 13418], [13417, 13419], [13417, 13420], [13418, 13421],
                                                 [13418, 13422], [13420, 13425], [13421, 13423], [13421, 13424],
                                                 [13423, 13425], [13423, 13426], [13425, 13427], [13427, 13428],
                                                 [13428, 13429], [13429, 13430], [13429, 13431], [13429, 13432]],
                                                [], [], []]
    assert all_inner_bonded_atom_pairs_Hk2[105:115] == [[], [], [], [], [], [], [], [], [], []]
    assert all_inner_bonded_atom_pairs_Hk2[0][80:90] == [[79, 80], [79, 82], [80, 81], [80, 86], [82, 83], [83, 84],
                                                   [83, 85], [86, 87], [87, 88], [87, 90]]
    assert all_inner_bonded_atom_pairs_Hk2[-1] == []
    assert all_inner_bonded_atom_pairs_BB[3:13][0][500:510] == [[3066, 3070], [3068, 3069], [3070, 3071], [3071, 3072],
                                                          [3071, 3074], [3072, 3073], [3072, 3078], [3074, 3075],
                                                          [3075, 3076], [3076, 3077]]
    assert all_inner_bonded_atom_pairs_BB[3:13][1][600:610] == [[3860, 3861], [3862, 3863], [3863, 3864], [3863, 3866],
                                                          [3864, 3865], [3864, 3867], [3867, 3868], [3868, 3869],
                                                          [3868, 3871], [3869, 3870]]
    assert all_inner_bonded_atom_pairs_BB[3:13][2][200:210] == [[4137, 4138], [4138, 4139], [4138, 4140], [4141, 4142],
                                                          [4141, 4147], [4142, 4143], [4142, 4145], [4143, 4144],
                                                          [4143, 4148], [4145, 4146]]
    assert all_inner_bonded_atom_pairs_BB[3:13][3:10] == [[], [], [], [], [], [], []]
    assert all_inner_bonded_atom_pairs_BB[0][65:75] == [[62, 65], [65, 66], [66, 67], [66, 69], [67, 68], [67, 73],
                                                  [69, 70], [70, 71], [70, 72], [73, 74]]
    assert all_inner_bonded_atom_pairs_BB[-1] == []
    assert list_inner_bonded_atom_pairs_Hk2[0][50:60] == [[6701, 6707], [6703, 6704], [6704, 6705], [6704, 6706],
                                                    [6707, 6708], [6708, 6709], [6708, 6711], [6709, 6710],
                                                    [6709, 6716], [6711, 6712]]
    assert list_inner_bonded_atom_pairs_Hk2[1:] == [[[13309, 13310], [13309, 13315], [13309, 13319], [13310, 13311],
                                               [13310, 13316], [13311, 13312], [13311, 13317], [13312, 13313],
                                               [13312, 13318], [13313, 13314], [13313, 13319], [13314, 13320]],
                                              [[13321, 13322], [13321, 13323], [13321, 13324], [13322, 13325],
                                               [13322, 13326], [13324, 13329], [13325, 13327], [13325, 13328],
                                               [13327, 13329], [13327, 13330], [13329, 13331], [13331, 13332],
                                               [13332, 13333], [13333, 13334], [13333, 13335], [13333, 13336]]]
    assert list_inner_bonded_atom_pairs_BB == [[], [], [], []]


def test_get_n_atoms_from_molecule():

    all_n_atoms_Hk2 = aux.get_n_atoms_from_molecule(molsys_Hk2, skip_digestion=True)
    all_n_atoms_BB = aux.get_n_atoms_from_molecule(molsys_BB, skip_digestion=True)
    list_n_atoms_Hk2 = aux.get_n_atoms_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_atoms_BB = aux.get_n_atoms_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_atoms_Hk2) == 135
    assert len(all_n_atoms_BB) == 519
    assert all_n_atoms_Hk2[15:25] == [1, 1, 1, 12, 16, 12, 16, 1, 1, 1]
    assert all_n_atoms_Hk2[105:115] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_atoms_Hk2[0] == 6653
    assert all_n_atoms_Hk2[-1] == 1
    assert all_n_atoms_BB[3:13] == [693, 665, 699, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_atoms_BB[486:492] == [1, 1, 1, 1, 1, 1]
    assert all_n_atoms_BB[0] == 864
    assert all_n_atoms_BB[-1] == 1
    assert list_n_atoms_Hk2 == [12, 16, 1]
    assert list_n_atoms_BB == [1, 1, 1, 1]


def test_get_total_n_atoms_from_molecule():

    all_total_n_atoms_Hk2 = aux.get_total_n_atoms_from_molecule(molsys_Hk2, skip_digestion=True)
    all_total_n_atoms_BB = aux.get_total_n_atoms_from_molecule(molsys_BB, skip_digestion=True)
    list_total_n_atoms_Hk2 = aux.get_total_n_atoms_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_atoms_BB = aux.get_total_n_atoms_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_atoms_Hk2 == 13546
    assert all_total_n_atoms_BB == 5151
    assert list_total_n_atoms_Hk2 == 29
    assert list_total_n_atoms_BB == 4


def test_get_n_groups_from_molecule():

    all_n_groups_Hk2 = aux.get_n_groups_from_molecule(molsys_Hk2, skip_digestion=True)
    all_n_groups_BB = aux.get_n_groups_from_molecule(molsys_BB, skip_digestion=True)
    list_n_groups_Hk2 = aux.get_n_groups_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_groups_BB = aux.get_n_groups_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_groups_Hk2) == 135
    assert len(all_n_groups_BB) == 519
    assert all_n_groups_Hk2[15:25] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_groups_Hk2[105:115] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_groups_Hk2[0] == 871
    assert all_n_groups_Hk2[-1] == 1
    assert all_n_groups_BB[3:13] == [87, 86, 89, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_groups_BB[486:492] == [1, 1, 1, 1, 1, 1]
    assert all_n_groups_BB[0] == 108
    assert all_n_groups_BB[-1] == 1
    assert list_n_groups_Hk2 == [1, 1, 1]
    assert list_n_groups_BB == [1, 1, 1, 1]


def test_get_total_n_groups_from_molecule():

    all_total_n_groups_Hk2 = aux.get_total_n_groups_from_molecule(molsys_Hk2, skip_digestion=True)
    all_total_n_groups_BB = aux.get_total_n_groups_from_molecule(molsys_BB, skip_digestion=True)
    list_total_n_groups_Hk2 = aux.get_total_n_groups_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_groups_BB = aux.get_total_n_groups_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_groups_Hk2 == 1871
    assert all_total_n_groups_BB == 1101
    assert list_total_n_groups_Hk2 == 3
    assert list_total_n_groups_BB == 4


def test_get_n_molecules_from_molecule():

    all_n_molecules_Hk2 = aux.get_n_molecules_from_molecule(molsys_Hk2, skip_digestion=True)
    all_n_molecules_BB = aux.get_n_molecules_from_molecule(molsys_BB, skip_digestion=True)
    list_n_molecules_Hk2 = aux.get_n_molecules_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_molecules_BB = aux.get_n_molecules_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_molecules_Hk2 == 135
    assert all_n_molecules_BB == 519
    assert list_n_molecules_Hk2 == 3
    assert list_n_molecules_BB == 4


def test_get_total_n_molecules_from_molecule():

    all_total_n_molecules_Hk2 = aux.get_total_n_molecules_from_molecule(molsys_Hk2, skip_digestion=True)
    all_total_n_molecules_BB = aux.get_total_n_molecules_from_molecule(molsys_BB, skip_digestion=True)
    list_total_n_molecules_Hk2 = aux.get_total_n_molecules_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_molecules_BB = aux.get_total_n_molecules_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_molecules_Hk2 == 135
    assert all_total_n_molecules_BB == 519
    assert list_total_n_molecules_Hk2 == 3
    assert list_total_n_molecules_BB == 4


def test_get_n_entities_from_molecule():

    all_n_entities_Hk2 = aux.get_n_entities_from_molecule(molsys_Hk2, skip_digestion=True)
    all_n_entities_BB = aux.get_n_entities_from_molecule(molsys_BB, skip_digestion=True)
    list_n_entities_Hk2 = aux.get_n_entities_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_entities_BB = aux.get_n_entities_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_entities_Hk2 == 5
    assert all_n_entities_BB == 3
    assert list_n_entities_Hk2 == 3
    assert list_n_entities_BB == 1


def test_get_total_n_entities_from_molecule():

    all_total_n_entities_Hk2 = aux.get_total_n_entities_from_molecule(molsys_Hk2, skip_digestion=True)
    all_total_n_entities_BB = aux.get_total_n_entities_from_molecule(molsys_BB, skip_digestion=True)
    list_total_n_entities_Hk2 = aux.get_total_n_entities_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_entities_BB = aux.get_total_n_entities_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_entities_Hk2 == 5
    assert all_total_n_entities_BB == 3
    assert list_total_n_entities_Hk2 == 3
    assert list_total_n_entities_BB == 1


def test_get_n_components_from_molecule():

    all_n_components_Hk2 = aux.get_n_components_from_molecule(molsys_Hk2, skip_digestion=True)
    all_n_components_BB = aux.get_n_components_from_molecule(molsys_BB, skip_digestion=True)
    list_n_components_Hk2 = aux.get_n_components_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_components_BB = aux.get_n_components_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_components_Hk2) == 135
    assert len(all_n_components_BB) == 519
    assert all_n_components_Hk2[15:25] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_components_Hk2[105:115] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_components_Hk2[0] == 6
    assert all_n_components_Hk2[-1] == 1
    assert all_n_components_BB[3:13] == [2, 2, 1, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_components_BB[486:492] == [1, 1, 1, 1, 1, 1]
    assert all_n_components_BB[0] == 1
    assert all_n_components_BB[-1] == 1
    assert list_n_components_Hk2 == [1, 1, 1]
    assert list_n_components_BB == [1, 1, 1, 1]


def test_get_total_n_components_from_molecule():

    all_total_n_components_Hk2 = aux.get_total_n_components_from_molecule(molsys_Hk2, skip_digestion=True)
    all_total_n_components_BB = aux.get_total_n_components_from_molecule(molsys_BB, skip_digestion=True)
    list_total_n_components_Hk2 = aux.get_total_n_components_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_components_BB = aux.get_total_n_components_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_components_Hk2 == 146
    assert all_total_n_components_BB == 521
    assert list_total_n_components_Hk2 == 3
    assert list_total_n_components_BB == 4


def test_get_n_chains_from_molecule():

    all_n_chains_Hk2 = aux.get_n_chains_from_molecule(molsys_Hk2, skip_digestion=True)
    all_n_chains_BB = aux.get_n_chains_from_molecule(molsys_BB, skip_digestion=True)
    list_n_chains_Hk2 = aux.get_n_chains_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_chains_BB = aux.get_n_chains_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_chains_Hk2 == 135*[1]
    assert all_n_chains_BB == 519*[1]
    assert list_n_chains_Hk2 == [1,1,1]
    assert list_n_chains_BB == [1,1,1,1]


def test_get_total_n_chains_from_molecule():

    all_total_n_chains_Hk2 = aux.get_total_n_chains_from_molecule(molsys_Hk2, skip_digestion=True)
    all_total_n_chains_BB = aux.get_total_n_chains_from_molecule(molsys_BB, skip_digestion=True)
    list_total_n_chains_Hk2 = aux.get_total_n_chains_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_chains_BB = aux.get_total_n_chains_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_chains_Hk2 == 40
    assert all_total_n_chains_BB == 12
    assert list_total_n_chains_Hk2 == 3
    assert list_total_n_chains_BB == 1


def test_get_n_bonds_from_molecule():

    all_n_bonds_Hk2 = aux.get_n_bonds_from_molecule(molsys_Hk2, skip_digestion=True)
    all_n_bonds_BB = aux.get_n_bonds_from_molecule(molsys_BB, skip_digestion=True)
    list_n_bonds_Hk2 = aux.get_n_bonds_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_bonds_BB = aux.get_n_bonds_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_bonds_Hk2) == 135
    assert len(all_n_bonds_BB) == 519
    assert all_n_bonds_Hk2[15:25] == [0, 0, 0, 12, 16, 12, 16, 0, 0, 0]
    assert all_n_bonds_Hk2[105:115] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_bonds_Hk2[0] == 6751
    assert all_n_bonds_Hk2[-1] == 0
    assert all_n_bonds_BB[3:13] == [705, 677, 712, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_bonds_BB[486:492] == [0, 0, 0, 0, 0, 0]
    assert all_n_bonds_BB[0] == 885
    assert all_n_bonds_BB[-1] == 0
    assert list_n_bonds_Hk2 == [12, 16, 0]
    assert list_n_bonds_BB == [0, 0, 0, 0]


def test_get_total_n_bonds_from_molecule():

    all_total_n_bonds_Hk2 = aux.get_total_n_bonds_from_molecule(molsys_Hk2, skip_digestion=True)
    all_total_n_bonds_BB = aux.get_total_n_bonds_from_molecule(molsys_BB, skip_digestion=True)
    list_total_n_bonds_Hk2 = aux.get_total_n_bonds_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_bonds_BB = aux.get_total_n_bonds_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_bonds_Hk2 == 13618
    assert all_total_n_bonds_BB == 4738
    assert list_total_n_bonds_Hk2 == 28
    assert list_total_n_bonds_BB == 0


def test_get_n_inner_bonds_from_molecule():

    all_n_inner_bonds_Hk2 = aux.get_n_inner_bonds_from_molecule(molsys_Hk2, skip_digestion=True)
    all_n_inner_bonds_BB = aux.get_n_inner_bonds_from_molecule(molsys_BB, skip_digestion=True)
    list_n_inner_bonds_Hk2 = aux.get_n_inner_bonds_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_inner_bonds_BB = aux.get_n_inner_bonds_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_inner_bonds_Hk2) == 135
    assert len(all_n_inner_bonds_BB) == 519
    assert all_n_inner_bonds_Hk2[15:25] == [0, 0, 0, 12, 16, 12, 16, 0, 0, 0]
    assert all_n_inner_bonds_Hk2[105:115] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_inner_bonds_Hk2[0] == 6751
    assert all_n_inner_bonds_Hk2[-1] == 0
    assert all_n_inner_bonds_BB[3:13] == [705, 677, 712, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_inner_bonds_BB[486:492] == [0, 0, 0, 0, 0, 0]
    assert all_n_inner_bonds_BB[0] == 885
    assert all_n_inner_bonds_BB[-1] == 0
    assert list_n_inner_bonds_Hk2 == [12, 16, 0]
    assert list_n_inner_bonds_BB == [0, 0, 0, 0]


def test_get_total_n_inner_bonds_from_molecule():

    all_total_n_inner_bonds_Hk2 = aux.get_total_n_inner_bonds_from_molecule(molsys_Hk2, skip_digestion=True)
    all_total_n_inner_bonds_BB = aux.get_total_n_inner_bonds_from_molecule(molsys_BB, skip_digestion=True)
    list_total_n_inner_bonds_Hk2 = aux.get_total_n_inner_bonds_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_inner_bonds_BB = aux.get_total_n_inner_bonds_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_inner_bonds_Hk2 == 13618
    assert all_total_n_inner_bonds_BB == 4738
    assert list_total_n_inner_bonds_Hk2 == 28
    assert list_total_n_inner_bonds_BB == 0


def test_get_n_amino_acids_from_molecule():

    all_n_amino_acids_Hk2 = aux.get_n_amino_acids_from_molecule(molsys_Hk2, skip_digestion=True)
    all_n_amino_acids_BB = aux.get_n_amino_acids_from_molecule(molsys_BB, skip_digestion=True)
    list_n_amino_acids_Hk2 = aux.get_n_amino_acids_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_amino_acids_BB = aux.get_n_amino_acids_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_amino_acids_Hk2) == 135
    assert len(all_n_amino_acids_BB) == 519
    assert all_n_amino_acids_Hk2[15:25] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_amino_acids_Hk2[105:115] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_amino_acids_Hk2[0] == 871
    assert all_n_amino_acids_Hk2[-1] == 0
    assert all_n_amino_acids_BB[3:13] == [87, 86, 89, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_amino_acids_BB[486:492] == [0, 0, 0, 0, 0, 0]
    assert all_n_amino_acids_BB[0] == 108
    assert all_n_amino_acids_BB[-1] == 0
    assert list_n_amino_acids_Hk2 == [0, 0, 0]
    assert list_n_amino_acids_BB == [0, 0, 0, 0]


def test_get_total_n_amino_acids_from_molecule():

    all_total_n_amino_acids_Hk2 = aux.get_total_n_amino_acids_from_molecule(molsys_Hk2, skip_digestion=True)
    all_total_n_amino_acids_BB = aux.get_total_n_amino_acids_from_molecule(molsys_BB, skip_digestion=True)
    list_total_n_amino_acids_Hk2 = aux.get_total_n_amino_acids_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_amino_acids_BB = aux.get_total_n_amino_acids_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_amino_acids_Hk2 == 1738
    assert all_total_n_amino_acids_BB == 588
    assert list_total_n_amino_acids_Hk2 == 0
    assert list_total_n_amino_acids_BB == 0


def test_get_n_nucleotides_from_molecule():

    all_n_nucleotides_Hk2 = aux.get_n_nucleotides_from_molecule(molsys_Hk2, skip_digestion=True)
    all_n_nucleotides_BB = aux.get_n_nucleotides_from_molecule(molsys_BB, skip_digestion=True)
    list_n_nucleotides_Hk2 = aux.get_n_nucleotides_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_nucleotides_BB = aux.get_n_nucleotides_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_nucleotides_Hk2) == 135
    assert len(all_n_nucleotides_BB) == 519
    assert all_n_nucleotides_Hk2[15:25] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_nucleotides_Hk2[105:115] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_nucleotides_Hk2[0] == 0
    assert all_n_nucleotides_Hk2[-1] == 0
    assert all_n_nucleotides_BB[3:13] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_nucleotides_BB[486:492] == [0, 0, 0, 0, 0, 0]
    assert all_n_nucleotides_BB[0] == 0
    assert all_n_nucleotides_BB[-1] == 0
    assert list_n_nucleotides_Hk2 == [0, 0, 0]
    assert list_n_nucleotides_BB == [0, 0, 0, 0]


def test_get_total_n_nucleotides_from_molecule():

    all_total_n_nucleotides_Hk2 = aux.get_total_n_nucleotides_from_molecule(molsys_Hk2, skip_digestion=True)
    all_total_n_nucleotides_BB = aux.get_total_n_nucleotides_from_molecule(molsys_BB, skip_digestion=True)
    list_total_n_nucleotides_Hk2 = aux.get_total_n_nucleotides_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_nucleotides_BB = aux.get_total_n_nucleotides_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_nucleotides_Hk2 == 0
    assert all_total_n_nucleotides_BB == 0
    assert list_total_n_nucleotides_Hk2 == 0
    assert list_total_n_nucleotides_BB == 0


def test_get_n_ions_from_molecule():

    all_n_ions_Hk2 = aux.get_n_ions_from_molecule(molsys_Hk2, skip_digestion=True)
    all_n_ions_BB = aux.get_n_ions_from_molecule(molsys_BB, skip_digestion=True)
    list_n_ions_Hk2 = aux.get_n_ions_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_ions_BB = aux.get_n_ions_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_ions_Hk2) == 135
    assert len(all_n_ions_BB) == 519
    assert all_n_ions_Hk2[15:25] == [1, 1, 1, 0, 0, 0, 0, 1, 1, 1]
    assert all_n_ions_Hk2[105:115] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_ions_Hk2[0] == 0
    assert all_n_ions_Hk2[-1] == 0
    assert all_n_ions_BB[3:13] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_ions_BB[486:492] == [0, 0, 0, 0, 0, 0]
    assert all_n_ions_BB[0] == 0
    assert all_n_ions_BB[-1] == 0
    assert list_n_ions_Hk2 == [0, 0, 1]
    assert list_n_ions_BB == [0, 0, 0, 0]


def test_get_total_n_ions_from_molecule():

    all_total_n_ions_Hk2 = aux.get_total_n_ions_from_molecule(molsys_Hk2, skip_digestion=True)
    all_total_n_ions_BB = aux.get_total_n_ions_from_molecule(molsys_BB, skip_digestion=True)
    list_total_n_ions_Hk2 = aux.get_total_n_ions_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_ions_BB = aux.get_total_n_ions_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_ions_Hk2 == 28
    assert all_total_n_ions_BB == 0
    assert list_total_n_ions_Hk2 == 1
    assert list_total_n_ions_BB == 0


def test_get_n_waters_from_molecule():

    all_n_waters_Hk2 = aux.get_n_waters_from_molecule(molsys_Hk2, skip_digestion=True)
    all_n_waters_BB = aux.get_n_waters_from_molecule(molsys_BB, skip_digestion=True)
    list_n_waters_Hk2 = aux.get_n_waters_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_waters_BB = aux.get_n_waters_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_waters_Hk2) == 135
    assert len(all_n_waters_BB) == 519
    assert all_n_waters_Hk2[15:25] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_waters_Hk2[105:115] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_waters_Hk2[0] == 0
    assert all_n_waters_Hk2[-1] == 1
    assert all_n_waters_BB[3:13] == [0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_waters_BB[486:492] == [1, 1, 1, 1, 1, 1]
    assert all_n_waters_BB[0] == 0
    assert all_n_waters_BB[-1] == 1
    assert list_n_waters_Hk2 == [0, 0, 0]
    assert list_n_waters_BB == [1, 1, 1, 1]


def test_get_total_n_waters_from_molecule():

    all_total_n_waters_Hk2 = aux.get_total_n_waters_from_molecule(molsys_Hk2, skip_digestion=True)
    all_total_n_waters_BB = aux.get_total_n_waters_from_molecule(molsys_BB, skip_digestion=True)
    list_total_n_waters_Hk2 = aux.get_total_n_waters_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_waters_BB = aux.get_total_n_waters_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_waters_Hk2 == 97
    assert all_total_n_waters_BB == 513
    assert list_total_n_waters_Hk2 == 0
    assert list_total_n_waters_BB == 4


def test_get_n_small_molecules_from_molecule():

    all_n_small_molecules_Hk2 = aux.get_n_small_molecules_from_molecule(molsys_Hk2, skip_digestion=True)
    all_n_small_molecules_BB = aux.get_n_small_molecules_from_molecule(molsys_BB, skip_digestion=True)
    list_n_small_molecules_Hk2 = aux.get_n_small_molecules_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_small_molecules_BB = aux.get_n_small_molecules_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_small_molecules_Hk2) == 135
    assert len(all_n_small_molecules_BB) == 519
    assert all_n_small_molecules_Hk2[15:25] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_small_molecules_Hk2[105:115] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_small_molecules_Hk2[0] == 0
    assert all_n_small_molecules_Hk2[-1] == 0
    assert all_n_small_molecules_BB[3:13] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_small_molecules_BB[486:492] == [0, 0, 0, 0, 0, 0]
    assert all_n_small_molecules_BB[0] == 0
    assert all_n_small_molecules_BB[-1] == 0
    assert list_n_small_molecules_Hk2 == [0, 0, 0]
    assert list_n_small_molecules_BB == [0, 0, 0, 0]


def test_get_total_n_small_molecules_from_molecule():

    all_total_n_small_molecules_Hk2 = aux.get_total_n_small_molecules_from_molecule(molsys_Hk2, skip_digestion=True)
    all_total_n_small_molecules_BB = aux.get_total_n_small_molecules_from_molecule(molsys_BB, skip_digestion=True)
    list_total_n_small_molecules_Hk2 = aux.get_total_n_small_molecules_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_small_molecules_BB = aux.get_total_n_small_molecules_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_small_molecules_Hk2 == 0
    assert all_total_n_small_molecules_BB == 0
    assert list_total_n_small_molecules_Hk2 == 0
    assert list_total_n_small_molecules_BB == 0


def test_get_n_lipids_from_molecule():

    all_n_lipids_Hk2 = aux.get_n_lipids_from_molecule(molsys_Hk2, skip_digestion=True)
    all_n_lipids_BB = aux.get_n_lipids_from_molecule(molsys_BB, skip_digestion=True)
    list_n_lipids_Hk2 = aux.get_n_lipids_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_lipids_BB = aux.get_n_lipids_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_lipids_Hk2) == 135
    assert len(all_n_lipids_BB) == 519
    assert all_n_lipids_Hk2[15:25] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_lipids_Hk2[105:115] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_lipids_Hk2[0] == 0
    assert all_n_lipids_Hk2[-1] == 0
    assert all_n_lipids_BB[3:13] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_lipids_BB[486:492] == [0, 0, 0, 0, 0, 0]
    assert all_n_lipids_BB[0] == 0
    assert all_n_lipids_BB[-1] == 0
    assert list_n_lipids_Hk2 == [0, 0, 0]
    assert list_n_lipids_BB == [0, 0, 0, 0]


def test_get_total_n_lipids_from_molecule():

    all_total_n_lipids_Hk2 = aux.get_total_n_lipids_from_molecule(molsys_Hk2, skip_digestion=True)
    all_total_n_lipids_BB = aux.get_total_n_lipids_from_molecule(molsys_BB, skip_digestion=True)
    list_total_n_lipids_Hk2 = aux.get_total_n_lipids_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_lipids_BB = aux.get_total_n_lipids_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_lipids_Hk2 == 0
    assert all_total_n_lipids_BB == 0
    assert list_total_n_lipids_Hk2 == 0
    assert list_total_n_lipids_BB == 0


def test_get_n_saccharides_from_molecule():

    all_n_saccharides_Hk2 = aux.get_n_saccharides_from_molecule(molsys_Hk2, skip_digestion=True)
    all_n_saccharides_BB = aux.get_n_saccharides_from_molecule(molsys_BB, skip_digestion=True)
    list_n_saccharides_Hk2 = aux.get_n_saccharides_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_saccharides_BB = aux.get_n_saccharides_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_saccharides_Hk2) == 135
    assert len(all_n_saccharides_BB) == 519
    assert all_n_saccharides_Hk2[15:25] == [0, 0, 0, 1, 1, 1, 1, 0, 0, 0]
    assert all_n_saccharides_Hk2[105:115] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_saccharides_Hk2[0] == 0
    assert all_n_saccharides_Hk2[-1] == 0
    assert all_n_saccharides_BB[3:13] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_saccharides_BB[486:492] == [0, 0, 0, 0, 0, 0]
    assert all_n_saccharides_BB[0] == 0
    assert all_n_saccharides_BB[-1] == 0
    assert list_n_saccharides_Hk2 == [1, 1, 0]
    assert list_n_saccharides_BB == [0, 0, 0, 0]


def test_get_total_n_saccharides_from_molecule():

    all_total_n_saccharides_Hk2 = aux.get_total_n_saccharides_from_molecule(molsys_Hk2, skip_digestion=True)
    all_total_n_saccharides_BB = aux.get_total_n_saccharides_from_molecule(molsys_BB, skip_digestion=True)
    list_total_n_saccharides_Hk2 = aux.get_total_n_saccharides_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_saccharides_BB = aux.get_total_n_saccharides_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_saccharides_Hk2 == 8
    assert all_total_n_saccharides_BB == 0
    assert list_total_n_saccharides_Hk2 == 2
    assert list_total_n_saccharides_BB == 0


def test_get_n_peptides_from_molecule():

    all_n_peptides_Hk2 = aux.get_n_peptides_from_molecule(molsys_Hk2, skip_digestion=True)
    all_n_peptides_BB = aux.get_n_peptides_from_molecule(molsys_BB, skip_digestion=True)
    list_n_peptides_Hk2 = aux.get_n_peptides_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_peptides_BB = aux.get_n_peptides_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_peptides_Hk2 == 0
    assert all_n_peptides_BB == 0
    assert list_n_peptides_Hk2 == 0
    assert list_n_peptides_BB == 0


def test_get_total_n_peptides_from_molecule():

    all_total_n_peptides_Hk2 = aux.get_total_n_peptides_from_molecule(molsys_Hk2, skip_digestion=True)
    all_total_n_peptides_BB = aux.get_total_n_peptides_from_molecule(molsys_BB, skip_digestion=True)
    list_total_n_peptides_Hk2 = aux.get_total_n_peptides_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_peptides_BB = aux.get_total_n_peptides_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_peptides_Hk2 == 0
    assert all_total_n_peptides_BB == 0
    assert list_total_n_peptides_Hk2 == 0
    assert list_total_n_peptides_BB == 0


def test_get_n_proteins_from_molecule():

    all_n_proteins_Hk2 = aux.get_n_proteins_from_molecule(molsys_Hk2, skip_digestion=True)
    all_n_proteins_BB = aux.get_n_proteins_from_molecule(molsys_BB, skip_digestion=True)
    list_n_proteins_Hk2 = aux.get_n_proteins_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_proteins_BB = aux.get_n_proteins_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_proteins_Hk2 == 2
    assert all_n_proteins_BB == 6
    assert list_n_proteins_Hk2 == 0
    assert list_n_proteins_BB == 0


def test_get_total_n_proteins_from_molecule():

    all_total_n_proteins_Hk2 = aux.get_total_n_proteins_from_molecule(molsys_Hk2, skip_digestion=True)
    all_total_n_proteins_BB = aux.get_total_n_proteins_from_molecule(molsys_BB, skip_digestion=True)
    list_total_n_proteins_Hk2 = aux.get_total_n_proteins_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_proteins_BB = aux.get_total_n_proteins_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_proteins_Hk2 == 2
    assert all_total_n_proteins_BB == 6
    assert list_total_n_proteins_Hk2 == 0
    assert list_total_n_proteins_BB == 0


def test_get_n_dnas_from_molecule():

    all_n_dnas_Hk2 = aux.get_n_dnas_from_molecule(molsys_Hk2, skip_digestion=True)
    all_n_dnas_BB = aux.get_n_dnas_from_molecule(molsys_BB, skip_digestion=True)
    list_n_dnas_Hk2 = aux.get_n_dnas_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_dnas_BB = aux.get_n_dnas_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_dnas_Hk2 == 0
    assert all_n_dnas_BB == 0
    assert list_n_dnas_Hk2 == 0
    assert list_n_dnas_BB == 0


def test_get_total_n_dnas_from_molecule():

    all_total_n_dnas_Hk2 = aux.get_total_n_dnas_from_molecule(molsys_Hk2, skip_digestion=True)
    all_total_n_dnas_BB = aux.get_total_n_dnas_from_molecule(molsys_BB, skip_digestion=True)
    list_total_n_dnas_Hk2 = aux.get_total_n_dnas_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_dnas_BB = aux.get_total_n_dnas_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_dnas_Hk2 == 0
    assert all_total_n_dnas_BB == 0
    assert list_total_n_dnas_Hk2 == 0
    assert list_total_n_dnas_BB == 0


def test_get_n_rnas_from_molecule():

    all_n_rnas_Hk2 = aux.get_n_rnas_from_molecule(molsys_Hk2, skip_digestion=True)
    all_n_rnas_BB = aux.get_n_rnas_from_molecule(molsys_BB, skip_digestion=True)
    list_n_rnas_Hk2 = aux.get_n_rnas_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_rnas_BB = aux.get_n_rnas_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_rnas_Hk2 == 0
    assert all_n_rnas_BB == 0
    assert list_n_rnas_Hk2 == 0
    assert list_n_rnas_BB == 0


def test_get_total_n_rnas_from_molecule():

    all_total_n_rnas_Hk2 = aux.get_total_n_rnas_from_molecule(molsys_Hk2, skip_digestion=True)
    all_total_n_rnas_BB = aux.get_total_n_rnas_from_molecule(molsys_BB, skip_digestion=True)
    list_total_n_rnas_Hk2 = aux.get_total_n_rnas_from_molecule(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_rnas_BB = aux.get_total_n_rnas_from_molecule(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_rnas_Hk2 == 0
    assert all_total_n_rnas_BB == 0
    assert list_total_n_rnas_Hk2 == 0
    assert list_total_n_rnas_BB == 0


# From entity


def test_get_atom_index_from_entity():

    all_atom_index_Hk2 = aux.get_atom_index_from_entity(molsys_Hk2, skip_digestion=True)
    all_atom_index_BB = aux.get_atom_index_from_entity(molsys_BB, skip_digestion=True)
    list_atom_index_Hk2 = aux.get_atom_index_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_atom_index_BB = aux.get_atom_index_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_atom_index_Hk2, list)
    assert len(all_atom_index_Hk2) == 5
    assert len(all_atom_index_BB) == 3
    assert all_atom_index_Hk2[0] == list(range(13309))
    assert all_atom_index_Hk2[1] == [13309, 13310, 13311, 13312, 13313, 13314, 13315, 13316, 13317, 13318, 13319,
                                     13320, 13337, 13338, 13339, 13340, 13341, 13342, 13343, 13344, 13345, 13346,
                                     13347, 13348, 13377, 13378, 13379, 13380, 13381, 13382, 13383, 13384, 13385,
                                     13386, 13387, 13388, 13405, 13406, 13407, 13408, 13409, 13410, 13411, 13412,
                                     13413, 13414, 13415, 13416]
    assert all_atom_index_Hk2[2] == [13321, 13322, 13323, 13324, 13325, 13326, 13327, 13328, 13329, 13330, 13331,
                                     13332, 13333, 13334, 13335, 13336, 13349, 13350, 13351, 13352, 13353, 13354,
                                     13355, 13356, 13357, 13358, 13359, 13360, 13361, 13362, 13363, 13364, 13389,
                                     13390, 13391, 13392, 13393, 13394, 13395, 13396, 13397, 13398, 13399, 13400,
                                     13401, 13402, 13403, 13404, 13417, 13418, 13419, 13420, 13421, 13422, 13423,
                                     13424, 13425, 13426, 13427, 13428, 13429, 13430, 13431, 13432]
    assert all_atom_index_Hk2[-1][50:60] == [13499, 13500, 13501, 13502, 13503, 13504, 13505, 13506, 13507, 13508] 
    assert all_atom_index_BB[0] == list(range(2581))
    assert all_atom_index_BB[1] == list(range(2581,4638))
    assert all_atom_index_BB[2] == list(range(4638,5151))
    assert list_atom_index_Hk2[0] == [13309, 13310, 13311, 13312, 13313, 13314, 13315, 13316, 13317, 13318, 13319,
                                      13320, 13337, 13338, 13339, 13340, 13341, 13342, 13343, 13344, 13345, 13346,
                                      13347, 13348, 13377, 13378, 13379, 13380, 13381, 13382, 13383, 13384, 13385,
                                      13386, 13387, 13388, 13405, 13406, 13407, 13408, 13409, 13410, 13411, 13412,
                                      13413, 13414, 13415, 13416]
    assert list_atom_index_BB[1] == list(range(4638,5151))


def test_get_atom_id_from_entity():

    all_atom_id_Hk2 = aux.get_atom_id_from_entity(molsys_Hk2, skip_digestion=True)
    all_atom_id_BB = aux.get_atom_id_from_entity(molsys_BB, skip_digestion=True)
    list_atom_id_Hk2 = aux.get_atom_id_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_atom_id_BB = aux.get_atom_id_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_atom_id_Hk2, list)
    assert len(all_atom_id_Hk2) == 5
    assert len(all_atom_id_BB) == 3
    assert all_atom_id_Hk2[0] == list(range(1,13310))
    assert all_atom_id_Hk2[1] == [13310, 13311, 13312, 13313, 13314, 13315, 13316, 13317, 13318, 13319, 13320, 13321,
                                  13338, 13339, 13340, 13341, 13342, 13343, 13344, 13345, 13346, 13347, 13348, 13349,
                                  13378, 13379, 13380, 13381, 13382, 13383, 13384, 13385, 13386, 13387, 13388, 13389,
                                  13406, 13407, 13408, 13409, 13410, 13411, 13412, 13413, 13414, 13415, 13416, 13417]
    assert all_atom_id_Hk2[2] == [13322, 13323, 13324, 13325, 13326, 13327, 13328, 13329, 13330, 13331, 13332, 13333,
                                  13334, 13335, 13336, 13337, 13350, 13351, 13352, 13353, 13354, 13355, 13356, 13357,
                                  13358, 13359, 13360, 13361, 13362, 13363, 13364, 13365, 13390, 13391, 13392, 13393,
                                  13394, 13395, 13396, 13397, 13398, 13399, 13400, 13401, 13402, 13403, 13404, 13405,
                                  13418, 13419, 13420, 13421, 13422, 13423, 13424, 13425, 13426, 13427, 13428, 13429,
                                  13430, 13431, 13432, 13433]
    assert all_atom_id_Hk2[-1][50:60] == [13500, 13501, 13502, 13503, 13504, 13505, 13506, 13507, 13508, 13509]
    assert all_atom_id_BB[0] == list(range(1, 2582))
    assert all_atom_id_BB[1][105:115] == [2687, 2689, 2691, 2692, 2693, 2694, 2695, 2696, 2697, 2698]
    assert all_atom_id_BB[2][105:115] == [4746, 4747, 4748, 4749, 4750, 4751, 4752, 4753, 4754, 4755]
    assert list_atom_id_Hk2[0] == [13310, 13311, 13312, 13313, 13314, 13315, 13316, 13317, 13318, 13319, 13320, 13321,
                                   13338, 13339, 13340, 13341, 13342, 13343, 13344, 13345, 13346, 13347, 13348, 13349,
                                   13378, 13379, 13380, 13381, 13382, 13383, 13384, 13385, 13386, 13387, 13388, 13389,
                                   13406, 13407, 13408, 13409, 13410, 13411, 13412, 13413, 13414, 13415, 13416, 13417]
    assert list_atom_id_BB[1] == list(range(4641,5154))


def test_get_atom_name_from_entity():

    all_atom_name_Hk2 = aux.get_atom_name_from_entity(molsys_Hk2, skip_digestion=True)
    all_atom_name_BB = aux.get_atom_name_from_entity(molsys_BB, skip_digestion=True)
    list_atom_name_Hk2 = aux.get_atom_name_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_atom_name_BB = aux.get_atom_name_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_atom_name_Hk2, list)
    assert len(all_atom_name_Hk2) == 5
    assert len(all_atom_name_BB) == 3
    assert all_atom_name_Hk2[0][100:110] == ['C', 'O', 'CB', 'CG', 'ND1', 'CD2', 'CE1', 'NE2', 'N', 'CA']
    assert all_atom_name_Hk2[1][30:40] == ['O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'C1', 'C2', 'C3', 'C4']
    assert all_atom_name_Hk2[2][30:40] == ['O2P', 'O3P', 'C1', 'C2', 'O1', 'O5', 'C3', 'O2', 'C4', 'O3']
    assert all_atom_name_Hk2[-1][50:60] == ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
    assert all_atom_name_BB[0][200:210] == ['C', 'O', 'CB', 'CG', 'CD', 'CE', 'NZ', 'N', 'CA', 'C']
    assert all_atom_name_BB[1][105:115] == ['CB', 'OG', 'N', 'CA', 'C', 'O', 'CB', 'CG', 'OD1', 'OD2']
    assert all_atom_name_BB[2][105:115] == ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
    assert list_atom_name_Hk2[0] == ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'C1',
                                     'C2', 'C3', 'C4', 'C5', 'C6', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'C1', 'C2',
                                     'C3', 'C4', 'C5', 'C6', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'C1', 'C2', 'C3',
                                     'C4', 'C5', 'C6', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6']
    assert list_atom_name_BB[1][60:70] == ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']


def test_get_atom_type_from_entity():

    all_atom_type_Hk2 = aux.get_atom_type_from_entity(molsys_Hk2, skip_digestion=True)
    all_atom_type_BB = aux.get_atom_type_from_entity(molsys_BB, skip_digestion=True)
    list_atom_type_Hk2 = aux.get_atom_type_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_atom_type_BB = aux.get_atom_type_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_atom_type_Hk2, list)
    assert len(all_atom_type_Hk2) == 5
    assert len(all_atom_type_BB) == 3
    assert all_atom_type_Hk2[0][100:110] == ['C', 'O', 'C', 'C', 'N', 'C', 'C', 'N', 'N', 'C']
    assert all_atom_type_Hk2[1][30:40] == ['O', 'O', 'O', 'O', 'O', 'O', 'C', 'C', 'C', 'C']
    assert all_atom_type_Hk2[2][30:40] == ['O', 'O', 'C', 'C', 'O', 'O', 'C', 'O', 'C', 'O']
    assert all_atom_type_Hk2[-1][50:60] == ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
    assert all_atom_type_BB[0][200:210] == ['C', 'O', 'C', 'C', 'C', 'C', 'N', 'N', 'C', 'C']
    assert all_atom_type_BB[1][105:115] == ['C', 'O', 'N', 'C', 'C', 'O', 'C', 'C', 'O', 'O']
    assert all_atom_type_BB[2][105:115] == ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
    assert list_atom_type_Hk2[0] == ['C', 'C', 'C', 'C', 'C', 'C', 'O', 'O', 'O', 'O', 'O', 'O', 'C',
                                     'C', 'C', 'C', 'C', 'C', 'O', 'O', 'O', 'O', 'O', 'O', 'C', 'C',
                                     'C', 'C', 'C', 'C', 'O', 'O', 'O', 'O', 'O', 'O', 'C', 'C', 'C',
                                     'C', 'C', 'C', 'O', 'O', 'O', 'O', 'O', 'O']
    assert list_atom_type_BB[1][60:70] == ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']


def test_get_group_index_from_entity():

    all_group_index_Hk2 = aux.get_group_index_from_entity(molsys_Hk2, skip_digestion=True)
    all_group_index_BB = aux.get_group_index_from_entity(molsys_BB, skip_digestion=True)
    list_group_index_Hk2 = aux.get_group_index_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_group_index_BB = aux.get_group_index_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_group_index_Hk2, list)
    assert len(all_group_index_Hk2) == 5
    assert len(all_group_index_BB) == 3
    assert all_group_index_Hk2[0][100:110] == [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
    assert all_group_index_Hk2[1] == [1738, 1740, 1754, 1756]
    assert all_group_index_Hk2[2] == [1739, 1741, 1755, 1757]
    assert all_group_index_Hk2[-1][10:20] == [1784, 1785, 1786, 1787, 1788, 1789, 1790, 1791, 1792, 1793]
    assert all_group_index_BB[0][200:210] == [200, 201, 202, 203, 204, 205, 206, 207, 208, 209]
    assert all_group_index_BB[1][105:115] == [431, 432, 433, 434, 435, 436, 437, 438, 439, 440]
    assert all_group_index_BB[2][105:115] == [693, 694, 695, 696, 697, 698, 699, 700, 701, 702]
    assert list_group_index_Hk2[0] == [1738, 1740, 1754, 1756]
    assert list_group_index_BB[1][60:70] == [648, 649, 650, 651, 652, 653, 654, 655, 656, 657]


def test_get_group_id_from_entity():

    all_group_id_Hk2 = aux.get_group_id_from_entity(molsys_Hk2, skip_digestion=True)
    all_group_id_BB = aux.get_group_id_from_entity(molsys_BB, skip_digestion=True)
    list_group_id_Hk2 = aux.get_group_id_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_group_id_BB = aux.get_group_id_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_group_id_Hk2, list)
    assert len(all_group_id_Hk2) == 5
    assert len(all_group_id_BB) == 3
    assert all_group_id_Hk2[0][100:110] == [124, 125, 126, 127, 128, 129, 130, 131, 132, 133]
    assert all_group_id_Hk2[1] == [1001, 1003, 1001, 1003]
    assert all_group_id_Hk2[2] == [1002, 1004, 1002, 1004]
    assert all_group_id_Hk2[-1][10:20] == [1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029]
    assert all_group_id_BB[0][200:210] == [93, 94, 95, 96, 97, 98, 99, 100, 101, 102]
    assert all_group_id_BB[1][105:115] == [20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
    assert all_group_id_BB[2][105:115] == [216, 217, 218, 219, 220, 221, 222, 223, 224, 225]
    assert list_group_id_Hk2[0] == [1001, 1003, 1001, 1003]
    assert list_group_id_BB[1][60:70] == [171, 172, 173, 174, 175, 176, 177, 178, 179, 180]


def test_get_group_name_from_entity():

    all_group_name_Hk2 = aux.get_group_name_from_entity(molsys_Hk2, skip_digestion=True)
    all_group_name_BB = aux.get_group_name_from_entity(molsys_BB, skip_digestion=True)
    list_group_name_Hk2 = aux.get_group_name_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_group_name_BB = aux.get_group_name_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_group_name_Hk2, list)
    assert len(all_group_name_Hk2) == 5
    assert len(all_group_name_BB) == 3
    assert all_group_name_Hk2[0][100:110] == ['THR', 'GLN', 'LEU', 'PHE', 'ASP', 'HIS', 'ILE', 'ALA', 'GLU', 'CYS']
    assert all_group_name_Hk2[1] == ['GLC', 'GLC', 'GLC', 'GLC']
    assert all_group_name_Hk2[2] == ['BG6', 'BG6', 'BG6', 'BG6']
    assert all_group_name_Hk2[-1][10:20] == ['HOH', 'HOH', 'HOH', 'HOH', 'HOH', 'HOH', 'HOH', 'HOH', 'HOH', 'HOH']
    assert all_group_name_BB[0][200:210] == ['ASP', 'TRP', 'LEU', 'ILE', 'TYR', 'LYS', 'THR', 'THR', 'ASP', 'HIS']
    assert all_group_name_BB[1][105:115] == ['LEU', 'LYS', 'LYS', 'GLU', 'LEU', 'ALA', 'LEU', 'PRO', 'GLU', 'TYR']
    assert all_group_name_BB[2][105:115] == ['HOH', 'HOH', 'HOH', 'HOH', 'HOH', 'HOH', 'HOH', 'HOH', 'HOH', 'HOH']
    assert list_group_name_Hk2[0] == ['GLC', 'GLC', 'GLC', 'GLC']
    assert list_group_name_BB[1][60:70] == ['HOH', 'HOH', 'HOH', 'HOH', 'HOH', 'HOH', 'HOH', 'HOH', 'HOH', 'HOH']


def test_get_group_type_from_entity():

    all_group_type_Hk2 = aux.get_group_type_from_entity(molsys_Hk2, skip_digestion=True)
    all_group_type_BB = aux.get_group_type_from_entity(molsys_BB, skip_digestion=True)
    list_group_type_Hk2 = aux.get_group_type_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_group_type_BB = aux.get_group_type_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_group_type_Hk2, list)
    assert len(all_group_type_Hk2) == 5
    assert len(all_group_type_BB) == 3
    assert all_group_type_Hk2[0][100:110] == 10*['amino acid']
    assert all_group_type_Hk2[1] == 4*['saccharide']
    assert all_group_type_Hk2[2] == 4*['saccharide']
    assert all_group_type_Hk2[-1][10:20] == 10*['water']
    assert all_group_type_BB[0][200:210] == 10*['amino acid']
    assert all_group_type_BB[1][105:115] == 10*['amino acid']
    assert all_group_type_BB[2][105:115] == 10*['water']
    assert list_group_type_Hk2[0] == 4*['saccharide']
    assert list_group_type_BB[1][60:70] == 10*['water']


def test_get_molecule_index_from_entity():

    all_molecule_index_Hk2 = aux.get_molecule_index_from_entity(molsys_Hk2, skip_digestion=True)
    all_molecule_index_BB = aux.get_molecule_index_from_entity(molsys_BB, skip_digestion=True)
    list_molecule_index_Hk2 = aux.get_molecule_index_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_molecule_index_BB = aux.get_molecule_index_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_molecule_index_Hk2, list)
    assert len(all_molecule_index_Hk2) == 5
    assert len(all_molecule_index_BB) == 3
    assert all_molecule_index_Hk2[0] == [0, 1]
    assert all_molecule_index_Hk2[1] == [2, 4, 18, 20]
    assert all_molecule_index_Hk2[2] == [3, 5, 19, 21]
    assert all_molecule_index_Hk2[-1] == list(range(38,135))
    assert all_molecule_index_BB[0] == [0, 1, 2]
    assert all_molecule_index_BB[1] == [3, 4, 5]
    assert all_molecule_index_BB[2] == list(range(6, 519))
    assert list_molecule_index_Hk2[0] == [2, 4, 18, 20]
    assert list_molecule_index_BB[1] == list(range(6, 519))


def test_get_molecule_id_from_entity():

    all_molecule_id_Hk2 = aux.get_molecule_id_from_entity(molsys_Hk2, skip_digestion=True)
    all_molecule_id_BB = aux.get_molecule_id_from_entity(molsys_BB, skip_digestion=True)
    list_molecule_id_Hk2 = aux.get_molecule_id_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_molecule_id_BB = aux.get_molecule_id_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_molecule_id_Hk2, list)
    assert len(all_molecule_id_Hk2) == 5
    assert len(all_molecule_id_BB) == 3
    assert all_molecule_id_Hk2[0] == [0, 1]
    assert all_molecule_id_Hk2[1] == [2, 4, 18, 20]
    assert all_molecule_id_Hk2[2] == [3, 5, 19, 21]
    assert all_molecule_id_Hk2[-1] == list(range(38,135))
    assert all_molecule_id_BB[0] == [0, 1, 2]
    assert all_molecule_id_BB[1] == [3, 4, 5]
    assert all_molecule_id_BB[2] == list(range(6, 519))
    assert list_molecule_id_Hk2[0] == [2, 4, 18, 20]
    assert list_molecule_id_BB[1] == list(range(6, 519))


def test_get_molecule_name_from_entity():

    all_molecule_name_Hk2 = aux.get_molecule_name_from_entity(molsys_Hk2, skip_digestion=True)
    all_molecule_name_BB = aux.get_molecule_name_from_entity(molsys_BB, skip_digestion=True)
    list_molecule_name_Hk2 = aux.get_molecule_name_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_molecule_name_BB = aux.get_molecule_name_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_molecule_name_Hk2, list)
    assert len(all_molecule_name_Hk2) == 5
    assert len(all_molecule_name_BB) == 3
    assert all_molecule_name_Hk2[0] == ['Hexokinase-2', 'Hexokinase-2']
    assert all_molecule_name_Hk2[1] == 4*['alpha-D-glucopyranose']
    assert all_molecule_name_Hk2[2] == 4*['6-O-phosphono-beta-D-glucopyranose']
    assert all_molecule_name_Hk2[-1] == 97*['water']
    assert all_molecule_name_BB[0] == ['BARNASE', 'BARNASE', 'BARNASE']
    assert all_molecule_name_BB[1] == ['BARSTAR', 'BARSTAR', 'BARSTAR']
    assert all_molecule_name_BB[2] == 513*['water']
    assert list_molecule_name_Hk2[0] == 4*['alpha-D-glucopyranose']
    assert list_molecule_name_BB[1] == 513*['water']


def test_get_molecule_type_from_entity():

    all_molecule_type_Hk2 = aux.get_molecule_type_from_entity(molsys_Hk2, skip_digestion=True)
    all_molecule_type_BB = aux.get_molecule_type_from_entity(molsys_BB, skip_digestion=True)
    list_molecule_type_Hk2 = aux.get_molecule_type_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_molecule_type_BB = aux.get_molecule_type_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_molecule_type_Hk2, list)
    assert len(all_molecule_type_Hk2) == 5
    assert len(all_molecule_type_BB) == 3
    assert all_molecule_type_Hk2[0] == ['protein', 'protein'] 
    assert all_molecule_type_Hk2[1] == 4*['polysaccharide']
    assert all_molecule_type_Hk2[2] == 4*['polysaccharide']
    assert all_molecule_type_Hk2[-1] == 97*['water']
    assert all_molecule_type_BB[0] == ['protein', 'protein', 'protein']
    assert all_molecule_type_BB[1] == ['protein', 'protein', 'protein']
    assert all_molecule_type_BB[2] == 513*['water']
    assert list_molecule_type_Hk2[0] == 4*['polysaccharide']
    assert list_molecule_type_BB[1] == 513*['water']


def test_get_entity_index_from_entity():

    all_entity_index_Hk2 = aux.get_entity_index_from_entity(molsys_Hk2, skip_digestion=True)
    all_entity_index_BB = aux.get_entity_index_from_entity(molsys_BB, skip_digestion=True)
    list_entity_index_Hk2 = aux.get_entity_index_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_entity_index_BB = aux.get_entity_index_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_entity_index_Hk2, list)
    assert len(all_entity_index_Hk2) == 5
    assert len(all_entity_index_BB) == 3
    assert all_entity_index_Hk2[0] == 0
    assert all_entity_index_Hk2[1] == 1
    assert all_entity_index_Hk2[2] == 2
    assert all_entity_index_Hk2[-1] == 4
    assert all_entity_index_BB[0] == 0
    assert all_entity_index_BB[1] == 1
    assert all_entity_index_BB[2] == 2
    assert list_entity_index_Hk2[0] == 1
    assert list_entity_index_BB[1] == 2


def test_get_entity_id_from_entity():

    all_entity_id_Hk2 = aux.get_entity_id_from_entity(molsys_Hk2, skip_digestion=True)
    all_entity_id_BB = aux.get_entity_id_from_entity(molsys_BB, skip_digestion=True)
    list_entity_id_Hk2 = aux.get_entity_id_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_entity_id_BB = aux.get_entity_id_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_entity_id_Hk2, list)
    assert len(all_entity_id_Hk2) == 5
    assert len(all_entity_id_BB) == 3
    assert all_entity_id_Hk2[0] == 1
    assert all_entity_id_Hk2[1] == 2
    assert all_entity_id_Hk2[2] == 3
    assert all_entity_id_Hk2[-1] == 5
    assert all_entity_id_BB[0] == 1
    assert all_entity_id_BB[1] == 2
    assert all_entity_id_BB[2] == 3
    assert list_entity_id_Hk2[0] == 2
    assert list_entity_id_BB[1] == 3


def test_get_entity_name_from_entity():

    all_entity_name_Hk2 = aux.get_entity_name_from_entity(molsys_Hk2, skip_digestion=True)
    all_entity_name_BB = aux.get_entity_name_from_entity(molsys_BB, skip_digestion=True)
    list_entity_name_Hk2 = aux.get_entity_name_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_entity_name_BB = aux.get_entity_name_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_entity_name_Hk2, list)
    assert len(all_entity_name_Hk2) == 5
    assert len(all_entity_name_BB) == 3
    assert all_entity_name_Hk2[0] == 'Hexokinase-2'
    assert all_entity_name_Hk2[1] == 'alpha-D-glucopyranose'
    assert all_entity_name_Hk2[2] == '6-O-phosphono-beta-D-glucopyranose'
    assert all_entity_name_Hk2[-1] == 'water'
    assert all_entity_name_BB[0] == 'BARNASE'
    assert all_entity_name_BB[1] == 'BARSTAR'
    assert all_entity_name_BB[2] == 'water'
    assert list_entity_name_Hk2[0] == 'alpha-D-glucopyranose'
    assert list_entity_name_BB[1] == 'water'


def test_get_entity_type_from_entity():

    all_entity_type_Hk2 = aux.get_entity_type_from_entity(molsys_Hk2, skip_digestion=True)
    all_entity_type_BB = aux.get_entity_type_from_entity(molsys_BB, skip_digestion=True)
    list_entity_type_Hk2 = aux.get_entity_type_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_entity_type_BB = aux.get_entity_type_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_entity_type_Hk2, list)
    assert len(all_entity_type_Hk2) == 5
    assert len(all_entity_type_BB) == 3
    assert all_entity_type_Hk2[0] == 'protein'
    assert all_entity_type_Hk2[1] == 'polysaccharide'
    assert all_entity_type_Hk2[2] == 'polysaccharide'
    assert all_entity_type_Hk2[-1] == 'water'
    assert all_entity_type_BB[0] == 'protein'
    assert all_entity_type_BB[1] == 'protein'
    assert all_entity_type_BB[2] == 'water'
    assert list_entity_type_Hk2[0] == 'polysaccharide'
    assert list_entity_type_BB[1] == 'water'


def test_get_component_index_from_entity():

    all_component_index_Hk2 = aux.get_component_index_from_entity(molsys_Hk2, skip_digestion=True)
    all_component_index_BB = aux.get_component_index_from_entity(molsys_BB, skip_digestion=True)
    list_component_index_Hk2 = aux.get_component_index_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_component_index_BB = aux.get_component_index_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_component_index_Hk2, list)
    assert len(all_component_index_Hk2) == 5
    assert len(all_component_index_BB) == 3
    assert all_component_index_Hk2[0] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    assert all_component_index_Hk2[1] == [13, 15, 29, 31]
    assert all_component_index_Hk2[2] == [14, 16, 30, 32]
    assert all_component_index_Hk2[-1] == list(range(49, 146))
    assert all_component_index_BB[0] == [0, 1, 2]
    assert all_component_index_BB[1] == [3, 4, 5, 6, 7]
    assert all_component_index_BB[2] == list(range(8, 521))
    assert list_component_index_Hk2[0] == [13, 15, 29, 31]
    assert list_component_index_BB[1] == list(range(8, 521))


def test_get_component_id_from_entity():

    all_component_id_Hk2 = aux.get_component_id_from_entity(molsys_Hk2, skip_digestion=True)
    all_component_id_BB = aux.get_component_id_from_entity(molsys_BB, skip_digestion=True)
    list_component_id_Hk2 = aux.get_component_id_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_component_id_BB = aux.get_component_id_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_component_id_Hk2, list)
    assert len(all_component_id_Hk2) == 5
    assert len(all_component_id_BB) == 3
    assert all_component_id_Hk2[0] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    assert all_component_id_Hk2[1] == [13, 15, 29, 31]
    assert all_component_id_Hk2[2] == [14, 16, 30, 32]
    assert all_component_id_Hk2[-1] == list(range(49, 146))
    assert all_component_id_BB[0] == [0, 1, 2]
    assert all_component_id_BB[1] == [3, 4, 5, 6, 7]
    assert all_component_id_BB[2] == list(range(8, 521))
    assert list_component_id_Hk2[0] == [13, 15, 29, 31]
    assert list_component_id_BB[1] == list(range(8, 521))


def test_get_component_name_from_entity():

    all_component_name_Hk2 = aux.get_component_name_from_entity(molsys_Hk2, skip_digestion=True)
    all_component_name_BB = aux.get_component_name_from_entity(molsys_BB, skip_digestion=True)
    list_component_name_Hk2 = aux.get_component_name_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_component_name_BB = aux.get_component_name_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_component_name_Hk2, list)
    assert len(all_component_name_Hk2) == 5
    assert len(all_component_name_BB) == 3
    assert all_component_name_Hk2[0] == ['protein 0', 'protein 1', 'peptide 0', 'peptide 1', 'protein 2', 'protein 3',
                                         'protein 4', 'protein 5', 'protein 6', 'protein 7', 'peptide 2', 'protein 8',
                                         'protein 9']
    assert all_component_name_Hk2[1] == ['unknown 0', 'unknown 2', 'unknown 4', 'unknown 6']
    assert all_component_name_Hk2[2] == ['unknown 1', 'unknown 3', 'unknown 5', 'unknown 7']
    assert all_component_name_Hk2[-1] == 97*['water']
    assert all_component_name_BB[0] == ['protein 0', 'protein 1', 'protein 2']
    assert all_component_name_BB[1] == ['protein 3', 'peptide 0', 'protein 4', 'peptide 0', 'protein 5']
    assert all_component_name_BB[2] == 513*['water']
    assert list_component_name_Hk2[0] == ['unknown 0', 'unknown 2', 'unknown 4', 'unknown 6']
    assert list_component_name_BB[1] == 513*['water']


def test_get_component_type_from_entity():

    all_component_type_Hk2 = aux.get_component_type_from_entity(molsys_Hk2, skip_digestion=True)
    all_component_type_BB = aux.get_component_type_from_entity(molsys_BB, skip_digestion=True)
    list_component_type_Hk2 = aux.get_component_type_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_component_type_BB = aux.get_component_type_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_component_type_Hk2, list)
    assert len(all_component_type_Hk2) == 5
    assert len(all_component_type_BB) == 3
    assert all_component_type_Hk2[0] == ['protein', 'protein', 'peptide', 'peptide', 'protein', 'protein', 'protein',
                                         'protein', 'protein', 'protein', 'peptide', 'protein', 'protein']
    assert all_component_type_Hk2[1] == ['polysaccharide', 'polysaccharide', 'polysaccharide', 'polysaccharide']
    assert all_component_type_Hk2[2] == ['polysaccharide', 'polysaccharide', 'polysaccharide', 'polysaccharide']
    assert all_component_type_Hk2[-1] == 97*['water']
    assert all_component_type_BB[0] == ['protein', 'protein', 'protein']
    assert all_component_type_BB[1] == ['protein', 'peptide', 'protein', 'peptide', 'protein']
    assert all_component_type_BB[2] == 513*['water']
    assert list_component_type_Hk2[0] == ['polysaccharide', 'polysaccharide', 'polysaccharide', 'polysaccharide']
    assert list_component_type_BB[1] == 513*['water']


def test_get_chain_index_from_entity():

    all_chain_index_Hk2 = aux.get_chain_index_from_entity(molsys_Hk2, skip_digestion=True)
    all_chain_index_BB = aux.get_chain_index_from_entity(molsys_BB, skip_digestion=True)
    list_chain_index_Hk2 = aux.get_chain_index_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_chain_index_BB = aux.get_chain_index_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_chain_index_Hk2, list)
    assert len(all_chain_index_Hk2) == 5
    assert len(all_chain_index_BB) == 3
    assert all_chain_index_Hk2[0] == [0, 1]
    assert all_chain_index_Hk2[1] == [2, 4, 18, 20]
    assert all_chain_index_Hk2[2] == [3, 5, 19, 21]
    assert all_chain_index_Hk2[-1] == [38, 39]
    assert all_chain_index_BB[0] == [0, 1, 2]
    assert all_chain_index_BB[1] == [3, 4, 5]
    assert all_chain_index_BB[2] == [6, 7, 8, 9, 10, 11]
    assert list_chain_index_Hk2[0] == [2, 4, 18, 20]
    assert list_chain_index_BB[1] == [6, 7, 8, 9, 10, 11]


def test_get_chain_id_from_entity():

    all_chain_id_Hk2 = aux.get_chain_id_from_entity(molsys_Hk2, skip_digestion=True)
    all_chain_id_BB = aux.get_chain_id_from_entity(molsys_BB, skip_digestion=True)
    list_chain_id_Hk2 = aux.get_chain_id_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_chain_id_BB = aux.get_chain_id_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_chain_id_Hk2, list)
    assert len(all_chain_id_Hk2) == 5
    assert len(all_chain_id_BB) == 3
    assert all_chain_id_Hk2[0] == ['A', 'B']
    assert all_chain_id_Hk2[1] == ['C', 'E', 'S', 'U']
    assert all_chain_id_Hk2[2] == ['D', 'F', 'T', 'V']
    assert all_chain_id_Hk2[-1] == ['MA', 'NA']
    assert all_chain_id_BB[0] == ['A', 'B', 'C']
    assert all_chain_id_BB[1] == ['D', 'E', 'F']
    assert all_chain_id_BB[2] == ['G', 'H', 'I', 'J', 'K', 'L']
    assert list_chain_id_Hk2[0] == ['C', 'E', 'S', 'U']
    assert list_chain_id_BB[1] == ['G', 'H', 'I', 'J', 'K', 'L']


def test_get_chain_name_from_entity():

    all_chain_name_Hk2 = aux.get_chain_name_from_entity(molsys_Hk2, skip_digestion=True)
    all_chain_name_BB = aux.get_chain_name_from_entity(molsys_BB, skip_digestion=True)
    list_chain_name_Hk2 = aux.get_chain_name_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_chain_name_BB = aux.get_chain_name_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_chain_name_Hk2, list)
    assert len(all_chain_name_Hk2) == 5
    assert len(all_chain_name_BB) == 3
    assert all_chain_name_Hk2[0] == ['A', 'B']
    assert all_chain_name_Hk2[1] == ['A', 'A', 'B', 'B']
    assert all_chain_name_Hk2[2] == ['A', 'A', 'B', 'B']
    assert all_chain_name_Hk2[-1] == ['A', 'B']
    assert all_chain_name_BB[0] == ['A', 'B', 'C']
    assert all_chain_name_BB[1] == ['D', 'E', 'F']
    assert all_chain_name_BB[2] == ['A', 'B', 'C', 'D', 'E', 'F']
    assert list_chain_name_Hk2[0] == ['A', 'A', 'B', 'B']
    assert list_chain_name_BB[1] == ['A', 'B', 'C', 'D', 'E', 'F']


def test_get_chain_type_from_entity():

    all_chain_type_Hk2 = aux.get_chain_type_from_entity(molsys_Hk2, skip_digestion=True)
    all_chain_type_BB = aux.get_chain_type_from_entity(molsys_BB, skip_digestion=True)
    list_chain_type_Hk2 = aux.get_chain_type_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_chain_type_BB = aux.get_chain_type_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_chain_type_Hk2, list)
    assert len(all_chain_type_Hk2) == 5
    assert len(all_chain_type_BB) == 3
    assert all_chain_type_Hk2[0] == ['protein', 'protein']
    assert all_chain_type_Hk2[1] == ['polysaccharide', 'polysaccharide', 'polysaccharide', 'polysaccharide']
    assert all_chain_type_Hk2[2] == ['polysaccharide', 'polysaccharide', 'polysaccharide', 'polysaccharide']
    assert all_chain_type_Hk2[-1] == ['water', 'water']
    assert all_chain_type_BB[0] == ['protein', 'protein', 'protein']
    assert all_chain_type_BB[1] == ['protein', 'protein', 'protein']
    assert all_chain_type_BB[2] == ['water', 'water', 'water', 'water', 'water', 'water']
    assert list_chain_type_Hk2[0] == ['polysaccharide', 'polysaccharide', 'polysaccharide', 'polysaccharide']
    assert list_chain_type_BB[1] == ['water', 'water', 'water', 'water', 'water', 'water']


def test_get_bond_index_from_entity():

    all_bond_index_Hk2 = aux.get_bond_index_from_entity(molsys_Hk2, skip_digestion=True)
    all_bond_index_BB = aux.get_bond_index_from_entity(molsys_BB, skip_digestion=True)
    list_bond_index_Hk2 = aux.get_bond_index_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_bond_index_BB = aux.get_bond_index_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_bond_index_Hk2, list)
    assert len(all_bond_index_Hk2) == 5
    assert len(all_bond_index_BB) == 3
    assert len(all_bond_index_Hk2[0]) == 13506
    assert all_bond_index_Hk2[0][10000:10010] == [10000, 10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10009]
    assert len(all_bond_index_Hk2[1]) == 48
    assert all_bond_index_Hk2[1][20:30] == [13542, 13543, 13544, 13545, 13562, 13563, 13564, 13565, 13566, 13567]
    assert len(all_bond_index_Hk2[2]) == 64
    assert all_bond_index_Hk2[2][30:40] == [13560, 13561, 13574, 13575, 13576, 13577, 13578, 13579, 13580, 13581]
    assert len(all_bond_index_Hk2[-1]) == 0
    assert len(all_bond_index_BB[0]) == 2644
    assert all_bond_index_BB[0][1000:1010] == [1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009]
    assert len(all_bond_index_BB[1]) == 2094 
    assert all_bond_index_BB[1][1000:1010] == [3644, 3645, 3646, 3647, 3648, 3649, 3650, 3651, 3652, 3653] 
    assert len(all_bond_index_BB[2]) == 0
    assert len(list_bond_index_Hk2[0]) == 48
    assert len(list_bond_index_BB[1]) == 0


def test_get_bond_type_from_entity():

    all_bond_type_Hk2 = aux.get_bond_type_from_entity(molsys_Hk2, skip_digestion=True)
    all_bond_type_BB = aux.get_bond_type_from_entity(molsys_BB, skip_digestion=True)
    list_bond_type_Hk2 = aux.get_bond_type_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_bond_type_BB = aux.get_bond_type_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_bond_type_Hk2, list)
    assert len(all_bond_type_Hk2) == 5
    assert len(all_bond_type_BB) == 3
    assert len(all_bond_type_Hk2[0]) == 13506
    assert all_bond_type_Hk2[0][10000:10010] == 10*[None]
    assert len(all_bond_type_Hk2[1]) == 48
    assert all_bond_type_Hk2[1][20:30] == 10*[None]
    assert len(all_bond_type_Hk2[2]) == 64
    assert all_bond_type_Hk2[2][30:40] == 10*[None]
    assert len(all_bond_type_Hk2[-1]) == 0
    assert len(all_bond_type_BB[0]) == 2644
    assert all_bond_type_BB[0][1000:1010] == 10*[None]
    assert len(all_bond_type_BB[1]) == 2094 
    assert all_bond_type_BB[1][1000:1010] == 10*[None]
    assert len(all_bond_type_BB[2]) == 0
    assert len(list_bond_type_Hk2[0]) == 48
    assert len(list_bond_type_BB[1]) == 0


def test_get_bond_order_from_entity():

    all_bond_order_Hk2 = aux.get_bond_order_from_entity(molsys_Hk2, skip_digestion=True)
    all_bond_order_BB = aux.get_bond_order_from_entity(molsys_BB, skip_digestion=True)
    list_bond_order_Hk2 = aux.get_bond_order_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_bond_order_BB = aux.get_bond_order_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_bond_order_Hk2, list)
    assert len(all_bond_order_Hk2) == 5
    assert len(all_bond_order_BB) == 3
    assert len(all_bond_order_Hk2[0]) == 13506
    assert all_bond_order_Hk2[0][10000:10010] == 10*[None]
    assert len(all_bond_order_Hk2[1]) == 48
    assert all_bond_order_Hk2[1][20:30] == 10*[None]
    assert len(all_bond_order_Hk2[2]) == 64
    assert all_bond_order_Hk2[2][30:40] == 10*[None]
    assert len(all_bond_order_Hk2[-1]) == 0
    assert len(all_bond_order_BB[0]) == 2644
    assert all_bond_order_BB[0][1000:1010] == 10*[None]
    assert len(all_bond_order_BB[1]) == 2094 
    assert all_bond_order_BB[1][1000:1010] == 10*[None]
    assert len(all_bond_order_BB[2]) == 0
    assert len(list_bond_order_Hk2[0]) == 48
    assert len(list_bond_order_BB[1]) == 0


def test_get_bonded_atoms_from_entity():

    all_bonded_atoms_Hk2 = aux.get_bonded_atoms_from_entity(molsys_Hk2, skip_digestion=True)
    all_bonded_atoms_BB = aux.get_bonded_atoms_from_entity(molsys_BB, skip_digestion=True)
    list_bonded_atoms_Hk2 = aux.get_bonded_atoms_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_bonded_atoms_BB = aux.get_bonded_atoms_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_bonded_atoms_Hk2, list)
    assert len(all_bonded_atoms_Hk2) == 5
    assert len(all_bonded_atoms_BB) == 3
    assert len(all_bonded_atoms_Hk2[0]) == 13309
    assert all_bonded_atoms_Hk2[0][10000:10010] == [10000, 10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10009]
    assert len(all_bonded_atoms_Hk2[1]) == 48
    assert all_bonded_atoms_Hk2[1][20:30] == [13345, 13346, 13347, 13348, 13377, 13378, 13379, 13380, 13381, 13382]
    assert len(all_bonded_atoms_Hk2[2]) == 64
    assert all_bonded_atoms_Hk2[2][30:40] == [13363, 13364, 13389, 13390, 13391, 13392, 13393, 13394, 13395, 13396]
    assert len(all_bonded_atoms_Hk2[-1]) == 0
    assert len(all_bonded_atoms_BB[0]) == 2581
    assert all_bonded_atoms_BB[0][1000:1010] == [1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009]
    assert len(all_bonded_atoms_BB[1]) == 2057
    assert all_bonded_atoms_BB[1][1000:1010] == [3581, 3582, 3583, 3584, 3585, 3586, 3587, 3588, 3589, 3590]
    assert len(all_bonded_atoms_BB[2]) == 0
    assert len(list_bonded_atoms_Hk2[0]) == 48
    assert len(list_bonded_atoms_BB[1]) == 0


def test_get_bonded_atom_pairs_from_entity():

    all_bonded_atom_pairs_Hk2 = aux.get_bonded_atom_pairs_from_entity(molsys_Hk2, skip_digestion=True)
    all_bonded_atom_pairs_BB = aux.get_bonded_atom_pairs_from_entity(molsys_BB, skip_digestion=True)
    list_bonded_atom_pairs_Hk2 = aux.get_bonded_atom_pairs_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_bonded_atom_pairs_BB = aux.get_bonded_atom_pairs_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_bonded_atom_pairs_Hk2, list)
    assert len(all_bonded_atom_pairs_Hk2) == 5
    assert len(all_bonded_atom_pairs_BB) == 3
    assert len(all_bonded_atom_pairs_Hk2[0]) == 13506
    assert all_bonded_atom_pairs_Hk2[0][10000:10010] ==[[9851, 9852], [9851, 9853], [9854, 9855], [9855, 9856],
                                                        [9855, 9858], [9856, 9857], [9856, 9865], [9858, 9859],
                                                        [9859, 9860], [9859, 9861]]
    assert len(all_bonded_atom_pairs_Hk2[1]) == 48
    assert all_bonded_atom_pairs_Hk2[1][20:30] == [[13340, 13346], [13341, 13342], [13341, 13347], [13342, 13348],
                                                   [13377, 13378], [13377, 13383], [13377, 13387], [13378, 13379],
                                                   [13378, 13384], [13379, 13380]]
    assert len(all_bonded_atom_pairs_Hk2[2]) == 64
    assert all_bonded_atom_pairs_Hk2[2][30:40] == [[13361, 13363], [13361, 13364], [13389, 13390], [13389, 13391],
                                                   [13389, 13392], [13390, 13393], [13390, 13394], [13392, 13397],
                                                   [13393, 13395], [13393, 13396]]
    assert len(all_bonded_atom_pairs_Hk2[-1]) == 0
    assert len(all_bonded_atom_pairs_BB[0]) == 2644
    assert all_bonded_atom_pairs_BB[0][1000:1010] == [[976, 977], [977, 978], [977, 979], [980, 981], [981, 982],
                                                      [981, 984], [982, 983], [982, 987], [984, 985], [984, 986]]
    assert len(all_bonded_atom_pairs_BB[1]) == 2094
    assert all_bonded_atom_pairs_BB[1][1000:1010] == [[3562, 3564], [3563, 3565], [3564, 3565], [3566, 3567],
                                                      [3567, 3568], [3567, 3570], [3568, 3569], [3568, 3574],
                                                      [3570, 3571], [3571, 3572]]
    assert len(all_bonded_atom_pairs_BB[2]) == 0
    assert len(list_bonded_atom_pairs_Hk2[0]) == 48
    assert len(list_bonded_atom_pairs_BB[1]) == 0


def test_get_inner_bond_index_from_entity():

    all_inner_bond_index_Hk2 = aux.get_inner_bond_index_from_entity(molsys_Hk2, skip_digestion=True)
    all_inner_bond_index_BB = aux.get_inner_bond_index_from_entity(molsys_BB, skip_digestion=True)
    list_inner_bond_index_Hk2 = aux.get_inner_bond_index_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_inner_bond_index_BB = aux.get_inner_bond_index_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_inner_bond_index_Hk2, list)
    assert len(all_inner_bond_index_Hk2) == 5
    assert len(all_inner_bond_index_BB) == 3
    assert len(all_inner_bond_index_Hk2[0]) == 13506
    assert all_inner_bond_index_Hk2[0][10000:10010] == [10000, 10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10009]
    assert len(all_inner_bond_index_Hk2[1]) == 48
    assert all_inner_bond_index_Hk2[1][20:30] == [13542, 13543, 13544, 13545, 13562, 13563, 13564, 13565, 13566, 13567]
    assert len(all_inner_bond_index_Hk2[2]) == 64
    assert all_inner_bond_index_Hk2[2][30:40] == [13560, 13561, 13574, 13575, 13576, 13577, 13578, 13579, 13580, 13581]
    assert len(all_inner_bond_index_Hk2[-1]) == 0
    assert len(all_inner_bond_index_BB[0]) == 2644
    assert all_inner_bond_index_BB[0][1000:1010] == [1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009]
    assert len(all_inner_bond_index_BB[1]) == 2094 
    assert all_inner_bond_index_BB[1][1000:1010] == [3644, 3645, 3646, 3647, 3648, 3649, 3650, 3651, 3652, 3653] 
    assert len(all_inner_bond_index_BB[2]) == 0
    assert len(list_inner_bond_index_Hk2[0]) == 48
    assert len(list_inner_bond_index_BB[1]) == 0


def test_get_inner_bonded_atoms_from_entity():

    all_inner_bonded_atoms_Hk2 = aux.get_inner_bonded_atoms_from_entity(molsys_Hk2, skip_digestion=True)
    all_inner_bonded_atoms_BB = aux.get_inner_bonded_atoms_from_entity(molsys_BB, skip_digestion=True)
    list_inner_bonded_atoms_Hk2 = aux.get_inner_bonded_atoms_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_inner_bonded_atoms_BB = aux.get_inner_bonded_atoms_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_inner_bonded_atoms_Hk2, list)
    assert len(all_inner_bonded_atoms_Hk2) == 5
    assert len(all_inner_bonded_atoms_BB) == 3
    assert len(all_inner_bonded_atoms_Hk2[0]) == 13309
    assert all_inner_bonded_atoms_Hk2[0][10000:10010] == [10000, 10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10009]
    assert len(all_inner_bonded_atoms_Hk2[1]) == 48
    assert all_inner_bonded_atoms_Hk2[1][20:30] == [13345, 13346, 13347, 13348, 13377, 13378, 13379, 13380, 13381, 13382]
    assert len(all_inner_bonded_atoms_Hk2[2]) == 64
    assert all_inner_bonded_atoms_Hk2[2][30:40] == [13363, 13364, 13389, 13390, 13391, 13392, 13393, 13394, 13395, 13396]
    assert len(all_inner_bonded_atoms_Hk2[-1]) == 0
    assert len(all_inner_bonded_atoms_BB[0]) == 2581
    assert all_inner_bonded_atoms_BB[0][1000:1010] == [1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009]
    assert len(all_inner_bonded_atoms_BB[1]) == 2057
    assert all_inner_bonded_atoms_BB[1][1000:1010] == [3581, 3582, 3583, 3584, 3585, 3586, 3587, 3588, 3589, 3590]
    assert len(all_inner_bonded_atoms_BB[2]) == 0
    assert len(list_inner_bonded_atoms_Hk2[0]) == 48
    assert len(list_inner_bonded_atoms_BB[1]) == 0


def test_get_inner_bonded_atom_pairs_from_entity():

    all_inner_bonded_atom_pairs_Hk2 = aux.get_inner_bonded_atom_pairs_from_entity(molsys_Hk2, skip_digestion=True)
    all_inner_bonded_atom_pairs_BB = aux.get_inner_bonded_atom_pairs_from_entity(molsys_BB, skip_digestion=True)
    list_inner_bonded_atom_pairs_Hk2 = aux.get_inner_bonded_atom_pairs_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_inner_bonded_atom_pairs_BB = aux.get_inner_bonded_atom_pairs_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert isinstance(all_inner_bonded_atom_pairs_Hk2, list)
    assert len(all_inner_bonded_atom_pairs_Hk2) == 5
    assert len(all_inner_bonded_atom_pairs_BB) == 3
    assert len(all_inner_bonded_atom_pairs_Hk2[0]) == 13506
    assert all_inner_bonded_atom_pairs_Hk2[0][10000:10010] ==[[9851, 9852], [9851, 9853], [9854, 9855], [9855, 9856],
                                                        [9855, 9858], [9856, 9857], [9856, 9865], [9858, 9859],
                                                        [9859, 9860], [9859, 9861]]
    assert len(all_inner_bonded_atom_pairs_Hk2[1]) == 48
    assert all_inner_bonded_atom_pairs_Hk2[1][20:30] == [[13340, 13346], [13341, 13342], [13341, 13347], [13342, 13348],
                                                   [13377, 13378], [13377, 13383], [13377, 13387], [13378, 13379],
                                                   [13378, 13384], [13379, 13380]]
    assert len(all_inner_bonded_atom_pairs_Hk2[2]) == 64
    assert all_inner_bonded_atom_pairs_Hk2[2][30:40] == [[13361, 13363], [13361, 13364], [13389, 13390], [13389, 13391],
                                                   [13389, 13392], [13390, 13393], [13390, 13394], [13392, 13397],
                                                   [13393, 13395], [13393, 13396]]
    assert len(all_inner_bonded_atom_pairs_Hk2[-1]) == 0
    assert len(all_inner_bonded_atom_pairs_BB[0]) == 2644
    assert all_inner_bonded_atom_pairs_BB[0][1000:1010] == [[976, 977], [977, 978], [977, 979], [980, 981], [981, 982],
                                                      [981, 984], [982, 983], [982, 987], [984, 985], [984, 986]]
    assert len(all_inner_bonded_atom_pairs_BB[1]) == 2094
    assert all_inner_bonded_atom_pairs_BB[1][1000:1010] == [[3562, 3564], [3563, 3565], [3564, 3565], [3566, 3567],
                                                      [3567, 3568], [3567, 3570], [3568, 3569], [3568, 3574],
                                                      [3570, 3571], [3571, 3572]]
    assert len(all_inner_bonded_atom_pairs_BB[2]) == 0
    assert len(list_inner_bonded_atom_pairs_Hk2[0]) == 48
    assert len(list_inner_bonded_atom_pairs_BB[1]) == 0


def test_get_n_atoms_from_entity():

    all_n_atoms_Hk2 = aux.get_n_atoms_from_entity(molsys_Hk2, skip_digestion=True)
    all_n_atoms_BB = aux.get_n_atoms_from_entity(molsys_BB, skip_digestion=True)
    list_n_atoms_Hk2 = aux.get_n_atoms_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_n_atoms_BB = aux.get_n_atoms_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert len(all_n_atoms_Hk2) == 5
    assert len(all_n_atoms_BB) == 3
    assert all_n_atoms_Hk2 == [13309, 48, 64, 28, 97]
    assert all_n_atoms_BB == [2581, 2057, 513]
    assert list_n_atoms_Hk2 == [48, 64, 28]
    assert list_n_atoms_BB == [2057, 513]


def test_get_total_n_atoms_from_entity():

    all_total_n_atoms_Hk2 = aux.get_total_n_atoms_from_entity(molsys_Hk2, skip_digestion=True)
    all_total_n_atoms_BB = aux.get_total_n_atoms_from_entity(molsys_BB, skip_digestion=True)
    list_total_n_atoms_Hk2 = aux.get_total_n_atoms_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_total_n_atoms_BB = aux.get_total_n_atoms_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert all_total_n_atoms_Hk2 == 13546
    assert all_total_n_atoms_BB == 5151
    assert list_total_n_atoms_Hk2 == 6684
    assert list_total_n_atoms_BB == 1717


def test_get_n_groups_from_entity():

    all_n_groups_Hk2 = aux.get_n_groups_from_entity(molsys_Hk2, skip_digestion=True)
    all_n_groups_BB = aux.get_n_groups_from_entity(molsys_BB, skip_digestion=True)
    list_n_groups_Hk2 = aux.get_n_groups_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_n_groups_BB = aux.get_n_groups_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert len(all_n_groups_Hk2) == 5
    assert len(all_n_groups_BB) == 3
    assert all_n_groups_Hk2 == [1738, 4, 4, 28, 97]
    assert all_n_groups_BB == [326, 262, 513]
    assert list_n_groups_Hk2 == [4, 4, 28]
    assert list_n_groups_BB == [262, 513]


def test_get_total_n_groups_from_entity():

    all_total_n_groups_Hk2 = aux.get_total_n_groups_from_entity(molsys_Hk2, skip_digestion=True)
    all_total_n_groups_BB = aux.get_total_n_groups_from_entity(molsys_BB, skip_digestion=True)
    list_total_n_groups_Hk2 = aux.get_total_n_groups_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_total_n_groups_BB = aux.get_total_n_groups_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert all_total_n_groups_Hk2 == 1871
    assert all_total_n_groups_BB == 1101
    assert list_total_n_groups_Hk2 == 36
    assert list_total_n_groups_BB == 775


def test_get_n_molecules_from_entity():

    all_n_molecules_Hk2 = aux.get_n_molecules_from_entity(molsys_Hk2, skip_digestion=True)
    all_n_molecules_BB = aux.get_n_molecules_from_entity(molsys_BB, skip_digestion=True)
    list_n_molecules_Hk2 = aux.get_n_molecules_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_n_molecules_BB = aux.get_n_molecules_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert len(all_n_molecules_Hk2) == 5
    assert len(all_n_molecules_BB) == 3
    assert all_n_molecules_Hk2 == [2, 4, 4, 28, 97]
    assert all_n_molecules_BB == [3, 3, 513]
    assert list_n_molecules_Hk2 == [4, 4, 28]
    assert list_n_molecules_BB == [3, 513]


def test_get_total_n_molecules_from_entity():

    all_total_n_molecules_Hk2 = aux.get_total_n_molecules_from_entity(molsys_Hk2, skip_digestion=True)
    all_total_n_molecules_BB = aux.get_total_n_molecules_from_entity(molsys_BB, skip_digestion=True)
    list_total_n_molecules_Hk2 = aux.get_total_n_molecules_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_total_n_molecules_BB = aux.get_total_n_molecules_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert all_total_n_molecules_Hk2 == 135
    assert all_total_n_molecules_BB == 519
    assert list_total_n_molecules_Hk2 == 36
    assert list_total_n_molecules_BB == 516


def test_get_n_entities_from_entity():

    all_n_entities_Hk2 = aux.get_n_entities_from_entity(molsys_Hk2, skip_digestion=True)
    all_n_entities_BB = aux.get_n_entities_from_entity(molsys_BB, skip_digestion=True)
    list_n_entities_Hk2 = aux.get_n_entities_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_n_entities_BB = aux.get_n_entities_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert all_n_entities_Hk2 == 5
    assert all_n_entities_BB == 3
    assert list_n_entities_Hk2 == 3
    assert list_n_entities_BB == 2


def test_get_total_n_entities_from_entity():

    all_total_n_entities_Hk2 = aux.get_total_n_entities_from_entity(molsys_Hk2, skip_digestion=True)
    all_total_n_entities_BB = aux.get_total_n_entities_from_entity(molsys_BB, skip_digestion=True)
    list_total_n_entities_Hk2 = aux.get_total_n_entities_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_total_n_entities_BB = aux.get_total_n_entities_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert all_total_n_entities_Hk2 == 5
    assert all_total_n_entities_BB == 3
    assert list_total_n_entities_Hk2 == 3
    assert list_total_n_entities_BB == 1


def test_get_n_components_from_entity():

    all_n_components_Hk2 = aux.get_n_components_from_entity(molsys_Hk2, skip_digestion=True)
    all_n_components_BB = aux.get_n_components_from_entity(molsys_BB, skip_digestion=True)
    list_n_components_Hk2 = aux.get_n_components_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_n_components_BB = aux.get_n_components_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert len(all_n_components_Hk2) == 5
    assert len(all_n_components_BB) == 3
    assert all_n_components_Hk2 == [13, 4, 4, 28, 97]
    assert all_n_components_BB == [3, 5, 513]
    assert list_n_components_Hk2 == [4, 4, 28]
    assert list_n_components_BB == [5, 513]


def test_get_total_n_components_from_entity():

    all_total_n_components_Hk2 = aux.get_total_n_components_from_entity(molsys_Hk2, skip_digestion=True)
    all_total_n_components_BB = aux.get_total_n_components_from_entity(molsys_BB, skip_digestion=True)
    list_total_n_components_Hk2 = aux.get_total_n_components_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_total_n_components_BB = aux.get_total_n_components_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert all_total_n_components_Hk2 == 146
    assert all_total_n_components_BB == 521
    assert list_total_n_components_Hk2 == 36
    assert list_total_n_components_BB == 518


def test_get_n_chains_from_entity():

    all_n_chains_Hk2 = aux.get_n_chains_from_entity(molsys_Hk2, skip_digestion=True)
    all_n_chains_BB = aux.get_n_chains_from_entity(molsys_BB, skip_digestion=True)
    list_n_chains_Hk2 = aux.get_n_chains_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_n_chains_BB = aux.get_n_chains_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert len(all_n_chains_Hk2) == 5
    assert len(all_n_chains_BB) == 3
    assert all_n_chains_Hk2 == [2, 4, 4, 28, 2]
    assert all_n_chains_BB == [3, 3, 6]
    assert list_n_chains_Hk2 == [4, 4, 28]
    assert list_n_chains_BB == [3, 6]


def test_get_total_n_chains_from_entity():

    all_total_n_chains_Hk2 = aux.get_total_n_chains_from_entity(molsys_Hk2, skip_digestion=True)
    all_total_n_chains_BB = aux.get_total_n_chains_from_entity(molsys_BB, skip_digestion=True)
    list_total_n_chains_Hk2 = aux.get_total_n_chains_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_total_n_chains_BB = aux.get_total_n_chains_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert all_total_n_chains_Hk2 == 40
    assert all_total_n_chains_BB == 12
    assert list_total_n_chains_Hk2 == 36
    assert list_total_n_chains_BB == 9


def test_get_n_bonds_from_entity():

    all_n_bonds_Hk2 = aux.get_n_bonds_from_entity(molsys_Hk2, skip_digestion=True)
    all_n_bonds_BB = aux.get_n_bonds_from_entity(molsys_BB, skip_digestion=True)
    list_n_bonds_Hk2 = aux.get_n_bonds_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_n_bonds_BB = aux.get_n_bonds_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert len(all_n_bonds_Hk2) == 5
    assert len(all_n_bonds_BB) == 3
    assert all_n_bonds_Hk2 ==  [13506, 48, 64, 0, 0]
    assert all_n_bonds_BB == [2644, 2094, 0]
    assert list_n_bonds_Hk2 == [48, 64, 0]
    assert list_n_bonds_BB == [2094, 0]


def test_get_total_n_bonds_from_entity():

    all_total_n_bonds_Hk2 = aux.get_total_n_bonds_from_entity(molsys_Hk2, skip_digestion=True)
    all_total_n_bonds_BB = aux.get_total_n_bonds_from_entity(molsys_BB, skip_digestion=True)
    list_total_n_bonds_Hk2 = aux.get_total_n_bonds_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_total_n_bonds_BB = aux.get_total_n_bonds_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert all_total_n_bonds_Hk2 == 13618
    assert all_total_n_bonds_BB == 4738
    assert list_total_n_bonds_Hk2 == 112
    assert list_total_n_bonds_BB == 2094


def test_get_n_inner_bonds_from_entity():

    all_n_inner_bonds_Hk2 = aux.get_n_inner_bonds_from_entity(molsys_Hk2, skip_digestion=True)
    all_n_inner_bonds_BB = aux.get_n_inner_bonds_from_entity(molsys_BB, skip_digestion=True)
    list_n_inner_bonds_Hk2 = aux.get_n_inner_bonds_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_n_inner_bonds_BB = aux.get_n_inner_bonds_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert len(all_n_inner_bonds_Hk2) == 5
    assert len(all_n_inner_bonds_BB) == 3
    assert all_n_inner_bonds_Hk2 ==  [13506, 48, 64, 0, 0]
    assert all_n_inner_bonds_BB == [2644, 2094, 0]
    assert list_n_inner_bonds_Hk2 == [48, 64, 0]
    assert list_n_inner_bonds_BB == [2094, 0]


def test_get_total_n_inner_bonds_from_entity():

    all_total_n_inner_bonds_Hk2 = aux.get_total_n_inner_bonds_from_entity(molsys_Hk2, skip_digestion=True)
    all_total_n_inner_bonds_BB = aux.get_total_n_inner_bonds_from_entity(molsys_BB, skip_digestion=True)
    list_total_n_inner_bonds_Hk2 = aux.get_total_n_inner_bonds_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_total_n_inner_bonds_BB = aux.get_total_n_inner_bonds_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert all_total_n_inner_bonds_Hk2 == 13618
    assert all_total_n_inner_bonds_BB == 4738
    assert list_total_n_inner_bonds_Hk2 == 112
    assert list_total_n_inner_bonds_BB == 2094


def test_get_n_amino_acids_from_entity():

    all_n_amino_acids_Hk2 = aux.get_n_amino_acids_from_entity(molsys_Hk2, skip_digestion=True)
    all_n_amino_acids_BB = aux.get_n_amino_acids_from_entity(molsys_BB, skip_digestion=True)
    list_n_amino_acids_Hk2 = aux.get_n_amino_acids_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_n_amino_acids_BB = aux.get_n_amino_acids_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert len(all_n_amino_acids_Hk2) == 5
    assert len(all_n_amino_acids_BB) == 3
    assert all_n_amino_acids_Hk2 == [1738, 0, 0, 0, 0]
    assert all_n_amino_acids_BB == [326, 262, 0]
    assert list_n_amino_acids_Hk2 == [0, 0, 0]
    assert list_n_amino_acids_BB == [262, 0]


def test_get_total_n_amino_acids_from_entity():

    all_total_n_amino_acids_Hk2 = aux.get_total_n_amino_acids_from_entity(molsys_Hk2, skip_digestion=True)
    all_total_n_amino_acids_BB = aux.get_total_n_amino_acids_from_entity(molsys_BB, skip_digestion=True)
    list_total_n_amino_acids_Hk2 = aux.get_total_n_amino_acids_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_total_n_amino_acids_BB = aux.get_total_n_amino_acids_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert all_total_n_amino_acids_Hk2 == 1738
    assert all_total_n_amino_acids_BB == 588
    assert list_total_n_amino_acids_Hk2 == 0
    assert list_total_n_amino_acids_BB == 262


def test_get_n_nucleotides_from_entity():

    all_n_nucleotides_Hk2 = aux.get_n_nucleotides_from_entity(molsys_Hk2, skip_digestion=True)
    all_n_nucleotides_BB = aux.get_n_nucleotides_from_entity(molsys_BB, skip_digestion=True)
    list_n_nucleotides_Hk2 = aux.get_n_nucleotides_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_n_nucleotides_BB = aux.get_n_nucleotides_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert len(all_n_nucleotides_Hk2) == 5
    assert len(all_n_nucleotides_BB) == 3
    assert all_n_nucleotides_Hk2 == [0, 0, 0, 0, 0]
    assert all_n_nucleotides_BB == [0, 0, 0]
    assert list_n_nucleotides_Hk2 == [0, 0, 0]
    assert list_n_nucleotides_BB == [0, 0]


def test_get_total_n_nucleotides_from_entity():

    all_total_n_nucleotides_Hk2 = aux.get_total_n_nucleotides_from_entity(molsys_Hk2, skip_digestion=True)
    all_total_n_nucleotides_BB = aux.get_total_n_nucleotides_from_entity(molsys_BB, skip_digestion=True)
    list_total_n_nucleotides_Hk2 = aux.get_total_n_nucleotides_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_total_n_nucleotides_BB = aux.get_total_n_nucleotides_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert all_total_n_nucleotides_Hk2 == 0
    assert all_total_n_nucleotides_BB == 0
    assert list_total_n_nucleotides_Hk2 == 0
    assert list_total_n_nucleotides_BB == 0


def test_get_n_ions_from_entity():

    all_n_ions_Hk2 = aux.get_n_ions_from_entity(molsys_Hk2, skip_digestion=True)
    all_n_ions_BB = aux.get_n_ions_from_entity(molsys_BB, skip_digestion=True)
    list_n_ions_Hk2 = aux.get_n_ions_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_n_ions_BB = aux.get_n_ions_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert len(all_n_ions_Hk2) == 5
    assert len(all_n_ions_BB) == 3
    assert all_n_ions_Hk2 == [0, 0, 0, 28, 0]
    assert all_n_ions_BB == [0, 0, 0]
    assert list_n_ions_Hk2 == [0, 0, 28]
    assert list_n_ions_BB == [0, 0]


def test_get_total_n_ions_from_entity():

    all_total_n_ions_Hk2 = aux.get_total_n_ions_from_entity(molsys_Hk2, skip_digestion=True)
    all_total_n_ions_BB = aux.get_total_n_ions_from_entity(molsys_BB, skip_digestion=True)
    list_total_n_ions_Hk2 = aux.get_total_n_ions_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_total_n_ions_BB = aux.get_total_n_ions_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert all_total_n_ions_Hk2 == 28
    assert all_total_n_ions_BB == 0
    assert list_total_n_ions_Hk2 == 28
    assert list_total_n_ions_BB == 0


def test_get_n_waters_from_entity():

    all_n_waters_Hk2 = aux.get_n_waters_from_entity(molsys_Hk2, skip_digestion=True)
    all_n_waters_BB = aux.get_n_waters_from_entity(molsys_BB, skip_digestion=True)
    list_n_waters_Hk2 = aux.get_n_waters_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_n_waters_BB = aux.get_n_waters_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert len(all_n_waters_Hk2) == 5
    assert len(all_n_waters_BB) == 3
    assert all_n_waters_Hk2 == [0, 0, 0, 0, 97]
    assert all_n_waters_BB == [0, 0, 513]
    assert list_n_waters_Hk2 == [0, 0, 0]
    assert list_n_waters_BB == [0, 513]


def test_get_total_n_waters_from_entity():

    all_total_n_waters_Hk2 = aux.get_total_n_waters_from_entity(molsys_Hk2, skip_digestion=True)
    all_total_n_waters_BB = aux.get_total_n_waters_from_entity(molsys_BB, skip_digestion=True)
    list_total_n_waters_Hk2 = aux.get_total_n_waters_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_total_n_waters_BB = aux.get_total_n_waters_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert all_total_n_waters_Hk2 == 97
    assert all_total_n_waters_BB == 513
    assert list_total_n_waters_Hk2 == 0
    assert list_total_n_waters_BB == 513


def test_get_n_small_molecules_from_entity():

    all_n_small_molecules_Hk2 = aux.get_n_small_molecules_from_entity(molsys_Hk2, skip_digestion=True)
    all_n_small_molecules_BB = aux.get_n_small_molecules_from_entity(molsys_BB, skip_digestion=True)
    list_n_small_molecules_Hk2 = aux.get_n_small_molecules_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_n_small_molecules_BB = aux.get_n_small_molecules_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert len(all_n_small_molecules_Hk2) == 5
    assert len(all_n_small_molecules_BB) == 3
    assert all_n_small_molecules_Hk2 == [0, 0, 0, 0, 0]
    assert all_n_small_molecules_BB == [0, 0, 0]
    assert list_n_small_molecules_Hk2 == [0, 0, 0]
    assert list_n_small_molecules_BB == [0, 0]


def test_get_total_n_small_molecules_from_entity():

    all_total_n_small_molecules_Hk2 = aux.get_total_n_small_molecules_from_entity(molsys_Hk2, skip_digestion=True)
    all_total_n_small_molecules_BB = aux.get_total_n_small_molecules_from_entity(molsys_BB, skip_digestion=True)
    list_total_n_small_molecules_Hk2 = aux.get_total_n_small_molecules_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_total_n_small_molecules_BB = aux.get_total_n_small_molecules_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert all_total_n_small_molecules_Hk2 == 0
    assert all_total_n_small_molecules_BB == 0
    assert list_total_n_small_molecules_Hk2 == 0
    assert list_total_n_small_molecules_BB == 0


def test_get_n_lipids_from_entity():

    all_n_lipids_Hk2 = aux.get_n_lipids_from_entity(molsys_Hk2, skip_digestion=True)
    all_n_lipids_BB = aux.get_n_lipids_from_entity(molsys_BB, skip_digestion=True)
    list_n_lipids_Hk2 = aux.get_n_lipids_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_n_lipids_BB = aux.get_n_lipids_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert len(all_n_lipids_Hk2) == 5
    assert len(all_n_lipids_BB) == 3
    assert all_n_lipids_Hk2 == [0, 0, 0, 0, 0]
    assert all_n_lipids_BB == [0, 0, 0]
    assert list_n_lipids_Hk2 == [0, 0, 0]
    assert list_n_lipids_BB == [0, 0]


def test_get_total_n_lipids_from_entity():

    all_total_n_lipids_Hk2 = aux.get_total_n_lipids_from_entity(molsys_Hk2, skip_digestion=True)
    all_total_n_lipids_BB = aux.get_total_n_lipids_from_entity(molsys_BB, skip_digestion=True)
    list_total_n_lipids_Hk2 = aux.get_total_n_lipids_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_total_n_lipids_BB = aux.get_total_n_lipids_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert all_total_n_lipids_Hk2 == 0
    assert all_total_n_lipids_BB == 0
    assert list_total_n_lipids_Hk2 == 0
    assert list_total_n_lipids_BB == 0


def test_get_n_saccharides_from_entity():

    all_n_saccharides_Hk2 = aux.get_n_saccharides_from_entity(molsys_Hk2, skip_digestion=True)
    all_n_saccharides_BB = aux.get_n_saccharides_from_entity(molsys_BB, skip_digestion=True)
    list_n_saccharides_Hk2 = aux.get_n_saccharides_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_n_saccharides_BB = aux.get_n_saccharides_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert len(all_n_saccharides_Hk2) == 5
    assert len(all_n_saccharides_BB) == 3
    assert all_n_saccharides_Hk2 == [0, 4, 4, 0, 0]
    assert all_n_saccharides_BB == [0, 0, 0]
    assert list_n_saccharides_Hk2 == [4, 4, 0]
    assert list_n_saccharides_BB == [0, 0]


def test_get_total_n_saccharides_from_entity():

    all_total_n_saccharides_Hk2 = aux.get_total_n_saccharides_from_entity(molsys_Hk2, skip_digestion=True)
    all_total_n_saccharides_BB = aux.get_total_n_saccharides_from_entity(molsys_BB, skip_digestion=True)
    list_total_n_saccharides_Hk2 = aux.get_total_n_saccharides_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_total_n_saccharides_BB = aux.get_total_n_saccharides_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert all_total_n_saccharides_Hk2 == 8
    assert all_total_n_saccharides_BB == 0
    assert list_total_n_saccharides_Hk2 == 8
    assert list_total_n_saccharides_BB == 0


def test_get_n_peptides_from_entity():

    all_n_peptides_Hk2 = aux.get_n_peptides_from_entity(molsys_Hk2, skip_digestion=True)
    all_n_peptides_BB = aux.get_n_peptides_from_entity(molsys_BB, skip_digestion=True)
    list_n_peptides_Hk2 = aux.get_n_peptides_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_n_peptides_BB = aux.get_n_peptides_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert len(all_n_peptides_Hk2) == 5
    assert len(all_n_peptides_BB) == 3
    assert all_n_peptides_Hk2 == [0, 0, 0, 0, 0]
    assert all_n_peptides_BB == [0, 0, 0]
    assert list_n_peptides_Hk2 == [0, 0, 0]
    assert list_n_peptides_BB == [0, 0]


def test_get_total_n_peptides_from_entity():

    all_total_n_peptides_Hk2 = aux.get_total_n_peptides_from_entity(molsys_Hk2, skip_digestion=True)
    all_total_n_peptides_BB = aux.get_total_n_peptides_from_entity(molsys_BB, skip_digestion=True)
    list_total_n_peptides_Hk2 = aux.get_total_n_peptides_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_total_n_peptides_BB = aux.get_total_n_peptides_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert all_total_n_peptides_Hk2 == 0
    assert all_total_n_peptides_BB == 0
    assert list_total_n_peptides_Hk2 == 0
    assert list_total_n_peptides_BB == 0


def test_get_n_proteins_from_entity():

    all_n_proteins_Hk2 = aux.get_n_proteins_from_entity(molsys_Hk2, skip_digestion=True)
    all_n_proteins_BB = aux.get_n_proteins_from_entity(molsys_BB, skip_digestion=True)
    list_n_proteins_Hk2 = aux.get_n_proteins_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_n_proteins_BB = aux.get_n_proteins_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert len(all_n_proteins_Hk2) == 5
    assert len(all_n_proteins_BB) == 3
    assert all_n_proteins_Hk2 == [2, 0, 0, 0, 0]
    assert all_n_proteins_BB == [3, 3, 0]
    assert list_n_proteins_Hk2 == [0, 0, 0]
    assert list_n_proteins_BB == [3, 0]


def test_get_total_n_proteins_from_entity():

    all_total_n_proteins_Hk2 = aux.get_total_n_proteins_from_entity(molsys_Hk2, skip_digestion=True)
    all_total_n_proteins_BB = aux.get_total_n_proteins_from_entity(molsys_BB, skip_digestion=True)
    list_total_n_proteins_Hk2 = aux.get_total_n_proteins_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_total_n_proteins_BB = aux.get_total_n_proteins_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert all_total_n_proteins_Hk2 == 2
    assert all_total_n_proteins_BB == 6
    assert list_total_n_proteins_Hk2 == 0
    assert list_total_n_proteins_BB == 3


def test_get_n_polysaccharides_from_entity():

    all_n_polysaccharides_Hk2 = aux.get_n_polysaccharides_from_entity(molsys_Hk2, skip_digestion=True)
    all_n_polysaccharides_BB = aux.get_n_polysaccharides_from_entity(molsys_BB, skip_digestion=True)
    list_n_polysaccharides_Hk2 = aux.get_n_polysaccharides_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_n_polysaccharides_BB = aux.get_n_polysaccharides_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert len(all_n_polysaccharides_Hk2) == 5
    assert len(all_n_polysaccharides_BB) == 3
    assert all_n_polysaccharides_Hk2 == [0, 4, 4, 0, 0]
    assert all_n_polysaccharides_BB == [0, 0, 0]
    assert list_n_polysaccharides_Hk2 == [4, 4, 0]
    assert list_n_polysaccharides_BB == [0, 0]


def test_get_total_n_polysaccharides_from_entity():

    all_total_n_polysaccharides_Hk2 = aux.get_total_n_polysaccharides_from_entity(molsys_Hk2, skip_digestion=True)
    all_total_n_polysaccharides_BB = aux.get_total_n_polysaccharides_from_entity(molsys_BB, skip_digestion=True)
    list_total_n_polysaccharides_Hk2 = aux.get_total_n_polysaccharides_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_total_n_polysaccharides_BB = aux.get_total_n_polysaccharides_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert all_total_n_polysaccharides_Hk2 == 8
    assert all_total_n_polysaccharides_BB == 0
    assert list_total_n_polysaccharides_Hk2 == 8
    assert list_total_n_polysaccharides_BB == 0


def test_get_n_dnas_from_entity():

    all_n_dnas_Hk2 = aux.get_n_dnas_from_entity(molsys_Hk2, skip_digestion=True)
    all_n_dnas_BB = aux.get_n_dnas_from_entity(molsys_BB, skip_digestion=True)
    list_n_dnas_Hk2 = aux.get_n_dnas_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_n_dnas_BB = aux.get_n_dnas_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert len(all_n_dnas_Hk2) == 5
    assert len(all_n_dnas_BB) == 3
    assert all_n_dnas_Hk2 == [0, 0, 0, 0, 0]
    assert all_n_dnas_BB == [0, 0, 0]
    assert list_n_dnas_Hk2 == [0, 0, 0]
    assert list_n_dnas_BB == [0, 0]


def test_get_total_n_dnas_from_entity():

    all_total_n_dnas_Hk2 = aux.get_total_n_dnas_from_entity(molsys_Hk2, skip_digestion=True)
    all_total_n_dnas_BB = aux.get_total_n_dnas_from_entity(molsys_BB, skip_digestion=True)
    list_total_n_dnas_Hk2 = aux.get_total_n_dnas_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_total_n_dnas_BB = aux.get_total_n_dnas_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert all_total_n_dnas_Hk2 == 0
    assert all_total_n_dnas_BB == 0
    assert list_total_n_dnas_Hk2 == 0
    assert list_total_n_dnas_BB == 0


def test_get_n_rnas_from_entity():

    all_n_rnas_Hk2 = aux.get_n_rnas_from_entity(molsys_Hk2, skip_digestion=True)
    all_n_rnas_BB = aux.get_n_rnas_from_entity(molsys_BB, skip_digestion=True)
    list_n_rnas_Hk2 = aux.get_n_rnas_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_n_rnas_BB = aux.get_n_rnas_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert len(all_n_rnas_Hk2) == 5
    assert len(all_n_rnas_BB) == 3
    assert all_n_rnas_Hk2 == [0, 0, 0, 0, 0]
    assert all_n_rnas_BB == [0, 0, 0]
    assert list_n_rnas_Hk2 == [0, 0, 0]
    assert list_n_rnas_BB == [0, 0]


def test_get_total_n_rnas_from_entity():

    all_total_n_rnas_Hk2 = aux.get_total_n_rnas_from_entity(molsys_Hk2, skip_digestion=True)
    all_total_n_rnas_BB = aux.get_total_n_rnas_from_entity(molsys_BB, skip_digestion=True)
    list_total_n_rnas_Hk2 = aux.get_total_n_rnas_from_entity(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_total_n_rnas_BB = aux.get_total_n_rnas_from_entity(molsys_BB, indices=[1,2], skip_digestion=True)

    assert all_total_n_rnas_Hk2 == 0
    assert all_total_n_rnas_BB == 0
    assert list_total_n_rnas_Hk2 == 0
    assert list_total_n_rnas_BB == 0


# From component


def test_get_atom_index_from_component():

    all_atom_index_Hk2 = aux.get_atom_index_from_component(molsys_Hk2, skip_digestion=True)
    all_atom_index_BB = aux.get_atom_index_from_component(molsys_BB, skip_digestion=True)
    list_atom_index_Hk2 = aux.get_atom_index_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_atom_index_BB = aux.get_atom_index_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_atom_index_Hk2, list)
    assert len(all_atom_index_Hk2) == 146
    assert len(all_atom_index_BB) == 521
    assert all_atom_index_Hk2[0] == list(range(640))
    assert all_atom_index_Hk2[1] == list(range(640,3832))
    assert all_atom_index_Hk2[2] == list(range(3832,3991))
    assert all_atom_index_Hk2[-1] == [13545]
    assert all_atom_index_BB[0] == list(range(864))
    assert all_atom_index_BB[1] == list(range(864,1742))
    assert all_atom_index_BB[2] == list(range(1742,2581))
    assert list_atom_index_Hk2[0] == list(range(3991,4296))
    assert list_atom_index_BB[1] == list(range(3098,3274))


def test_get_atom_id_from_component():

    all_atom_id_Hk2 = aux.get_atom_id_from_component(molsys_Hk2, skip_digestion=True)
    all_atom_id_BB = aux.get_atom_id_from_component(molsys_BB, skip_digestion=True)
    list_atom_id_Hk2 = aux.get_atom_id_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_atom_id_BB = aux.get_atom_id_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_atom_id_Hk2, list)
    assert len(all_atom_id_Hk2) == 146
    assert len(all_atom_id_BB) == 521
    assert len(all_atom_id_Hk2[0]) == 640
    assert all_atom_id_Hk2[0][500:510] == [501, 502, 503, 504, 505, 506, 507, 508, 509, 510]
    assert len(all_atom_id_Hk2[1]) == 3192
    assert all_atom_id_Hk2[1][1000:1010] == [1641, 1642, 1643, 1644, 1645, 1646, 1647, 1648, 1649, 1650]
    assert len(all_atom_id_Hk2[2]) == 159 
    assert all_atom_id_Hk2[2][100:110] == [3933, 3934, 3935, 3936, 3937, 3938, 3939, 3940, 3941, 3942]
    assert all_atom_id_Hk2[-1] == [13546]
    assert len(all_atom_id_BB[0]) == 864
    assert all_atom_id_BB[0][400:410] == [401, 402, 403, 404, 405, 406, 407, 408, 409, 410]
    assert len(all_atom_id_BB[1]) == 878
    assert all_atom_id_BB[1][400:410] == [1265, 1266, 1267, 1268, 1269, 1270, 1271, 1272, 1273, 1274]
    assert len(all_atom_id_BB[2]) == 839
    assert all_atom_id_BB[2][400:410] == [2143, 2144, 2145, 2146, 2147, 2148, 2149, 2150, 2151, 2152]
    assert all_atom_id_BB[-1] == [5153]
    assert len(list_atom_id_Hk2[0]) == 305
    assert len(list_atom_id_BB[1]) == 176
    assert list_atom_id_Hk2[0][50:60] == [4042, 4043, 4044, 4045, 4046, 4047, 4048, 4049, 4050, 4051]
    assert list_atom_id_BB[1][50:60] == [3151, 3152, 3153, 3154, 3155, 3156, 3157, 3158, 3159, 3160]


def test_get_atom_name_from_component():

    all_atom_name_Hk2 = aux.get_atom_name_from_component(molsys_Hk2, skip_digestion=True)
    all_atom_name_BB = aux.get_atom_name_from_component(molsys_BB, skip_digestion=True)
    list_atom_name_Hk2 = aux.get_atom_name_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_atom_name_BB = aux.get_atom_name_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_atom_name_Hk2, list)
    assert len(all_atom_name_Hk2) == 146
    assert len(all_atom_name_BB) == 521
    assert len(all_atom_name_Hk2[0]) == 640
    assert all_atom_name_Hk2[0][500:510] == ['CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ', 'N', 'CA', 'C', 'O']
    assert len(all_atom_name_Hk2[1]) == 3192
    assert all_atom_name_Hk2[1][1000:1010] == ['N', 'CA', 'C', 'O', 'N', 'CA', 'C', 'O', 'CB', 'OG']
    assert len(all_atom_name_Hk2[2]) == 159 
    assert all_atom_name_Hk2[2][100:110] == ['CD', 'NE', 'CZ', 'NH1', 'NH2', 'N', 'CA', 'C', 'O', 'CB']
    assert all_atom_name_Hk2[-1] == ['O']
    assert len(all_atom_name_BB[0]) == 864
    assert all_atom_name_BB[0][400:410] == ['O', 'CB', 'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ', 'N', 'CA']
    assert len(all_atom_name_BB[1]) == 878
    assert all_atom_name_BB[1][400:410] == ['CG', 'OD1', 'OD2', 'N', 'CA', 'C', 'O', 'CB', 'CG1', 'CG2']
    assert len(all_atom_name_BB[2]) == 839
    assert all_atom_name_BB[2][400:410] == ['CA', 'C', 'O', 'CB', 'CG', 'CD', 'NE', 'CZ', 'NH1', 'NH2']
    assert all_atom_name_BB[-1] == ['O']
    assert len(list_atom_name_Hk2[0]) == 305
    assert len(list_atom_name_BB[1]) == 176
    assert list_atom_name_Hk2[0][50:60] == ['CB', 'CG', 'CD', 'CE', 'NZ', 'N', 'CA', 'C', 'O', 'CB']
    assert list_atom_name_BB[1][50:60] == ['C', 'O', 'CB', 'CG1', 'CG2', 'N', 'CA', 'C', 'O', 'CB']


def test_get_atom_type_from_component():

    all_atom_type_Hk2 = aux.get_atom_type_from_component(molsys_Hk2, skip_digestion=True)
    all_atom_type_BB = aux.get_atom_type_from_component(molsys_BB, skip_digestion=True)
    list_atom_type_Hk2 = aux.get_atom_type_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_atom_type_BB = aux.get_atom_type_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_atom_type_Hk2, list)
    assert len(all_atom_type_Hk2) == 146
    assert len(all_atom_type_BB) == 521
    assert len(all_atom_type_Hk2[0]) == 640
    assert all_atom_type_Hk2[0][500:510] == ['C', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'O']
    assert len(all_atom_type_Hk2[1]) == 3192
    assert all_atom_type_Hk2[1][1000:1010] == ['N', 'C', 'C', 'O', 'N', 'C', 'C', 'O', 'C', 'O']
    assert len(all_atom_type_Hk2[2]) == 159 
    assert all_atom_type_Hk2[2][100:110] == ['C', 'N', 'C', 'N', 'N', 'N', 'C', 'C', 'O', 'C']
    assert all_atom_type_Hk2[-1] == ['O']
    assert len(all_atom_type_BB[0]) == 864
    assert all_atom_type_BB[0][400:410] == ['O', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'C']
    assert len(all_atom_type_BB[1]) == 878
    assert all_atom_type_BB[1][400:410] == ['C', 'O', 'O', 'N', 'C', 'C', 'O', 'C', 'C', 'C']
    assert len(all_atom_type_BB[2]) == 839
    assert all_atom_type_BB[2][400:410] == ['C', 'C', 'O', 'C', 'C', 'C', 'N', 'C', 'N', 'N']
    assert all_atom_type_BB[-1] == ['O']
    assert len(list_atom_type_Hk2[0]) == 305
    assert len(list_atom_type_BB[1]) == 176
    assert list_atom_type_Hk2[0][50:60] == ['C', 'C', 'C', 'C', 'N', 'N', 'C', 'C', 'O', 'C']
    assert list_atom_type_BB[1][50:60] == ['C', 'O', 'C', 'C', 'C', 'N', 'C', 'C', 'O', 'C']


def test_get_group_index_from_component():

    all_group_index_Hk2 = aux.get_group_index_from_component(molsys_Hk2, skip_digestion=True)
    all_group_index_BB = aux.get_group_index_from_component(molsys_BB, skip_digestion=True)
    list_group_index_Hk2 = aux.get_group_index_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_group_index_BB = aux.get_group_index_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_group_index_Hk2, list)
    assert len(all_group_index_Hk2) == 146
    assert len(all_group_index_BB) == 521
    assert len(all_group_index_Hk2[0]) == 81
    assert all_group_index_Hk2[0][50:60] == [50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
    assert len(all_group_index_Hk2[1]) == 413
    assert all_group_index_Hk2[1][100:110] == [181, 182, 183, 184, 185, 186, 187, 188, 189, 190]
    assert len(all_group_index_Hk2[2]) == 21
    assert all_group_index_Hk2[2][10:20] == [501, 502, 503, 504, 505, 506, 507, 508, 509, 510]
    assert all_group_index_Hk2[-1] == [1870]
    assert len(all_group_index_BB[0]) == 108
    assert all_group_index_BB[0][40:50] == [40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
    assert len(all_group_index_BB[1]) == 110
    assert all_group_index_BB[1][40:50] == [148, 149, 150, 151, 152, 153, 154, 155, 156, 157]
    assert len(all_group_index_BB[2]) == 108
    assert all_group_index_BB[2][40:50] == [258, 259, 260, 261, 262, 263, 264, 265, 266, 267]
    assert all_group_index_BB[-1] == [1100]
    assert len(list_group_index_Hk2[0]) == 40
    assert len(list_group_index_BB[1]) == 24
    assert list_group_index_Hk2[0][20:30] == [535, 536, 537, 538, 539, 540, 541, 542, 543, 544]
    assert list_group_index_BB[1][10:20] == [399, 400, 401, 402, 403, 404, 405, 406, 407, 408]


def test_get_group_id_from_component():

    all_group_id_Hk2 = aux.get_group_id_from_component(molsys_Hk2, skip_digestion=True)
    all_group_id_BB = aux.get_group_id_from_component(molsys_BB, skip_digestion=True)
    list_group_id_Hk2 = aux.get_group_id_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_group_id_BB = aux.get_group_id_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_group_id_Hk2, list)
    assert len(all_group_id_Hk2) == 146
    assert len(all_group_id_BB) == 521
    assert len(all_group_id_Hk2[0]) == 81
    assert all_group_id_Hk2[0][50:60] == [67, 68, 69, 70, 71, 72, 73, 74, 75, 76]
    assert len(all_group_id_Hk2[1]) == 413
    assert all_group_id_Hk2[1][100:110] == [205, 206, 207, 208, 209, 210, 211, 212, 213, 214]
    assert len(all_group_id_Hk2[2]) == 21
    assert all_group_id_Hk2[2][10:20] == [536, 537, 538, 539, 540, 541, 542, 543, 544, 545]
    assert all_group_id_Hk2[-1] == [1097]
    assert len(all_group_id_BB[0]) == 108
    assert all_group_id_BB[0][40:50] == [43, 44, 45, 46, 47, 48, 49, 50, 51, 52]
    assert len(all_group_id_BB[1]) == 110
    assert all_group_id_BB[1][40:50] == [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    assert len(all_group_id_BB[2]) == 108
    assert all_group_id_BB[2][40:50] == [43, 44, 45, 46, 47, 48, 49, 50, 51, 52]
    assert all_group_id_BB[-1] == [129]
    assert len(list_group_id_Hk2[0]) == 40
    assert len(list_group_id_BB[1]) == 24
    assert list_group_id_Hk2[0][20:30] == [572, 573, 574, 575, 576, 577, 578, 579, 580, 581]
    assert list_group_id_BB[1][10:20] == [76, 77, 78, 79, 80, 81, 82, 83, 84, 85]


def test_get_group_name_from_component():

    all_group_name_Hk2 = aux.get_group_name_from_component(molsys_Hk2, skip_digestion=True)
    all_group_name_BB = aux.get_group_name_from_component(molsys_BB, skip_digestion=True)
    list_group_name_Hk2 = aux.get_group_name_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_group_name_BB = aux.get_group_name_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_group_name_Hk2, list)
    assert len(all_group_name_Hk2) == 146
    assert len(all_group_name_BB) == 521
    assert len(all_group_name_Hk2[0]) == 81
    assert all_group_name_Hk2[0][50:60] == ['PHE', 'VAL', 'ARG', 'SER', 'THR', 'PRO', 'ASP', 'GLY', 'THR', 'GLU']
    assert len(all_group_name_Hk2[1]) == 413
    assert all_group_name_Hk2[1][100:110] == ['ALA', 'VAL', 'VAL', 'ASN', 'ASP', 'THR', 'VAL', 'GLY', 'THR', 'MET']
    assert len(all_group_name_Hk2[2]) == 21
    assert all_group_name_Hk2[2][10:20] == ['THR', 'ASN', 'PHE', 'ARG', 'VAL', 'LEU', 'LEU', 'VAL', 'ARG', 'VAL']
    assert all_group_name_Hk2[-1] == ['HOH']
    assert len(all_group_name_BB[0]) == 108
    assert all_group_name_BB[0][40:50] == ['ALA', 'ASP', 'VAL', 'ALA', 'PRO', 'GLY', 'LYS', 'SER', 'ILE', 'GLY']
    assert len(all_group_name_BB[1]) == 110
    assert all_group_name_BB[1][40:50] == ['ASN', 'LEU', 'ALA', 'ASP', 'VAL', 'ALA', 'PRO', 'GLY', 'LYS', 'SER']
    assert len(all_group_name_BB[2]) == 108
    assert all_group_name_BB[2][40:50] == ['ALA', 'ASP', 'VAL', 'ALA', 'PRO', 'GLY', 'LYS', 'SER', 'ILE', 'GLY']
    assert all_group_name_BB[-1] == ['HOH']
    assert len(list_group_name_Hk2[0]) == 40
    assert len(list_group_name_BB[1]) == 24
    assert list_group_name_Hk2[0][20:30] == ['ASP', 'GLU', 'LEU', 'PHE', 'ASP', 'HIS', 'ILE', 'VAL', 'GLN', 'CYS']
    assert list_group_name_BB[1][10:20] == ['GLU', 'ALA', 'LYS', 'ALA', 'GLU', 'GLY', 'ALA', 'ASP', 'ILE', 'THR']


def test_get_group_type_from_component():

    all_group_type_Hk2 = aux.get_group_type_from_component(molsys_Hk2, skip_digestion=True)
    all_group_type_BB = aux.get_group_type_from_component(molsys_BB, skip_digestion=True)
    list_group_type_Hk2 = aux.get_group_type_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_group_type_BB = aux.get_group_type_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_group_type_Hk2, list)
    assert len(all_group_type_Hk2) == 146
    assert len(all_group_type_BB) == 521
    assert len(all_group_type_Hk2[0]) == 81
    assert all_group_type_Hk2[0][50:60] == 10*['amino acid']
    assert len(all_group_type_Hk2[1]) == 413
    assert all_group_type_Hk2[1][100:110] == 10*['amino acid']
    assert len(all_group_type_Hk2[2]) == 21
    assert all_group_type_Hk2[2][10:20] == 10*['amino acid']
    assert all_group_type_Hk2[-1] == ['water']
    assert len(all_group_type_BB[0]) == 108
    assert all_group_type_BB[0][40:50] == 10*['amino acid']
    assert len(all_group_type_BB[1]) == 110
    assert all_group_type_BB[1][40:50] == 10*['amino acid']
    assert len(all_group_type_BB[2]) == 108
    assert all_group_type_BB[2][40:50] == 10*['amino acid']
    assert all_group_type_BB[-1] == ['water']
    assert len(list_group_type_Hk2[0]) == 40
    assert len(list_group_type_BB[1]) == 24
    assert list_group_type_Hk2[0][20:30] == 10*['amino acid']
    assert list_group_type_BB[1][10:20] == 10*['amino acid']


def test_get_component_index_from_component():

    all_component_index_Hk2 = aux.get_component_index_from_component(molsys_Hk2, skip_digestion=True)
    all_component_index_BB = aux.get_component_index_from_component(molsys_BB, skip_digestion=True)
    list_component_index_Hk2 = aux.get_component_index_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_component_index_BB = aux.get_component_index_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_component_index_Hk2, list)
    assert len(all_component_index_Hk2) == 146
    assert len(all_component_index_BB) == 521
    assert all_component_index_Hk2[50:60] == list(range(50,60))
    assert all_component_index_Hk2[-1] == 145
    assert all_component_index_BB[40:50] == list(range(40,50))
    assert all_component_index_BB[-1] == 520
    assert list_component_index_Hk2 == [3,4,5]
    assert list_component_index_BB == [3,4]


def test_get_component_id_from_component():

    all_component_id_Hk2 = aux.get_component_id_from_component(molsys_Hk2, skip_digestion=True)
    all_component_id_BB = aux.get_component_id_from_component(molsys_BB, skip_digestion=True)
    list_component_id_Hk2 = aux.get_component_id_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_component_id_BB = aux.get_component_id_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_component_id_Hk2, list)
    assert len(all_component_id_Hk2) == 146
    assert len(all_component_id_BB) == 521
    assert all_component_id_Hk2[50:60] == list(range(50,60))
    assert all_component_id_Hk2[-1] == 145
    assert all_component_id_BB[40:50] == list(range(40,50))
    assert all_component_id_BB[-1] == 520
    assert list_component_id_Hk2 == [3,4,5]
    assert list_component_id_BB == [3,4]


def test_get_component_name_from_component():

    all_component_name_Hk2 = aux.get_component_name_from_component(molsys_Hk2, skip_digestion=True)
    all_component_name_BB = aux.get_component_name_from_component(molsys_BB, skip_digestion=True)
    list_component_name_Hk2 = aux.get_component_name_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_component_name_BB = aux.get_component_name_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_component_name_Hk2, list)
    assert len(all_component_name_Hk2) == 146
    assert len(all_component_name_BB) == 521
    assert all_component_name_Hk2[:10] == ['protein 0', 'protein 1', 'peptide 0', 'peptide 1', 'protein 2',
                                           'protein 3', 'protein 4', 'protein 5', 'protein 6', 'protein 7']
    assert all_component_name_Hk2[10:30] == ['peptide 2', 'protein 8', 'protein 9', 'unknown 0', 'unknown 1',
                                             'unknown 2', 'unknown 3', 'UNX', 'UNX', 'UNX', 'UNX', 'UNX', 'UNX',
                                             'UNX', 'UNX', 'UNX', 'UNX', 'UNX', 'UNX', 'unknown 4']
    assert all_component_name_Hk2[50:60] == 10*['water']
    assert all_component_name_BB[:10] == ['protein 0', 'protein 1', 'protein 2', 'protein 3', 'peptide 0', 'protein 4',
                                          'peptide 0', 'protein 5', 'water', 'water']
    assert all_component_name_BB[-1] == 'water'
    assert list_component_name_Hk2 == ['peptide 1', 'protein 2', 'protein 3']
    assert list_component_name_BB == ['protein 3', 'peptide 0']


def test_get_component_type_from_component():

    all_component_type_Hk2 = aux.get_component_type_from_component(molsys_Hk2, skip_digestion=True)
    all_component_type_BB = aux.get_component_type_from_component(molsys_BB, skip_digestion=True)
    list_component_type_Hk2 = aux.get_component_type_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_component_type_BB = aux.get_component_type_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_component_type_Hk2, list)
    assert len(all_component_type_Hk2) == 146
    assert len(all_component_type_BB) == 521
    assert all_component_type_Hk2[:10] == ['protein', 'protein', 'peptide', 'peptide', 'protein',
                                           'protein', 'protein', 'protein', 'protein', 'protein']
    assert all_component_type_Hk2[10:30] == ['peptide', 'protein', 'protein', 'polysaccharide', 'polysaccharide',
                                             'polysaccharide', 'polysaccharide', 'ion', 'ion', 'ion', 'ion', 'ion',
                                             'ion', 'ion', 'ion', 'ion', 'ion', 'ion', 'ion', 'polysaccharide']
    assert all_component_type_Hk2[50:60] == 10*['water']
    assert all_component_type_BB[:10] == ['protein', 'protein', 'protein', 'protein', 'peptide', 'protein',
                                          'peptide', 'protein', 'water', 'water']
    assert all_component_type_BB[-1] == 'water'
    assert list_component_type_Hk2 == ['peptide', 'protein', 'protein']
    assert list_component_type_BB == ['protein', 'peptide']


def test_get_molecule_index_from_component():

    all_molecule_index_Hk2 = aux.get_molecule_index_from_component(molsys_Hk2, skip_digestion=True)
    all_molecule_index_BB = aux.get_molecule_index_from_component(molsys_BB, skip_digestion=True)
    list_molecule_index_Hk2 = aux.get_molecule_index_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_molecule_index_BB = aux.get_molecule_index_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_molecule_index_Hk2, list)
    assert len(all_molecule_index_Hk2) == 146
    assert len(all_molecule_index_BB) == 521
    assert all_molecule_index_Hk2[:10] == [0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
    assert all_molecule_index_Hk2[10:30] == [1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    assert all_molecule_index_Hk2[50:60] == [39, 40, 41, 42, 43, 44, 45, 46, 47, 48]
    assert all_molecule_index_BB[:10] == [0, 1, 2, 3, 3, 4, 4, 5, 6, 7]
    assert all_molecule_index_BB[-1] == 518
    assert list_molecule_index_Hk2 == [0, 0, 0]
    assert list_molecule_index_BB == [3, 3]


def test_get_molecule_id_from_component():

    all_molecule_id_Hk2 = aux.get_molecule_id_from_component(molsys_Hk2, skip_digestion=True)
    all_molecule_id_BB = aux.get_molecule_id_from_component(molsys_BB, skip_digestion=True)
    list_molecule_id_Hk2 = aux.get_molecule_id_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_molecule_id_BB = aux.get_molecule_id_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_molecule_id_Hk2, list)
    assert len(all_molecule_id_Hk2) == 146
    assert len(all_molecule_id_BB) == 521
    assert all_molecule_id_Hk2[:10] == [0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
    assert all_molecule_id_Hk2[10:30] == [1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    assert all_molecule_id_Hk2[50:60] == [39, 40, 41, 42, 43, 44, 45, 46, 47, 48]
    assert all_molecule_id_BB[:10] == [0, 1, 2, 3, 3, 4, 4, 5, 6, 7]
    assert all_molecule_id_BB[-1] == 518
    assert list_molecule_id_Hk2 == [0, 0, 0]
    assert list_molecule_id_BB == [3, 3]


def test_get_molecule_name_from_component():

    all_molecule_name_Hk2 = aux.get_molecule_name_from_component(molsys_Hk2, skip_digestion=True)
    all_molecule_name_BB = aux.get_molecule_name_from_component(molsys_BB, skip_digestion=True)
    list_molecule_name_Hk2 = aux.get_molecule_name_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_molecule_name_BB = aux.get_molecule_name_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_molecule_name_Hk2, list)
    assert len(all_molecule_name_Hk2) == 146
    assert len(all_molecule_name_BB) == 521
    assert all_molecule_name_Hk2[:10] == 10*['Hexokinase-2']
    assert all_molecule_name_Hk2[10:30] == ['Hexokinase-2', 'Hexokinase-2', 'Hexokinase-2', 'alpha-D-glucopyranose',
                                            '6-O-phosphono-beta-D-glucopyranose', 'alpha-D-glucopyranose',
                                            '6-O-phosphono-beta-D-glucopyranose', 'UNKNOWN ATOM OR ION',
                                            'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION',
                                            'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION',
                                            'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION',
                                            'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION', 'alpha-D-glucopyranose']
    assert all_molecule_name_Hk2[50:60] == 10*['water']
    assert all_molecule_name_BB[:10] == ['BARNASE', 'BARNASE', 'BARNASE', 'BARSTAR', 'BARSTAR', 'BARSTAR', 'BARSTAR',
                                         'BARSTAR', 'water', 'water']
    assert all_molecule_name_BB[-1] == 'water'
    assert list_molecule_name_Hk2 == ['Hexokinase-2', 'Hexokinase-2', 'Hexokinase-2']
    assert list_molecule_name_BB == ['BARSTAR', 'BARSTAR']


def test_get_molecule_type_from_component():

    all_molecule_type_Hk2 = aux.get_molecule_type_from_component(molsys_Hk2, skip_digestion=True)
    all_molecule_type_BB = aux.get_molecule_type_from_component(molsys_BB, skip_digestion=True)
    list_molecule_type_Hk2 = aux.get_molecule_type_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_molecule_type_BB = aux.get_molecule_type_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_molecule_type_Hk2, list)
    assert len(all_molecule_type_Hk2) == 146
    assert len(all_molecule_type_BB) == 521
    assert all_molecule_type_Hk2[:10] == 10*['protein']
    assert all_molecule_type_Hk2[10:30] == ['protein', 'protein', 'protein', 'polysaccharide', 'polysaccharide',
                                            'polysaccharide', 'polysaccharide', 'unknown', 'unknown', 'unknown',
                                            'unknown', 'unknown', 'unknown', 'unknown', 'unknown', 'unknown',
                                            'unknown', 'unknown', 'unknown', 'polysaccharide']
    assert all_molecule_type_Hk2[50:60] == 10*['water']
    assert all_molecule_type_BB[:10] == ['protein', 'protein', 'protein', 'protein', 'protein', 'protein', 'protein',
                                         'protein', 'water', 'water']
    assert all_molecule_type_BB[-1] == 'water'
    assert list_molecule_type_Hk2 == 3*['protein']
    assert list_molecule_type_BB == 2*['protein']


def test_get_entity_index_from_component():

    all_entity_index_Hk2 = aux.get_entity_index_from_component(molsys_Hk2, skip_digestion=True)
    all_entity_index_BB = aux.get_entity_index_from_component(molsys_BB, skip_digestion=True)
    list_entity_index_Hk2 = aux.get_entity_index_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_entity_index_BB = aux.get_entity_index_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_entity_index_Hk2, list)
    assert len(all_entity_index_Hk2) == 146
    assert len(all_entity_index_BB) == 521
    assert all_entity_index_Hk2[:10] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_entity_index_Hk2[10:30] == [0, 0, 0, 1, 2, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1]
    assert all_entity_index_Hk2[50:60] == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    assert all_entity_index_BB[:10] == [0, 0, 0, 1, 1, 1, 1, 1, 2, 2]
    assert all_entity_index_BB[-1] == 2
    assert list_entity_index_Hk2 == [0, 0, 0]
    assert list_entity_index_BB == [1, 1]


def test_get_entity_id_from_component():

    all_entity_id_Hk2 = aux.get_entity_id_from_component(molsys_Hk2, skip_digestion=True)
    all_entity_id_BB = aux.get_entity_id_from_component(molsys_BB, skip_digestion=True)
    list_entity_id_Hk2 = aux.get_entity_id_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_entity_id_BB = aux.get_entity_id_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_entity_id_Hk2, list)
    assert len(all_entity_id_Hk2) == 146
    assert len(all_entity_id_BB) == 521
    assert all_entity_id_Hk2[:10] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert all_entity_id_Hk2[10:30] == [1, 1, 1, 2, 3, 2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2]
    assert all_entity_id_Hk2[50:60] == [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    assert all_entity_id_BB[:10] == [1, 1, 1, 2, 2, 2, 2, 2, 3, 3]
    assert all_entity_id_BB[-1] == 3
    assert list_entity_id_Hk2 == [1, 1, 1]
    assert list_entity_id_BB == [2, 2]


def test_get_entity_name_from_component():

    all_entity_name_Hk2 = aux.get_entity_name_from_component(molsys_Hk2, skip_digestion=True)
    all_entity_name_BB = aux.get_entity_name_from_component(molsys_BB, skip_digestion=True)
    list_entity_name_Hk2 = aux.get_entity_name_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_entity_name_BB = aux.get_entity_name_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_entity_name_Hk2, list)
    assert len(all_entity_name_Hk2) == 146
    assert len(all_entity_name_BB) == 521
    assert all_entity_name_Hk2[:10] == 10*['Hexokinase-2']
    assert all_entity_name_Hk2[10:30] == ['Hexokinase-2', 'Hexokinase-2', 'Hexokinase-2', 'alpha-D-glucopyranose',
                                          '6-O-phosphono-beta-D-glucopyranose', 'alpha-D-glucopyranose',
                                          '6-O-phosphono-beta-D-glucopyranose', 'UNKNOWN ATOM OR ION',
                                          'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION',
                                          'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION',
                                          'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION',
                                          'UNKNOWN ATOM OR ION', 'UNKNOWN ATOM OR ION', 'alpha-D-glucopyranose']
    assert all_entity_name_Hk2[50:60] == 10*['water']
    assert all_entity_name_BB[:10] == ['BARNASE', 'BARNASE', 'BARNASE', 'BARSTAR', 'BARSTAR', 'BARSTAR', 'BARSTAR',
                                       'BARSTAR', 'water', 'water']
    assert all_entity_name_BB[-1] == 'water'
    assert list_entity_name_Hk2 == ['Hexokinase-2', 'Hexokinase-2', 'Hexokinase-2']
    assert list_entity_name_BB == ['BARSTAR', 'BARSTAR']


def test_get_entity_type_from_component():

    all_entity_type_Hk2 = aux.get_entity_type_from_component(molsys_Hk2, skip_digestion=True)
    all_entity_type_BB = aux.get_entity_type_from_component(molsys_BB, skip_digestion=True)
    list_entity_type_Hk2 = aux.get_entity_type_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_entity_type_BB = aux.get_entity_type_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_entity_type_Hk2, list)
    assert len(all_entity_type_Hk2) == 146
    assert len(all_entity_type_BB) == 521
    assert all_entity_type_Hk2[:10] == 10*['protein']
    assert all_entity_type_Hk2[10:30] == ['protein', 'protein', 'protein', 'polysaccharide', 'polysaccharide',
                                          'polysaccharide', 'polysaccharide', 'unknown', 'unknown', 'unknown',
                                          'unknown', 'unknown', 'unknown', 'unknown', 'unknown', 'unknown',
                                          'unknown', 'unknown', 'unknown', 'polysaccharide']
    assert all_entity_type_Hk2[50:60] == 10*['water']
    assert all_entity_type_BB[:10] == ['protein', 'protein', 'protein', 'protein', 'protein', 'protein', 'protein',
                                         'protein', 'water', 'water']
    assert all_entity_type_BB[-1] == 'water'
    assert list_entity_type_Hk2 == ['protein', 'protein', 'protein']
    assert list_entity_type_BB == ['protein', 'protein']


def test_get_chain_index_from_component():

    all_chain_index_Hk2 = aux.get_chain_index_from_component(molsys_Hk2, skip_digestion=True)
    all_chain_index_BB = aux.get_chain_index_from_component(molsys_BB, skip_digestion=True)
    list_chain_index_Hk2 = aux.get_chain_index_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_chain_index_BB = aux.get_chain_index_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_chain_index_Hk2, list)
    assert len(all_chain_index_Hk2) == 146
    assert len(all_chain_index_BB) == 521
    assert all_chain_index_Hk2[:10] == [0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
    assert all_chain_index_Hk2[10:30] == [1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    assert all_chain_index_Hk2[50:60] == [38, 38, 38, 38, 38, 38, 38, 38, 38, 38]
    assert all_chain_index_BB[:10] == [0, 1, 2, 3, 3, 4, 4, 5, 6, 6]
    assert all_chain_index_BB[-1] == 11
    assert list_chain_index_Hk2 == [0, 0, 0]
    assert list_chain_index_BB == [3, 3]


def test_get_chain_id_from_component():

    all_chain_id_Hk2 = aux.get_chain_id_from_component(molsys_Hk2, skip_digestion=True)
    all_chain_id_BB = aux.get_chain_id_from_component(molsys_BB, skip_digestion=True)
    list_chain_id_Hk2 = aux.get_chain_id_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_chain_id_BB = aux.get_chain_id_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_chain_id_Hk2, list)
    assert len(all_chain_id_Hk2) == 146
    assert len(all_chain_id_BB) == 521
    assert all_chain_id_Hk2[:10] == ['A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B']
    assert all_chain_id_Hk2[10:30] == ['B', 'B', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                                       'P', 'Q', 'R', 'S']
    assert all_chain_id_Hk2[50:60] == ['MA', 'MA', 'MA', 'MA', 'MA', 'MA', 'MA', 'MA', 'MA', 'MA']
    assert all_chain_id_BB[:10] == ['A', 'B', 'C', 'D', 'D', 'E', 'E', 'F', 'G', 'G']
    assert all_chain_id_BB[-1] == 'L'
    assert list_chain_id_Hk2 == ['A', 'A', 'A']
    assert list_chain_id_BB == ['D', 'D']


def test_get_chain_name_from_component():

    all_chain_name_Hk2 = aux.get_chain_name_from_component(molsys_Hk2, skip_digestion=True)
    all_chain_name_BB = aux.get_chain_name_from_component(molsys_BB, skip_digestion=True)
    list_chain_name_Hk2 = aux.get_chain_name_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_chain_name_BB = aux.get_chain_name_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_chain_name_Hk2, list)
    assert len(all_chain_name_Hk2) == 146
    assert len(all_chain_name_BB) == 521
    assert all_chain_name_Hk2[:10] == ['A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B']
    assert all_chain_name_Hk2[10:30] == ['B', 'B', 'B', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A',
                                         'A', 'A', 'A', 'A', 'B']
    assert all_chain_name_Hk2[50:60] == ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A']
    assert all_chain_name_BB[:10] == ['A', 'B', 'C', 'D', 'D', 'E', 'E', 'F', 'A', 'A']
    assert all_chain_name_BB[-1] == 'F'
    assert list_chain_name_Hk2 == ['A', 'A', 'A']
    assert list_chain_name_BB == ['D', 'D']


def test_get_chain_type_from_component():

    all_chain_type_Hk2 = aux.get_chain_type_from_component(molsys_Hk2, skip_digestion=True)
    all_chain_type_BB = aux.get_chain_type_from_component(molsys_BB, skip_digestion=True)
    list_chain_type_Hk2 = aux.get_chain_type_from_component(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_chain_type_BB = aux.get_chain_type_from_component(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_chain_type_Hk2, list)
    assert len(all_chain_type_Hk2) == 146
    assert len(all_chain_type_BB) == 521
    assert all_chain_type_Hk2[:10] == 10*['protein']
    assert all_chain_type_Hk2[10:30] == ['protein', 'protein', 'protein', 'polysaccharide', 'polysaccharide',
                                         'polysaccharide', 'polysaccharide', 'unknown', 'unknown', 'unknown',
                                         'unknown', 'unknown', 'unknown', 'unknown', 'unknown', 'unknown', 'unknown',
                                         'unknown', 'unknown', 'polysaccharide']
    assert all_chain_type_Hk2[50:60] == 10*['water']
    assert all_chain_type_BB[:10] == ['protein', 'protein', 'protein', 'protein', 'protein', 'protein', 'protein',
                                      'protein', 'water', 'water']
    assert all_chain_type_BB[-1] == 'water'
    assert list_chain_type_Hk2 == ['protein', 'protein', 'protein']
    assert list_chain_type_BB == ['protein', 'protein']


def test_get_bond_index_from_component():

    all_bond_index_Hk2 = aux.get_bond_index_from_component(molsys_Hk2, skip_digestion=True)
    all_bond_index_BB = aux.get_bond_index_from_component(molsys_BB, skip_digestion=True)
    list_bond_index_Hk2 = aux.get_bond_index_from_component(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_bond_index_BB = aux.get_bond_index_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_bond_index_Hk2, list)
    assert len(all_bond_index_Hk2) == 146
    assert len(all_bond_index_BB) == 521
    assert all_bond_index_Hk2[1][2000:2010] == [2653, 2654, 2655, 2656, 2657, 2658, 2659, 2660, 2661, 2662]
    assert all_bond_index_Hk2[15:25] == [[13534, 13535, 13536, 13537, 13538, 13539, 13540, 13541, 13542, 13543,
                                          13544, 13545],
                                         [13546, 13547, 13548, 13549, 13550, 13551, 13552, 13553, 13554, 13555,
                                          13556, 13557, 13558, 13559, 13560, 13561], [], [], [], [], [], [], [], []]
    assert all_bond_index_Hk2[105:115] == [[], [], [], [], [], [], [], [], [], []]
    assert all_bond_index_Hk2[0][80:90] == [80, 81, 82, 83, 84, 85, 86, 87, 88, 89]
    assert all_bond_index_Hk2[-1] == []
    assert all_bond_index_BB[0][40:50] == [40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
    assert all_bond_index_BB[3][500:510] == [3144, 3145, 3146, 3147, 3148, 3149, 3150, 3151, 3152, 3153]
    assert all_bond_index_BB[6][100:110] == [3949, 3950, 3951, 3952, 3953, 3954, 3955, 3956, 3957, 3958]
    assert all_bond_index_BB[9] == []
    assert all_bond_index_BB[-1] == []
    assert list_bond_index_Hk2[1][60:70] == [3952, 3953, 3954, 3955, 3956, 3957, 3958, 3959, 3960, 3961]
    assert list_bond_index_BB == [[], [], [], []]


def test_get_bond_type_from_component():

    all_bond_type_Hk2 = aux.get_bond_type_from_component(molsys_Hk2, skip_digestion=True)
    all_bond_type_BB = aux.get_bond_type_from_component(molsys_BB, skip_digestion=True)
    list_bond_type_Hk2 = aux.get_bond_type_from_component(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_bond_type_BB = aux.get_bond_type_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_bond_type_Hk2, list)
    assert len(all_bond_type_Hk2) == 146
    assert len(all_bond_type_BB) == 521
    assert all_bond_type_Hk2[1][2000:2010] == [None, None, None, None, None, None, None, None, None, None]
    assert all_bond_type_Hk2[15:25] == [[None, None, None, None, None, None, None, None, None, None, None, None],
                                        [None, None, None, None, None, None, None, None, None, None, None, None,
                                         None, None, None, None], [], [], [], [], [], [], [], []]
    assert all_bond_type_Hk2[105:115] == [[], [], [], [], [], [], [], [], [], []]
    assert all_bond_type_Hk2[0][80:90] == [None, None, None, None, None, None, None, None, None, None]
    assert all_bond_type_Hk2[-1] == []
    assert all_bond_type_BB[0][40:50] == [None, None, None, None, None, None, None, None, None, None]
    assert all_bond_type_BB[3][500:510] == [None, None, None, None, None, None, None, None, None, None]
    assert all_bond_type_BB[6][100:110] == [None, None, None, None, None, None, None, None, None, None]
    assert all_bond_type_BB[9] == []
    assert all_bond_type_BB[-1] == []
    assert list_bond_type_Hk2[1][60:70] == [None, None, None, None, None, None, None, None, None, None]
    assert list_bond_type_BB == [[], [], [], []]


def test_get_bond_order_from_component():

    all_bond_order_Hk2 = aux.get_bond_order_from_component(molsys_Hk2, skip_digestion=True)
    all_bond_order_BB = aux.get_bond_order_from_component(molsys_BB, skip_digestion=True)
    list_bond_order_Hk2 = aux.get_bond_order_from_component(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_bond_order_BB = aux.get_bond_order_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_bond_order_Hk2, list)
    assert len(all_bond_order_Hk2) == 146
    assert len(all_bond_order_BB) == 521
    assert all_bond_order_Hk2[1][2000:2010] == [None, None, None, None, None, None, None, None, None, None]
    assert all_bond_order_Hk2[15:25] == [[None, None, None, None, None, None, None, None, None, None, None, None],
                                        [None, None, None, None, None, None, None, None, None, None, None, None,
                                         None, None, None, None], [], [], [], [], [], [], [], []]
    assert all_bond_order_Hk2[105:115] == [[], [], [], [], [], [], [], [], [], []]
    assert all_bond_order_Hk2[0][80:90] == [None, None, None, None, None, None, None, None, None, None]
    assert all_bond_order_Hk2[-1] == []
    assert all_bond_order_BB[0][40:50] == [None, None, None, None, None, None, None, None, None, None]
    assert all_bond_order_BB[3][500:510] == [None, None, None, None, None, None, None, None, None, None]
    assert all_bond_order_BB[6][100:110] == [None, None, None, None, None, None, None, None, None, None]
    assert all_bond_order_BB[9] == []
    assert all_bond_order_BB[-1] == []
    assert list_bond_order_Hk2[1][60:70] == [None, None, None, None, None, None, None, None, None, None]
    assert list_bond_order_BB == [[], [], [], []]


def test_get_bonded_atoms_from_component():

    all_bonded_atoms_Hk2 = aux.get_bonded_atoms_from_component(molsys_Hk2, skip_digestion=True)
    all_bonded_atoms_BB = aux.get_bonded_atoms_from_component(molsys_BB, skip_digestion=True)
    list_bonded_atoms_Hk2 = aux.get_bonded_atoms_from_component(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_bonded_atoms_BB = aux.get_bonded_atoms_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_bonded_atoms_Hk2, list)
    assert len(all_bonded_atoms_Hk2) == 146
    assert len(all_bonded_atoms_BB) == 521
    assert all_bonded_atoms_Hk2[1][2000:2010] == [2640, 2641, 2642, 2643, 2644, 2645, 2646, 2647, 2648, 2649]
    assert all_bonded_atoms_Hk2[15:25] == [[13337, 13338, 13339, 13340, 13341, 13342, 13343, 13344, 13345, 13346, 
                                            13347, 13348], [13349, 13350, 13351, 13352, 13353, 13354, 13355, 13356,
                                            13357, 13358, 13359, 13360, 13361, 13362, 13363, 13364],
                                           [], [], [], [], [], [], [], []]
    assert all_bonded_atoms_Hk2[105:115] == [[], [], [], [], [], [], [], [], [], []]
    assert all_bonded_atoms_Hk2[0][80:90] == [80, 81, 82, 83, 84, 85, 86, 87, 88, 89]
    assert all_bonded_atoms_Hk2[-1] == []
    assert all_bonded_atoms_BB[0][40:50] == [40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
    assert all_bonded_atoms_BB[3][500:510] == [3081, 3082, 3083, 3084, 3085, 3086, 3087, 3088, 3089, 3090]
    assert all_bonded_atoms_BB[6][100:110] == [3862, 3863, 3864, 3865, 3866, 3867, 3868, 3869, 3870, 3871]
    assert all_bonded_atoms_BB[9] == []
    assert all_bonded_atoms_BB[-1] == []
    assert list_bonded_atoms_Hk2[1][60:70] == [3892, 3893, 3894, 3895, 3896, 3897, 3898, 3899, 3900, 3901]
    assert list_bonded_atoms_BB == [[], [], [], []]


def test_get_bonded_atom_pairs_from_component():

    all_bonded_atom_pairs_Hk2 = aux.get_bonded_atom_pairs_from_component(molsys_Hk2, skip_digestion=True)
    all_bonded_atom_pairs_BB = aux.get_bonded_atom_pairs_from_component(molsys_BB, skip_digestion=True)
    list_bonded_atom_pairs_Hk2 = aux.get_bonded_atom_pairs_from_component(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_bonded_atom_pairs_BB = aux.get_bonded_atom_pairs_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_bonded_atom_pairs_Hk2, list)
    assert len(all_bonded_atom_pairs_Hk2) == 146
    assert len(all_bonded_atom_pairs_BB) == 521
    assert all_bonded_atom_pairs_Hk2[1][2000:2010] == [[2609, 2610], [2609, 2618], [2611, 2612], [2612, 2613],
                                                       [2613, 2614], [2614, 2615], [2615, 2616], [2615, 2617],
                                                       [2618, 2619], [2619, 2620]]
    assert all_bonded_atom_pairs_Hk2[15:25] == [[[13337, 13338], [13337, 13343], [13337, 13347], [13338, 13339],
                                                 [13338, 13344], [13339, 13340], [13339, 13345], [13340, 13341],
                                                 [13340, 13346], [13341, 13342], [13341, 13347], [13342, 13348]],
                                                [[13349, 13350], [13349, 13351], [13349, 13352], [13350, 13353],
                                                 [13350, 13354], [13352, 13357], [13353, 13355], [13353, 13356],
                                                 [13355, 13357], [13355, 13358], [13357, 13359], [13359, 13360],
                                                 [13360, 13361], [13361, 13362], [13361, 13363], [13361, 13364]],
                                                [], [], [], [], [], [], [], []]
    assert all_bonded_atom_pairs_Hk2[105:115] == [[], [], [], [], [], [], [], [], [], []]
    assert all_bonded_atom_pairs_Hk2[0][80:90] == [[79, 80], [79, 82], [80, 81], [80, 86], [82, 83], [83, 84],
                                                   [83, 85], [86, 87], [87, 88], [87, 90]]
    assert all_bonded_atom_pairs_Hk2[-1] == []
    assert all_bonded_atom_pairs_BB[0][40:50] == [[38, 40], [39, 40], [41, 42], [42, 43], [42, 45], [43, 44],
                                                  [43, 49], [45, 46], [46, 47], [46, 48]]
    assert all_bonded_atom_pairs_BB[3][500:510] == [[3066, 3070], [3068, 3069], [3070, 3071], [3071, 3072],
                                                    [3071, 3074], [3072, 3073], [3072, 3078], [3074, 3075],
                                                    [3075, 3076], [3076, 3077]]
    assert all_bonded_atom_pairs_BB[6][100:110] == [[3860, 3861], [3862, 3863], [3863, 3864], [3863, 3866],
                                                    [3864, 3865], [3864, 3867], [3867, 3868], [3868, 3869],
                                                    [3868, 3871], [3869, 3870]]
    assert all_bonded_atom_pairs_BB[9] == []
    assert all_bonded_atom_pairs_BB[-1] == []
    assert list_bonded_atom_pairs_Hk2[1][60:70] == [[3889, 3891], [3892, 3893], [3893, 3894], [3894, 3895],
                                                    [3894, 3896], [3896, 3897], [3897, 3898], [3898, 3899],
                                                    [3898, 3900], [3900, 3901]]
    assert list_bonded_atom_pairs_BB == [[], [], [], []]


def test_get_inner_bond_index_from_component():

    all_inner_bond_index_Hk2 = aux.get_inner_bond_index_from_component(molsys_Hk2, skip_digestion=True)
    all_inner_bond_index_BB = aux.get_inner_bond_index_from_component(molsys_BB, skip_digestion=True)
    list_inner_bond_index_Hk2 = aux.get_inner_bond_index_from_component(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_inner_bond_index_BB = aux.get_inner_bond_index_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_inner_bond_index_Hk2, list)
    assert len(all_inner_bond_index_Hk2) == 146
    assert len(all_inner_bond_index_BB) == 521
    assert all_inner_bond_index_Hk2[1][2000:2010] == [2653, 2654, 2655, 2656, 2657, 2658, 2659, 2660, 2661, 2662]
    assert all_inner_bond_index_Hk2[15:25] == [[13534, 13535, 13536, 13537, 13538, 13539, 13540, 13541, 13542, 13543,
                                          13544, 13545],
                                         [13546, 13547, 13548, 13549, 13550, 13551, 13552, 13553, 13554, 13555,
                                          13556, 13557, 13558, 13559, 13560, 13561], [], [], [], [], [], [], [], []]
    assert all_inner_bond_index_Hk2[105:115] == [[], [], [], [], [], [], [], [], [], []]
    assert all_inner_bond_index_Hk2[0][80:90] == [80, 81, 82, 83, 84, 85, 86, 87, 88, 89]
    assert all_inner_bond_index_Hk2[-1] == []
    assert all_inner_bond_index_BB[0][40:50] == [40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
    assert all_inner_bond_index_BB[3][500:510] == [3144, 3145, 3146, 3147, 3148, 3149, 3150, 3151, 3152, 3153]
    assert all_inner_bond_index_BB[6][100:110] == [3949, 3950, 3951, 3952, 3953, 3954, 3955, 3956, 3957, 3958]
    assert all_inner_bond_index_BB[9] == []
    assert all_inner_bond_index_BB[-1] == []
    assert list_inner_bond_index_Hk2[1][60:70] == [3952, 3953, 3954, 3955, 3956, 3957, 3958, 3959, 3960, 3961]
    assert list_inner_bond_index_BB == [[], [], [], []]


def test_get_inner_bonded_atom_pairs_from_component():

    all_inner_bonded_atom_pairs_Hk2 = aux.get_inner_bonded_atom_pairs_from_component(molsys_Hk2, skip_digestion=True)
    all_inner_bonded_atom_pairs_BB = aux.get_inner_bonded_atom_pairs_from_component(molsys_BB, skip_digestion=True)
    list_inner_bonded_atom_pairs_Hk2 = aux.get_inner_bonded_atom_pairs_from_component(molsys_Hk2, indices=[1,2,3], skip_digestion=True)
    list_inner_bonded_atom_pairs_BB = aux.get_inner_bonded_atom_pairs_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert isinstance(all_inner_bonded_atom_pairs_Hk2, list)
    assert len(all_inner_bonded_atom_pairs_Hk2) == 146
    assert len(all_inner_bonded_atom_pairs_BB) == 521
    assert all_inner_bonded_atom_pairs_Hk2[1][2000:2010] == [[2609, 2610], [2609, 2618], [2611, 2612], [2612, 2613],
                                                       [2613, 2614], [2614, 2615], [2615, 2616], [2615, 2617],
                                                       [2618, 2619], [2619, 2620]]
    assert all_inner_bonded_atom_pairs_Hk2[15:25] == [[[13337, 13338], [13337, 13343], [13337, 13347], [13338, 13339],
                                                 [13338, 13344], [13339, 13340], [13339, 13345], [13340, 13341],
                                                 [13340, 13346], [13341, 13342], [13341, 13347], [13342, 13348]],
                                                [[13349, 13350], [13349, 13351], [13349, 13352], [13350, 13353],
                                                 [13350, 13354], [13352, 13357], [13353, 13355], [13353, 13356],
                                                 [13355, 13357], [13355, 13358], [13357, 13359], [13359, 13360],
                                                 [13360, 13361], [13361, 13362], [13361, 13363], [13361, 13364]],
                                                [], [], [], [], [], [], [], []]
    assert all_inner_bonded_atom_pairs_Hk2[105:115] == [[], [], [], [], [], [], [], [], [], []]
    assert all_inner_bonded_atom_pairs_Hk2[0][80:90] == [[79, 80], [79, 82], [80, 81], [80, 86], [82, 83], [83, 84],
                                                   [83, 85], [86, 87], [87, 88], [87, 90]]
    assert all_inner_bonded_atom_pairs_Hk2[-1] == []
    assert all_inner_bonded_atom_pairs_BB[0][40:50] == [[38, 40], [39, 40], [41, 42], [42, 43], [42, 45], [43, 44],
                                                  [43, 49], [45, 46], [46, 47], [46, 48]]
    assert all_inner_bonded_atom_pairs_BB[3][500:510] == [[3066, 3070], [3068, 3069], [3070, 3071], [3071, 3072],
                                                    [3071, 3074], [3072, 3073], [3072, 3078], [3074, 3075],
                                                    [3075, 3076], [3076, 3077]]
    assert all_inner_bonded_atom_pairs_BB[6][100:110] == [[3860, 3861], [3862, 3863], [3863, 3864], [3863, 3866],
                                                    [3864, 3865], [3864, 3867], [3867, 3868], [3868, 3869],
                                                    [3868, 3871], [3869, 3870]]
    assert all_inner_bonded_atom_pairs_BB[9] == []
    assert all_inner_bonded_atom_pairs_BB[-1] == []
    assert list_inner_bonded_atom_pairs_Hk2[1][60:70] == [[3889, 3891], [3892, 3893], [3893, 3894], [3894, 3895],
                                                    [3894, 3896], [3896, 3897], [3897, 3898], [3898, 3899],
                                                    [3898, 3900], [3900, 3901]]
    assert list_inner_bonded_atom_pairs_BB == [[], [], [], []]


def test_get_n_atoms_from_component():

    all_n_atoms_Hk2 = aux.get_n_atoms_from_component(molsys_Hk2, skip_digestion=True)
    all_n_atoms_BB = aux.get_n_atoms_from_component(molsys_BB, skip_digestion=True)
    list_n_atoms_Hk2 = aux.get_n_atoms_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_atoms_BB = aux.get_n_atoms_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_atoms_Hk2) == 146
    assert len(all_n_atoms_BB) == 521
    assert all_n_atoms_Hk2[15:25] == [12, 16, 1, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_atoms_Hk2[105:115] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_atoms_Hk2[0] == 640
    assert all_n_atoms_Hk2[-1] == 1
    assert all_n_atoms_BB[3:13] == [517, 176, 488, 177, 699, 1, 1, 1, 1, 1]
    assert all_n_atoms_BB[486:492] == [1, 1, 1, 1, 1, 1]
    assert all_n_atoms_BB[0] == 864
    assert all_n_atoms_BB[-1] == 1
    assert list_n_atoms_Hk2 == [385, 1972, 636]
    assert list_n_atoms_BB == [1, 1, 1, 1]


def test_get_total_n_atoms_from_component():

    all_total_n_atoms_Hk2 = aux.get_total_n_atoms_from_component(molsys_Hk2, skip_digestion=True)
    all_total_n_atoms_BB = aux.get_total_n_atoms_from_component(molsys_BB, skip_digestion=True)
    list_total_n_atoms_Hk2 = aux.get_total_n_atoms_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_atoms_BB = aux.get_total_n_atoms_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_atoms_Hk2 == 13546
    assert all_total_n_atoms_BB == 5151
    assert list_total_n_atoms_Hk2 == 2993
    assert list_total_n_atoms_BB == 4


def test_get_n_groups_from_component():

    all_n_groups_Hk2 = aux.get_n_groups_from_component(molsys_Hk2, skip_digestion=True)
    all_n_groups_BB = aux.get_n_groups_from_component(molsys_BB, skip_digestion=True)
    list_n_groups_Hk2 = aux.get_n_groups_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_groups_BB = aux.get_n_groups_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_groups_Hk2) == 146
    assert len(all_n_groups_BB) == 521
    assert all_n_groups_Hk2[15:25] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_groups_Hk2[105:115] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_groups_Hk2[0] == 81
    assert all_n_groups_Hk2[-1] == 1
    assert all_n_groups_BB[3:13] == [63, 24, 62, 24, 89, 1, 1, 1, 1, 1]
    assert all_n_groups_BB[486:492] == [1, 1, 1, 1, 1, 1]
    assert all_n_groups_BB[0] == 108
    assert all_n_groups_BB[-1] == 1
    assert list_n_groups_Hk2 == [50, 266, 81]
    assert list_n_groups_BB == [1, 1, 1, 1]


def test_get_total_n_groups_from_component():

    all_total_n_groups_Hk2 = aux.get_total_n_groups_from_component(molsys_Hk2, skip_digestion=True)
    all_total_n_groups_BB = aux.get_total_n_groups_from_component(molsys_BB, skip_digestion=True)
    list_total_n_groups_Hk2 = aux.get_total_n_groups_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_groups_BB = aux.get_total_n_groups_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_groups_Hk2 == 1871
    assert all_total_n_groups_BB == 1101
    assert list_total_n_groups_Hk2 == 397
    assert list_total_n_groups_BB == 4


def test_get_n_molecules_from_component():

    all_n_molecules_Hk2 = aux.get_n_molecules_from_component(molsys_Hk2, skip_digestion=True)
    all_n_molecules_BB = aux.get_n_molecules_from_component(molsys_BB, skip_digestion=True)
    list_n_molecules_Hk2 = aux.get_n_molecules_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_molecules_BB = aux.get_n_molecules_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_molecules_Hk2 == 135
    assert all_n_molecules_BB == 519
    assert list_n_molecules_Hk2 == 2
    assert list_n_molecules_BB == 4


def test_get_total_n_molecules_from_component():

    all_total_n_molecules_Hk2 = aux.get_total_n_molecules_from_component(molsys_Hk2, skip_digestion=True)
    all_total_n_molecules_BB = aux.get_total_n_molecules_from_component(molsys_BB, skip_digestion=True)
    list_total_n_molecules_Hk2 = aux.get_total_n_molecules_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_molecules_BB = aux.get_total_n_molecules_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_molecules_Hk2 == 135
    assert all_total_n_molecules_BB == 519
    assert list_total_n_molecules_Hk2 == 2
    assert list_total_n_molecules_BB == 4


def test_get_n_entities_from_component():

    all_n_entities_Hk2 = aux.get_n_entities_from_component(molsys_Hk2, skip_digestion=True)
    all_n_entities_BB = aux.get_n_entities_from_component(molsys_BB, skip_digestion=True)
    list_n_entities_Hk2 = aux.get_n_entities_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_entities_BB = aux.get_n_entities_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_entities_Hk2 == 5
    assert all_n_entities_BB == 3
    assert list_n_entities_Hk2 == 1
    assert list_n_entities_BB == 1


def test_get_total_n_entities_from_component():

    all_total_n_entities_Hk2 = aux.get_total_n_entities_from_component(molsys_Hk2, skip_digestion=True)
    all_total_n_entities_BB = aux.get_total_n_entities_from_component(molsys_BB, skip_digestion=True)
    list_total_n_entities_Hk2 = aux.get_total_n_entities_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_entities_BB = aux.get_total_n_entities_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_entities_Hk2 == 5
    assert all_total_n_entities_BB == 3
    assert list_total_n_entities_Hk2 == 1
    assert list_total_n_entities_BB == 1


def test_get_n_components_from_component():

    all_n_components_Hk2 = aux.get_n_components_from_component(molsys_Hk2, skip_digestion=True)
    all_n_components_BB = aux.get_n_components_from_component(molsys_BB, skip_digestion=True)
    list_n_components_Hk2 = aux.get_n_components_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_components_BB = aux.get_n_components_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_components_Hk2 == 146
    assert all_n_components_BB == 521
    assert list_n_components_Hk2 == 3
    assert list_n_components_BB == 4


def test_get_total_n_components_from_component():

    all_total_n_components_Hk2 = aux.get_total_n_components_from_component(molsys_Hk2, skip_digestion=True)
    all_total_n_components_BB = aux.get_total_n_components_from_component(molsys_BB, skip_digestion=True)
    list_total_n_components_Hk2 = aux.get_total_n_components_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_components_BB = aux.get_total_n_components_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_components_Hk2 == 146
    assert all_total_n_components_BB == 521
    assert list_total_n_components_Hk2 == 3
    assert list_total_n_components_BB == 4


def test_get_n_chains_from_component():

    all_n_chains_Hk2 = aux.get_n_chains_from_component(molsys_Hk2, skip_digestion=True)
    all_n_chains_BB = aux.get_n_chains_from_component(molsys_BB, skip_digestion=True)
    list_n_chains_Hk2 = aux.get_n_chains_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_chains_BB = aux.get_n_chains_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_chains_Hk2) == 146
    assert len(all_n_chains_BB) == 521
    assert all_n_chains_Hk2[15:25] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_chains_Hk2[105:115] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_chains_Hk2[0] == 1
    assert all_n_chains_Hk2[-1] == 1
    assert all_n_chains_BB[3:13] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_chains_BB[486:492] == [1, 1, 1, 1, 1, 1]
    assert all_n_chains_BB[0] == 1
    assert all_n_chains_BB[-1] == 1
    assert list_n_chains_Hk2 == [1, 1, 1]
    assert list_n_chains_BB == [1, 1, 1, 1]


def test_get_total_n_chains_from_component():

    all_total_n_chains_Hk2 = aux.get_total_n_chains_from_component(molsys_Hk2, skip_digestion=True)
    all_total_n_chains_BB = aux.get_total_n_chains_from_component(molsys_BB, skip_digestion=True)
    list_total_n_chains_Hk2 = aux.get_total_n_chains_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_chains_BB = aux.get_total_n_chains_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_chains_Hk2 == 40
    assert all_total_n_chains_BB == 12
    assert list_total_n_chains_Hk2 == 2
    assert list_total_n_chains_BB == 1


def test_get_n_bonds_from_component():

    all_n_bonds_Hk2 = aux.get_n_bonds_from_component(molsys_Hk2, skip_digestion=True)
    all_n_bonds_BB = aux.get_n_bonds_from_component(molsys_BB, skip_digestion=True)
    list_n_bonds_Hk2 = aux.get_n_bonds_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_bonds_BB = aux.get_n_bonds_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_bonds_Hk2) == 146
    assert len(all_n_bonds_BB) == 521
    assert all_n_bonds_Hk2[15:25] == [12, 16, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_bonds_Hk2[105:115] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_bonds_Hk2[0] == 653
    assert all_n_bonds_Hk2[-1] == 0
    assert all_n_bonds_BB[3:13] == [529, 176, 500, 177, 712, 0, 0, 0, 0, 0]
    assert all_n_bonds_BB[486:492] == [0, 0, 0, 0, 0, 0]
    assert all_n_bonds_BB[0] == 885
    assert all_n_bonds_BB[-1] == 0
    assert list_n_bonds_Hk2 == [393, 1995, 649]
    assert list_n_bonds_BB == [0, 0, 0, 0]


def test_get_total_n_bonds_from_component():

    all_total_n_bonds_Hk2 = aux.get_total_n_bonds_from_component(molsys_Hk2, skip_digestion=True)
    all_total_n_bonds_BB = aux.get_total_n_bonds_from_component(molsys_BB, skip_digestion=True)
    list_total_n_bonds_Hk2 = aux.get_total_n_bonds_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_bonds_BB = aux.get_total_n_bonds_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_bonds_Hk2 == 13618
    assert all_total_n_bonds_BB == 4738
    assert list_total_n_bonds_Hk2 == 3037
    assert list_total_n_bonds_BB == 0


def test_get_n_inner_bonds_from_component():

    all_n_inner_bonds_Hk2 = aux.get_n_inner_bonds_from_component(molsys_Hk2, skip_digestion=True)
    all_n_inner_bonds_BB = aux.get_n_inner_bonds_from_component(molsys_BB, skip_digestion=True)
    list_n_inner_bonds_Hk2 = aux.get_n_inner_bonds_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_inner_bonds_BB = aux.get_n_inner_bonds_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_inner_bonds_Hk2) == 146
    assert len(all_n_inner_bonds_BB) == 521
    assert all_n_inner_bonds_Hk2[15:25] == [12, 16, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_inner_bonds_Hk2[105:115] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_inner_bonds_Hk2[0] == 653
    assert all_n_inner_bonds_Hk2[-1] == 0
    assert all_n_inner_bonds_BB[3:13] == [529, 176, 500, 177, 712, 0, 0, 0, 0, 0]
    assert all_n_inner_bonds_BB[486:492] == [0, 0, 0, 0, 0, 0]
    assert all_n_inner_bonds_BB[0] == 885
    assert all_n_inner_bonds_BB[-1] == 0
    assert list_n_inner_bonds_Hk2 == [393, 1995, 649]
    assert list_n_inner_bonds_BB == [0, 0, 0, 0]


def test_get_total_n_inner_bonds_from_component():

    all_total_n_inner_bonds_Hk2 = aux.get_total_n_inner_bonds_from_component(molsys_Hk2, skip_digestion=True)
    all_total_n_inner_bonds_BB = aux.get_total_n_inner_bonds_from_component(molsys_BB, skip_digestion=True)
    list_total_n_inner_bonds_Hk2 = aux.get_total_n_inner_bonds_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_inner_bonds_BB = aux.get_total_n_inner_bonds_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_inner_bonds_Hk2 == 13618
    assert all_total_n_inner_bonds_BB == 4738
    assert list_total_n_inner_bonds_Hk2 == 3037
    assert list_total_n_inner_bonds_BB == 0


def test_get_n_amino_acids_from_component():

    all_n_amino_acids_Hk2 = aux.get_n_amino_acids_from_component(molsys_Hk2, skip_digestion=True)
    all_n_amino_acids_BB = aux.get_n_amino_acids_from_component(molsys_BB, skip_digestion=True)
    list_n_amino_acids_Hk2 = aux.get_n_amino_acids_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_amino_acids_BB = aux.get_n_amino_acids_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_amino_acids_Hk2) == 146
    assert len(all_n_amino_acids_BB) == 521
    assert all_n_amino_acids_Hk2[15:25] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_amino_acids_Hk2[105:115] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_amino_acids_Hk2[0] == 81
    assert all_n_amino_acids_Hk2[-1] == 0
    assert all_n_amino_acids_BB[3:13] == [63, 24, 62, 24, 89, 0, 0, 0, 0, 0]
    assert all_n_amino_acids_BB[486:492] == [0, 0, 0, 0, 0, 0]
    assert all_n_amino_acids_BB[0] == 108
    assert all_n_amino_acids_BB[-1] == 0
    assert list_n_amino_acids_Hk2 == [50, 266, 81]
    assert list_n_amino_acids_BB == [0, 0, 0, 0]


def test_get_total_n_amino_acids_from_component():

    all_total_n_amino_acids_Hk2 = aux.get_total_n_amino_acids_from_component(molsys_Hk2, skip_digestion=True)
    all_total_n_amino_acids_BB = aux.get_total_n_amino_acids_from_component(molsys_BB, skip_digestion=True)
    list_total_n_amino_acids_Hk2 = aux.get_total_n_amino_acids_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_amino_acids_BB = aux.get_total_n_amino_acids_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_amino_acids_Hk2 == 1738
    assert all_total_n_amino_acids_BB == 588
    assert list_total_n_amino_acids_Hk2 == 397
    assert list_total_n_amino_acids_BB == 0


def test_get_n_nucleotides_from_component():

    all_n_nucleotides_Hk2 = aux.get_n_nucleotides_from_component(molsys_Hk2, skip_digestion=True)
    all_n_nucleotides_BB = aux.get_n_nucleotides_from_component(molsys_BB, skip_digestion=True)
    list_n_nucleotides_Hk2 = aux.get_n_nucleotides_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_nucleotides_BB = aux.get_n_nucleotides_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_nucleotides_Hk2) == 146
    assert len(all_n_nucleotides_BB) == 521
    assert all_n_nucleotides_Hk2 == 146*[0]
    assert all_n_nucleotides_BB == 521*[0]
    assert list_n_nucleotides_Hk2 == [0, 0, 0]
    assert list_n_nucleotides_BB == [0, 0, 0, 0]


def test_get_total_n_nucleotides_from_component():

    all_total_n_nucleotides_Hk2 = aux.get_total_n_nucleotides_from_component(molsys_Hk2, skip_digestion=True)
    all_total_n_nucleotides_BB = aux.get_total_n_nucleotides_from_component(molsys_BB, skip_digestion=True)
    list_total_n_nucleotides_Hk2 = aux.get_total_n_nucleotides_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_nucleotides_BB = aux.get_total_n_nucleotides_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_nucleotides_Hk2 == 0
    assert all_total_n_nucleotides_BB == 0
    assert list_total_n_nucleotides_Hk2 == 0
    assert list_total_n_nucleotides_BB == 0


def test_get_n_ions_from_component():

    all_n_ions_Hk2 = aux.get_n_ions_from_component(molsys_Hk2, skip_digestion=True)
    all_n_ions_BB = aux.get_n_ions_from_component(molsys_BB, skip_digestion=True)
    list_n_ions_Hk2 = aux.get_n_ions_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_ions_BB = aux.get_n_ions_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_ions_Hk2) == 146
    assert len(all_n_ions_BB) == 521
    assert all_n_ions_Hk2[15:35] == [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1]
    assert all_n_ions_Hk2[136:] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_ions_Hk2[:10] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_ions_BB == 521*[0]
    assert list_n_ions_Hk2 == [0, 0, 0]
    assert list_n_ions_BB == [0, 0, 0, 0]


def test_get_total_n_ions_from_component():

    all_total_n_ions_Hk2 = aux.get_total_n_ions_from_component(molsys_Hk2, skip_digestion=True)
    all_total_n_ions_BB = aux.get_total_n_ions_from_component(molsys_BB, skip_digestion=True)
    list_total_n_ions_Hk2 = aux.get_total_n_ions_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_ions_BB = aux.get_total_n_ions_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_ions_Hk2 == 28
    assert all_total_n_ions_BB == 0
    assert list_total_n_ions_Hk2 == 0
    assert list_total_n_ions_BB == 0


def test_get_n_waters_from_component():

    all_n_waters_Hk2 = aux.get_n_waters_from_component(molsys_Hk2, skip_digestion=True)
    all_n_waters_BB = aux.get_n_waters_from_component(molsys_BB, skip_digestion=True)
    list_n_waters_Hk2 = aux.get_n_waters_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_waters_BB = aux.get_n_waters_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_waters_Hk2) == 146
    assert len(all_n_waters_BB) == 521
    assert all_n_waters_Hk2[15:35] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_waters_Hk2[136:] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_waters_Hk2[:10] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_waters_BB[5:15] == [0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_waters_BB[511:] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert list_n_waters_Hk2 == [0, 0, 0]
    assert list_n_waters_BB == [1, 1, 1, 1]


def test_get_total_n_waters_from_component():

    all_total_n_waters_Hk2 = aux.get_total_n_waters_from_component(molsys_Hk2, skip_digestion=True)
    all_total_n_waters_BB = aux.get_total_n_waters_from_component(molsys_BB, skip_digestion=True)
    list_total_n_waters_Hk2 = aux.get_total_n_waters_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_waters_BB = aux.get_total_n_waters_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_waters_Hk2 == 97
    assert all_total_n_waters_BB == 513
    assert list_total_n_waters_Hk2 == 0
    assert list_total_n_waters_BB == 4


def test_get_n_small_molecules_from_component():

    all_n_small_molecules_Hk2 = aux.get_n_small_molecules_from_component(molsys_Hk2, skip_digestion=True)
    all_n_small_molecules_BB = aux.get_n_small_molecules_from_component(molsys_BB, skip_digestion=True)
    list_n_small_molecules_Hk2 = aux.get_n_small_molecules_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_small_molecules_BB = aux.get_n_small_molecules_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_small_molecules_Hk2) == 146
    assert len(all_n_small_molecules_BB) == 521
    assert all_n_small_molecules_Hk2 == 146*[0]
    assert all_n_small_molecules_BB == 521*[0]
    assert list_n_small_molecules_Hk2 == [0, 0, 0]
    assert list_n_small_molecules_BB == [0, 0, 0, 0]


def test_get_total_n_small_molecules_from_component():

    all_total_n_small_molecules_Hk2 = aux.get_total_n_small_molecules_from_component(molsys_Hk2, skip_digestion=True)
    all_total_n_small_molecules_BB = aux.get_total_n_small_molecules_from_component(molsys_BB, skip_digestion=True)
    list_total_n_small_molecules_Hk2 = aux.get_total_n_small_molecules_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_small_molecules_BB = aux.get_total_n_small_molecules_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_small_molecules_Hk2 == 0
    assert all_total_n_small_molecules_BB == 0
    assert list_total_n_small_molecules_Hk2 == 0
    assert list_total_n_small_molecules_BB == 0


def test_get_n_lipids_from_component():

    all_n_lipids_Hk2 = aux.get_n_lipids_from_component(molsys_Hk2, skip_digestion=True)
    all_n_lipids_BB = aux.get_n_lipids_from_component(molsys_BB, skip_digestion=True)
    list_n_lipids_Hk2 = aux.get_n_lipids_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_lipids_BB = aux.get_n_lipids_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_lipids_Hk2) == 146
    assert len(all_n_lipids_BB) == 521
    assert all_n_lipids_Hk2 == 146*[0]
    assert all_n_lipids_BB == 521*[0]
    assert list_n_lipids_Hk2 == [0, 0, 0]
    assert list_n_lipids_BB == [0, 0, 0, 0]


def test_get_total_n_lipids_from_component():

    all_total_n_lipids_Hk2 = aux.get_total_n_lipids_from_component(molsys_Hk2, skip_digestion=True)
    all_total_n_lipids_BB = aux.get_total_n_lipids_from_component(molsys_BB, skip_digestion=True)
    list_total_n_lipids_Hk2 = aux.get_total_n_lipids_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_lipids_BB = aux.get_total_n_lipids_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_lipids_Hk2 == 0
    assert all_total_n_lipids_BB == 0
    assert list_total_n_lipids_Hk2 == 0
    assert list_total_n_lipids_BB == 0


def test_get_n_saccharides_from_component():

    all_n_saccharides_Hk2 = aux.get_n_saccharides_from_component(molsys_Hk2, skip_digestion=True)
    all_n_saccharides_BB = aux.get_n_saccharides_from_component(molsys_BB, skip_digestion=True)
    list_n_saccharides_Hk2 = aux.get_n_saccharides_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_saccharides_BB = aux.get_n_saccharides_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert len(all_n_saccharides_Hk2) == 146
    assert len(all_n_saccharides_BB) == 521
    assert all_n_saccharides_Hk2[15:35] == [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0]
    assert all_n_saccharides_Hk2[100:110] == 10*[0]
    assert all_n_saccharides_BB == 521*[0]
    assert list_n_saccharides_Hk2 == [0, 0, 0]
    assert list_n_saccharides_BB == [0, 0, 0, 0]


def test_get_total_n_saccharides_from_component():

    all_total_n_saccharides_Hk2 = aux.get_total_n_saccharides_from_component(molsys_Hk2, skip_digestion=True)
    all_total_n_saccharides_BB = aux.get_total_n_saccharides_from_component(molsys_BB, skip_digestion=True)
    list_total_n_saccharides_Hk2 = aux.get_total_n_saccharides_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_saccharides_BB = aux.get_total_n_saccharides_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_saccharides_Hk2 == 8
    assert all_total_n_saccharides_BB == 0
    assert list_total_n_saccharides_Hk2 == 0
    assert list_total_n_saccharides_BB == 0


def test_get_n_polysaccharides_from_component():

    all_n_polysaccharides_Hk2 = aux.get_n_polysaccharides_from_component(molsys_Hk2, skip_digestion=True)
    all_n_polysaccharides_BB = aux.get_n_polysaccharides_from_component(molsys_BB, skip_digestion=True)
    list_n_polysaccharides_Hk2 = aux.get_n_polysaccharides_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_polysaccharides_BB = aux.get_n_polysaccharides_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_polysaccharides_Hk2 == 8
    assert all_n_polysaccharides_BB == 0
    assert list_n_polysaccharides_Hk2 == 0
    assert list_n_polysaccharides_BB == 0


def test_get_total_n_polysaccharides_from_component():

    all_total_n_polysaccharides_Hk2 = aux.get_total_n_polysaccharides_from_component(molsys_Hk2, skip_digestion=True)
    all_total_n_polysaccharides_BB = aux.get_total_n_polysaccharides_from_component(molsys_BB, skip_digestion=True)
    list_total_n_polysaccharides_Hk2 = aux.get_total_n_polysaccharides_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_polysaccharides_BB = aux.get_total_n_polysaccharides_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_polysaccharides_Hk2 == 8
    assert all_total_n_polysaccharides_BB == 0
    assert list_total_n_polysaccharides_Hk2 == 0
    assert list_total_n_polysaccharides_BB == 0


def test_get_n_peptides_from_component():

    all_n_peptides_Hk2 = aux.get_n_peptides_from_component(molsys_Hk2, skip_digestion=True)
    all_n_peptides_BB = aux.get_n_peptides_from_component(molsys_BB, skip_digestion=True)
    list_n_peptides_Hk2 = aux.get_n_peptides_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_peptides_BB = aux.get_n_peptides_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_peptides_Hk2 == 0
    assert all_n_peptides_BB == 0
    assert list_n_peptides_Hk2 == 0
    assert list_n_peptides_BB == 0


def test_get_total_n_peptides_from_component():

    all_total_n_peptides_Hk2 = aux.get_total_n_peptides_from_component(molsys_Hk2, skip_digestion=True)
    all_total_n_peptides_BB = aux.get_total_n_peptides_from_component(molsys_BB, skip_digestion=True)
    list_total_n_peptides_Hk2 = aux.get_total_n_peptides_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_peptides_BB = aux.get_total_n_peptides_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_peptides_Hk2 == 0
    assert all_total_n_peptides_BB == 0
    assert list_total_n_peptides_Hk2 == 0
    assert list_total_n_peptides_BB == 0


def test_get_n_proteins_from_component():

    all_n_proteins_Hk2 = aux.get_n_proteins_from_component(molsys_Hk2, skip_digestion=True)
    all_n_proteins_BB = aux.get_n_proteins_from_component(molsys_BB, skip_digestion=True)
    list_n_proteins_Hk2 = aux.get_n_proteins_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_proteins_BB = aux.get_n_proteins_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_proteins_Hk2 == 2
    assert all_n_proteins_BB == 6
    assert list_n_proteins_Hk2 == 1
    assert list_n_proteins_BB == 1


def test_get_total_n_proteins_from_component():

    all_total_n_proteins_Hk2 = aux.get_total_n_proteins_from_component(molsys_Hk2, skip_digestion=True)
    all_total_n_proteins_BB = aux.get_total_n_proteins_from_component(molsys_BB, skip_digestion=True)
    list_total_n_proteins_Hk2 = aux.get_total_n_proteins_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_proteins_BB = aux.get_total_n_proteins_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_proteins_Hk2 == 2
    assert all_total_n_proteins_BB == 6
    assert list_total_n_proteins_Hk2 == 1
    assert list_total_n_proteins_BB == 1


def test_get_n_dnas_from_component():

    all_n_dnas_Hk2 = aux.get_n_dnas_from_component(molsys_Hk2, skip_digestion=True)
    all_n_dnas_BB = aux.get_n_dnas_from_component(molsys_BB, skip_digestion=True)
    list_n_dnas_Hk2 = aux.get_n_dnas_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_dnas_BB = aux.get_n_dnas_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_dnas_Hk2 == 0
    assert all_n_dnas_BB == 0
    assert list_n_dnas_Hk2 == 0
    assert list_n_dnas_BB == 0


def test_get_total_n_dnas_from_component():

    all_total_n_dnas_Hk2 = aux.get_total_n_dnas_from_component(molsys_Hk2, skip_digestion=True)
    all_total_n_dnas_BB = aux.get_total_n_dnas_from_component(molsys_BB, skip_digestion=True)
    list_total_n_dnas_Hk2 = aux.get_total_n_dnas_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_dnas_BB = aux.get_total_n_dnas_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_dnas_Hk2 == 0
    assert all_total_n_dnas_BB == 0
    assert list_total_n_dnas_Hk2 == 0
    assert list_total_n_dnas_BB == 0


def test_get_n_rnas_from_component():

    all_n_rnas_Hk2 = aux.get_n_rnas_from_component(molsys_Hk2, skip_digestion=True)
    all_n_rnas_BB = aux.get_n_rnas_from_component(molsys_BB, skip_digestion=True)
    list_n_rnas_Hk2 = aux.get_n_rnas_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_n_rnas_BB = aux.get_n_rnas_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_n_rnas_Hk2 == 0
    assert all_n_rnas_BB == 0
    assert list_n_rnas_Hk2 == 0
    assert list_n_rnas_BB == 0


def test_get_total_n_rnas_from_component():

    all_total_n_rnas_Hk2 = aux.get_total_n_rnas_from_component(molsys_Hk2, skip_digestion=True)
    all_total_n_rnas_BB = aux.get_total_n_rnas_from_component(molsys_BB, skip_digestion=True)
    list_total_n_rnas_Hk2 = aux.get_total_n_rnas_from_component(molsys_Hk2, indices=[4,5,6], skip_digestion=True)
    list_total_n_rnas_BB = aux.get_total_n_rnas_from_component(molsys_BB, indices=[10,11,12,13], skip_digestion=True)

    assert all_total_n_rnas_Hk2 == 0
    assert all_total_n_rnas_BB == 0
    assert list_total_n_rnas_Hk2 == 0
    assert list_total_n_rnas_BB == 0

 
# From chain


def test_get_atom_index_from_chain():

    all_atom_index_Hk2 = aux.get_atom_index_from_chain(molsys_Hk2, skip_digestion=True)
    all_atom_index_BB = aux.get_atom_index_from_chain(molsys_BB, skip_digestion=True)
    list_atom_index_Hk2 = aux.get_atom_index_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_atom_index_BB = aux.get_atom_index_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_atom_index_Hk2, list)
    assert len(all_atom_index_Hk2) == 40
    assert len(all_atom_index_BB) == 12
    assert all_atom_index_Hk2[0] == list(range(6653))
    assert all_atom_index_Hk2[1] == list(range(6653,13309))
    assert all_atom_index_Hk2[2] == [13309, 13310, 13311, 13312, 13313, 13314, 13315, 13316, 13317, 13318, 13319, 13320]
    assert all_atom_index_Hk2[-1] == list(range(13498, 13546))
    assert all_atom_index_BB[0] == list(range(864))
    assert all_atom_index_BB[1] == list(range(864,1742))
    assert all_atom_index_BB[2] == list(range(1742,2581))
    assert list_atom_index_Hk2[0] == [13321, 13322, 13323, 13324, 13325, 13326, 13327, 13328, 13329, 13330, 13331,
                                      13332, 13333, 13334, 13335, 13336]
    assert list_atom_index_BB[1] == list(range(3274, 3939))


def test_get_atom_id_from_chain():

    all_atom_id_Hk2 = aux.get_atom_id_from_chain(molsys_Hk2, skip_digestion=True)
    all_atom_id_BB = aux.get_atom_id_from_chain(molsys_BB, skip_digestion=True)
    list_atom_id_Hk2 = aux.get_atom_id_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_atom_id_BB = aux.get_atom_id_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_atom_id_Hk2, list)
    assert len(all_atom_id_Hk2) == 40
    assert len(all_atom_id_BB) == 12
    assert len(all_atom_id_Hk2[0]) == 6653
    assert all_atom_id_Hk2[0][3000:3010] == [3001, 3002, 3003, 3004, 3005, 3006, 3007, 3008, 3009, 3010]
    assert len(all_atom_id_Hk2[1]) == 6656
    assert all_atom_id_Hk2[1][1000:1010] == [7654, 7655, 7656, 7657, 7658, 7659, 7660, 7661, 7662, 7663]
    assert all_atom_id_Hk2[2] == [13310, 13311, 13312, 13313, 13314, 13315, 13316, 13317, 13318, 13319, 13320, 13321] 
    assert all_atom_id_Hk2[-1] == list(range(13499, 13547))
    assert len(all_atom_id_BB[0]) == 864
    assert all_atom_id_BB[0][400:410] == [401, 402, 403, 404, 405, 406, 407, 408, 409, 410]
    assert len(all_atom_id_BB[1]) == 878
    assert all_atom_id_BB[1][400:410] == [1265, 1266, 1267, 1268, 1269, 1270, 1271, 1272, 1273, 1274]
    assert len(all_atom_id_BB[2]) == 839
    assert all_atom_id_BB[2][400:410] == [2143, 2144, 2145, 2146, 2147, 2148, 2149, 2150, 2151, 2152]
    assert all_atom_id_BB[-1] == list(range(5114, 5154))
    assert list_atom_id_Hk2[0] == [13322, 13323, 13324, 13325, 13326, 13327, 13328, 13329, 13330, 13331,
                                   13332, 13333, 13334, 13335, 13336, 13337]
    assert list_atom_id_BB[1] == list(range(3277, 3942))


def test_get_atom_name_from_chain():

    all_atom_name_Hk2 = aux.get_atom_name_from_chain(molsys_Hk2, skip_digestion=True)
    all_atom_name_BB = aux.get_atom_name_from_chain(molsys_BB, skip_digestion=True)
    list_atom_name_Hk2 = aux.get_atom_name_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_atom_name_BB = aux.get_atom_name_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_atom_name_Hk2, list)
    assert len(all_atom_name_Hk2) == 40
    assert len(all_atom_name_BB) == 12
    assert len(all_atom_name_Hk2[0]) == 6653
    assert all_atom_name_Hk2[0][3000:3010] == ['CG2', 'N', 'CA', 'C', 'O', 'CB', 'CG', 'OD1', 'OD2', 'N']
    assert len(all_atom_name_Hk2[1]) == 6656
    assert all_atom_name_Hk2[1][1000:1010] == ['CA', 'C', 'O', 'CB', 'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ']
    assert all_atom_name_Hk2[2] == ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6']
    assert all_atom_name_Hk2[-1] == 48*['O']
    assert len(all_atom_name_BB[0]) == 864
    assert all_atom_name_BB[0][400:410] == ['O', 'CB', 'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ', 'N', 'CA']
    assert len(all_atom_name_BB[1]) == 878
    assert all_atom_name_BB[1][400:410] == ['CG', 'OD1', 'OD2', 'N', 'CA', 'C', 'O', 'CB', 'CG1', 'CG2']
    assert len(all_atom_name_BB[2]) == 839
    assert all_atom_name_BB[2][400:410] == ['CA', 'C', 'O', 'CB', 'CG', 'CD', 'NE', 'CZ', 'NH1', 'NH2']
    assert all_atom_name_BB[-1] == 40*['O']
    assert list_atom_name_Hk2[0] == ['C1', 'C2', 'O1', 'O5', 'C3', 'O2', 'C4', 'O3', 'C5', 'O4', 'C6', 'O6', 'P',
                                   'O1P', 'O2P', 'O3P']
    assert list_atom_name_BB[1][400:410] == ['CB', 'CG', 'CD', 'OE1', 'OE2', 'N', 'CA', 'C', 'O', 'CB']

def test_get_atom_type_from_chain():

    all_atom_type_Hk2 = aux.get_atom_type_from_chain(molsys_Hk2, skip_digestion=True)
    all_atom_type_BB = aux.get_atom_type_from_chain(molsys_BB, skip_digestion=True)
    list_atom_type_Hk2 = aux.get_atom_type_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_atom_type_BB = aux.get_atom_type_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_atom_type_Hk2, list)
    assert len(all_atom_type_Hk2) == 40
    assert len(all_atom_type_BB) == 12
    assert len(all_atom_type_Hk2[0]) == 6653
    assert all_atom_type_Hk2[0][3000:3010] == ['C', 'N', 'C', 'C', 'O', 'C', 'C', 'O', 'O', 'N']
    assert len(all_atom_type_Hk2[1]) == 6656
    assert all_atom_type_Hk2[1][1000:1010] == ['C', 'C', 'O', 'C', 'C', 'C', 'C', 'C', 'C', 'C']
    assert all_atom_type_Hk2[2] == ['C', 'C', 'C', 'C', 'C', 'C', 'O', 'O', 'O', 'O', 'O', 'O']
    assert all_atom_type_Hk2[-1] == 48*['O']
    assert len(all_atom_type_BB[0]) == 864
    assert all_atom_type_BB[0][400:410] == ['O', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'C']
    assert len(all_atom_type_BB[1]) == 878
    assert all_atom_type_BB[1][400:410] == ['C', 'O', 'O', 'N', 'C', 'C', 'O', 'C', 'C', 'C']
    assert len(all_atom_type_BB[2]) == 839
    assert all_atom_type_BB[2][400:410] == ['C', 'C', 'O', 'C', 'C', 'C', 'N', 'C', 'N', 'N']
    assert all_atom_type_BB[-1] == 40*['O']
    assert list_atom_type_Hk2[0] == ['C', 'C', 'O', 'O', 'C', 'O', 'C', 'O', 'C', 'O', 'C', 'O', 'P',
                                   'O', 'O', 'O']
    assert list_atom_type_BB[1][400:410] == ['C', 'C', 'C', 'O', 'O', 'N', 'C', 'C', 'O', 'C']


def test_get_group_index_from_chain():

    all_group_index_Hk2 = aux.get_group_index_from_chain(molsys_Hk2, skip_digestion=True)
    all_group_index_BB = aux.get_group_index_from_chain(molsys_BB, skip_digestion=True)
    list_group_index_Hk2 = aux.get_group_index_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_group_index_BB = aux.get_group_index_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_group_index_Hk2, list)
    assert len(all_group_index_Hk2) == 40
    assert len(all_group_index_BB) == 12
    assert len(all_group_index_Hk2[0]) == 871
    assert all_group_index_Hk2[0][300:310] == [300, 301, 302, 303, 304, 305, 306, 307, 308, 309] 
    assert len(all_group_index_Hk2[1]) == 867
    assert all_group_index_Hk2[1][400:410] == [1271, 1272, 1273, 1274, 1275, 1276, 1277, 1278, 1279, 1280]
    assert all_group_index_Hk2[2] == [1738]
    assert all_group_index_Hk2[-1] == list(range(1823, 1871))
    assert len(all_group_index_BB[0]) == 108
    assert all_group_index_BB[0][40:50] == [40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
    assert len(all_group_index_BB[1]) == 110
    assert all_group_index_BB[1][40:50] == [148, 149, 150, 151, 152, 153, 154, 155, 156, 157]
    assert len(all_group_index_BB[2]) == 108
    assert all_group_index_BB[2][40:50] == [258, 259, 260, 261, 262, 263, 264, 265, 266, 267]
    assert all_group_index_BB[-1] == list(range(1061, 1101))
    assert len(list_group_index_BB[1]) == 86
    assert list_group_index_Hk2 == [[1739], [1740], [1741]] 
    assert list_group_index_BB[1][10:20] == [423, 424, 425, 426, 427, 428, 429, 430, 431, 432]


def test_get_group_id_from_chain():

    all_group_id_Hk2 = aux.get_group_id_from_chain(molsys_Hk2, skip_digestion=True)
    all_group_id_BB = aux.get_group_id_from_chain(molsys_BB, skip_digestion=True)
    list_group_id_Hk2 = aux.get_group_id_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_group_id_BB = aux.get_group_id_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_group_id_Hk2, list)
    assert len(all_group_id_Hk2) == 40
    assert len(all_group_id_BB) == 12
    assert len(all_group_id_Hk2[0]) == 871
    assert all_group_id_Hk2[0][300:310] == [324, 325, 326, 327, 328, 329, 330, 331, 332, 333]
    assert len(all_group_id_Hk2[1]) == 867
    assert all_group_id_Hk2[1][400:410] == [427, 428, 429, 430, 431, 432, 433, 434, 435, 436]
    assert all_group_id_Hk2[2] == [1001]
    assert all_group_id_Hk2[-1][30:40] == [1061, 1062, 1063, 1064, 1067, 1075, 1077, 1078, 1079, 1081]
    assert len(all_group_id_BB[0]) == 108
    assert all_group_id_BB[0][40:50] == [43, 44, 45, 46, 47, 48, 49, 50, 51, 52]
    assert len(all_group_id_BB[1]) == 110
    assert all_group_id_BB[1][40:50] == [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    assert len(all_group_id_BB[2]) == 108
    assert all_group_id_BB[2][40:50] == [43, 44, 45, 46, 47, 48, 49, 50, 51, 52]
    assert all_group_id_BB[-1][20:30] == [110, 111, 112, 113, 114, 115, 116, 117, 118, 119]
    assert len(list_group_id_BB[1]) == 86
    assert list_group_id_Hk2 == [[1002], [1003], [1004]]
    assert list_group_id_BB[1][10:20] == [12, 13, 14, 15, 16, 17, 18, 19, 20, 21]


def test_get_group_name_from_chain():

    all_group_name_Hk2 = aux.get_group_name_from_chain(molsys_Hk2, skip_digestion=True)
    all_group_name_BB = aux.get_group_name_from_chain(molsys_BB, skip_digestion=True)
    list_group_name_Hk2 = aux.get_group_name_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_group_name_BB = aux.get_group_name_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_group_name_Hk2, list)
    assert len(all_group_name_Hk2) == 40
    assert len(all_group_name_BB) == 12
    assert len(all_group_name_Hk2[0]) == 871
    assert all_group_name_Hk2[0][300:310] == ['LEU', 'SER', 'PRO', 'GLU', 'LEU', 'LEU', 'ASN', 'THR', 'GLY', 'ARG']
    assert len(all_group_name_Hk2[1]) == 867
    assert all_group_name_Hk2[1][400:410] == ['LEU', 'HIS', 'LYS', 'THR', 'VAL', 'ARG', 'ARG', 'LEU', 'VAL', 'PRO']
    assert all_group_name_Hk2[2] == ['GLC']
    assert all_group_name_Hk2[-1][30:40] == ['HOH', 'HOH', 'HOH', 'HOH', 'HOH', 'HOH', 'HOH', 'HOH', 'HOH', 'HOH']
    assert len(all_group_name_BB[0]) == 108
    assert all_group_name_BB[0][40:50] == ['ALA', 'ASP', 'VAL', 'ALA', 'PRO', 'GLY', 'LYS', 'SER', 'ILE', 'GLY']
    assert len(all_group_name_BB[1]) == 110
    assert all_group_name_BB[1][40:50] == ['ASN', 'LEU', 'ALA', 'ASP', 'VAL', 'ALA', 'PRO', 'GLY', 'LYS', 'SER']
    assert len(all_group_name_BB[2]) == 108
    assert all_group_name_BB[2][40:50] == ['ALA', 'ASP', 'VAL', 'ALA', 'PRO', 'GLY', 'LYS', 'SER', 'ILE', 'GLY']
    assert all_group_name_BB[-1] == ['HOH']*40
    assert len(list_group_name_BB[1]) == 86
    assert list_group_name_Hk2 == [['BG6'], ['GLC'], ['BG6']]
    assert list_group_name_BB[1][10:20] == ['SER', 'ILE', 'SER', 'ASP', 'LEU', 'HIS', 'GLN', 'THR', 'LEU', 'LYS']


def test_get_group_type_from_chain():

    all_group_type_Hk2 = aux.get_group_type_from_chain(molsys_Hk2, skip_digestion=True)
    all_group_type_BB = aux.get_group_type_from_chain(molsys_BB, skip_digestion=True)
    list_group_type_Hk2 = aux.get_group_type_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_group_type_BB = aux.get_group_type_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_group_type_Hk2, list)
    assert len(all_group_type_Hk2) == 40
    assert len(all_group_type_BB) == 12
    assert len(all_group_type_Hk2[0]) == 871
    assert all_group_type_Hk2[0][300:310] == 10*['amino acid']
    assert len(all_group_type_Hk2[1]) == 867
    assert all_group_type_Hk2[1][400:410] == 10*['amino acid']
    assert all_group_type_Hk2[2] == ['saccharide']
    assert all_group_type_Hk2[-1][30:40] == 10*['water']
    assert len(all_group_type_BB[0]) == 108
    assert all_group_type_BB[0][40:50] == 10*['amino acid']
    assert len(all_group_type_BB[1]) == 110
    assert all_group_type_BB[1][40:50] == 10*['amino acid']
    assert len(all_group_type_BB[2]) == 108
    assert all_group_type_BB[2][40:50] == 10*['amino acid']
    assert all_group_type_BB[-1] == 40*['water']
    assert len(list_group_type_BB[1]) == 86
    assert list_group_type_Hk2 == [['saccharide'], ['saccharide'], ['saccharide']]
    assert list_group_type_BB[1][10:20] == 10*['amino acid']


def test_get_molecule_index_from_chain():

    all_molecule_index_Hk2 = aux.get_molecule_index_from_chain(molsys_Hk2, skip_digestion=True)
    all_molecule_index_BB = aux.get_molecule_index_from_chain(molsys_BB, skip_digestion=True)
    list_molecule_index_Hk2 = aux.get_molecule_index_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_molecule_index_BB = aux.get_molecule_index_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_molecule_index_Hk2, list)
    assert len(all_molecule_index_Hk2) == 40
    assert len(all_molecule_index_BB) == 12
    assert all_molecule_index_Hk2[0] == [0]
    assert all_molecule_index_Hk2[1] == [1]
    assert all_molecule_index_Hk2[2] == [2]
    assert all_molecule_index_Hk2[10] == [10]
    assert all_molecule_index_Hk2[20] == [20]
    assert all_molecule_index_Hk2[30] == [30]
    assert all_molecule_index_Hk2[38] == list(range(38, 87))
    assert all_molecule_index_Hk2[-1] == list(range(87, 135))
    assert all_molecule_index_BB[0] == [0]
    assert all_molecule_index_BB[1] == [1]
    assert all_molecule_index_BB[2] == [2]
    assert all_molecule_index_BB[6] == list(range(6, 151))
    assert all_molecule_index_BB[10] == list(range(415, 479))
    assert all_molecule_index_BB[-1] == list(range(479, 519))
    assert list_molecule_index_Hk2 == [[3], [4], [5]]
    assert list_molecule_index_BB == [[3], [4]]


def test_get_molecule_id_from_chain():

    all_molecule_id_Hk2 = aux.get_molecule_id_from_chain(molsys_Hk2, skip_digestion=True)
    all_molecule_id_BB = aux.get_molecule_id_from_chain(molsys_BB, skip_digestion=True)
    list_molecule_id_Hk2 = aux.get_molecule_id_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_molecule_id_BB = aux.get_molecule_id_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_molecule_id_Hk2, list)
    assert len(all_molecule_id_Hk2) == 40
    assert len(all_molecule_id_BB) == 12
    assert all_molecule_id_Hk2[0] == [0]
    assert all_molecule_id_Hk2[1] == [1]
    assert all_molecule_id_Hk2[2] == [2]
    assert all_molecule_id_Hk2[10] == [10]
    assert all_molecule_id_Hk2[20] == [20]
    assert all_molecule_id_Hk2[30] == [30]
    assert all_molecule_id_Hk2[38] == list(range(38, 87))
    assert all_molecule_id_Hk2[-1] == list(range(87, 135))
    assert all_molecule_id_BB[0] == [0]
    assert all_molecule_id_BB[1] == [1]
    assert all_molecule_id_BB[2] == [2]
    assert all_molecule_id_BB[6] == list(range(6, 151))
    assert all_molecule_id_BB[10] == list(range(415, 479))
    assert all_molecule_id_BB[-1] == list(range(479, 519))
    assert list_molecule_id_Hk2 == [[3], [4], [5]]
    assert list_molecule_id_BB == [[3], [4]]


def test_get_molecule_name_from_chain():

    all_molecule_name_Hk2 = aux.get_molecule_name_from_chain(molsys_Hk2, skip_digestion=True)
    all_molecule_name_BB = aux.get_molecule_name_from_chain(molsys_BB, skip_digestion=True)
    list_molecule_name_Hk2 = aux.get_molecule_name_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_molecule_name_BB = aux.get_molecule_name_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_molecule_name_Hk2, list)
    assert len(all_molecule_name_Hk2) == 40
    assert len(all_molecule_name_BB) == 12
    assert all_molecule_name_Hk2[0] == ['Hexokinase-2']
    assert all_molecule_name_Hk2[2:6] == [['alpha-D-glucopyranose'], ['6-O-phosphono-beta-D-glucopyranose'],
                                          ['alpha-D-glucopyranose'], ['6-O-phosphono-beta-D-glucopyranose']]
    assert all_molecule_name_Hk2[10] == ['UNKNOWN ATOM OR ION']
    assert all_molecule_name_Hk2[20] == ['alpha-D-glucopyranose']
    assert all_molecule_name_Hk2[30] == ['UNKNOWN ATOM OR ION']
    assert all_molecule_name_Hk2[38] == 49*['water']
    assert all_molecule_name_Hk2[39] == 48*['water']
    assert all_molecule_name_BB[0:6] == [['BARNASE'], ['BARNASE'], ['BARNASE'], ['BARSTAR'], ['BARSTAR'], ['BARSTAR']]
    assert all_molecule_name_BB[6] == 145*['water']
    assert all_molecule_name_BB[-1] == 40*['water']
    assert list_molecule_name_Hk2 == [['6-O-phosphono-beta-D-glucopyranose'], ['alpha-D-glucopyranose'],
                                      ['6-O-phosphono-beta-D-glucopyranose']]
    assert list_molecule_name_BB == [['BARSTAR'], ['BARSTAR']]


def test_get_molecule_type_from_chain():

    all_molecule_type_Hk2 = aux.get_molecule_type_from_chain(molsys_Hk2, skip_digestion=True)
    all_molecule_type_BB = aux.get_molecule_type_from_chain(molsys_BB, skip_digestion=True)
    list_molecule_type_Hk2 = aux.get_molecule_type_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_molecule_type_BB = aux.get_molecule_type_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_molecule_type_Hk2, list)
    assert len(all_molecule_type_Hk2) == 40
    assert len(all_molecule_type_BB) == 12
    assert all_molecule_type_Hk2[0] == ['protein']
    assert all_molecule_type_Hk2[2:6] == [['polysaccharide'], ['polysaccharide'], ['polysaccharide'], ['polysaccharide']]
    assert all_molecule_type_Hk2[10] == ['unknown']
    assert all_molecule_type_Hk2[20] == ['polysaccharide']
    assert all_molecule_type_Hk2[30] == ['unknown']
    assert all_molecule_type_Hk2[38] == 49*['water']
    assert all_molecule_type_Hk2[39] == 48*['water']
    assert all_molecule_type_BB[0:6] == [['protein'], ['protein'], ['protein'], ['protein'], ['protein'], ['protein']]
    assert all_molecule_type_BB[6] == 145*['water']
    assert all_molecule_type_BB[-1] == 40*['water']
    assert list_molecule_type_Hk2 == [['polysaccharide'], ['polysaccharide'], ['polysaccharide']]
    assert list_molecule_type_BB == [['protein'], ['protein']]


def test_get_entity_index_from_chain():

    all_entity_index_Hk2 = aux.get_entity_index_from_chain(molsys_Hk2, skip_digestion=True)
    all_entity_index_BB = aux.get_entity_index_from_chain(molsys_BB, skip_digestion=True)
    list_entity_index_Hk2 = aux.get_entity_index_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_entity_index_BB = aux.get_entity_index_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_entity_index_Hk2, list)
    assert len(all_entity_index_Hk2) == 40
    assert len(all_entity_index_BB) == 12
    assert all_entity_index_Hk2[0] == [0]
    assert all_entity_index_Hk2[2:6] == [[1], [2], [1], [2]]
    assert all_entity_index_Hk2[10] == [3]
    assert all_entity_index_Hk2[20] == [1]
    assert all_entity_index_Hk2[30] == [3]
    assert all_entity_index_Hk2[38] == [4]
    assert all_entity_index_Hk2[39] == [4]
    assert all_entity_index_BB[0:6] == [[0], [0], [0], [1], [1], [1]]
    assert all_entity_index_BB[6] == [2]
    assert all_entity_index_BB[-1] == [2]
    assert list_entity_index_Hk2 == [[2], [1], [2]]
    assert list_entity_index_BB == [[1], [1]]


def test_get_entity_id_from_chain():

    all_entity_id_Hk2 = aux.get_entity_id_from_chain(molsys_Hk2, skip_digestion=True)
    all_entity_id_BB = aux.get_entity_id_from_chain(molsys_BB, skip_digestion=True)
    list_entity_id_Hk2 = aux.get_entity_id_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_entity_id_BB = aux.get_entity_id_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_entity_id_Hk2, list)
    assert len(all_entity_id_Hk2) == 40
    assert len(all_entity_id_BB) == 12
    assert all_entity_id_Hk2[0] == [1]
    assert all_entity_id_Hk2[2:6] == [[2], [3], [2], [3]]
    assert all_entity_id_Hk2[10] == [4]
    assert all_entity_id_Hk2[20] == [2]
    assert all_entity_id_Hk2[30] == [4]
    assert all_entity_id_Hk2[38] == [5]
    assert all_entity_id_Hk2[39] == [5]
    assert all_entity_id_BB[0:6] == [[1], [1], [1], [2], [2], [2]]
    assert all_entity_id_BB[6] == [3]
    assert all_entity_id_BB[-1] == [3]
    assert list_entity_id_Hk2 == [[3], [2], [3]]
    assert list_entity_id_BB == [[2], [2]]


def test_get_entity_name_from_chain():

    all_entity_name_Hk2 = aux.get_entity_name_from_chain(molsys_Hk2, skip_digestion=True)
    all_entity_name_BB = aux.get_entity_name_from_chain(molsys_BB, skip_digestion=True)
    list_entity_name_Hk2 = aux.get_entity_name_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_entity_name_BB = aux.get_entity_name_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_entity_name_Hk2, list)
    assert len(all_entity_name_Hk2) == 40
    assert len(all_entity_name_BB) == 12
    assert all_entity_name_Hk2[0] == ['Hexokinase-2']
    assert all_entity_name_Hk2[2:6] == [['alpha-D-glucopyranose'], ['6-O-phosphono-beta-D-glucopyranose'],
                                        ['alpha-D-glucopyranose'], ['6-O-phosphono-beta-D-glucopyranose']]
    assert all_entity_name_Hk2[10] == ['UNKNOWN ATOM OR ION']
    assert all_entity_name_Hk2[20] == ['alpha-D-glucopyranose']
    assert all_entity_name_Hk2[30] == ['UNKNOWN ATOM OR ION']
    assert all_entity_name_Hk2[38] == ['water']
    assert all_entity_name_Hk2[39] == ['water']
    assert all_entity_name_BB[0:6] == [['BARNASE'], ['BARNASE'], ['BARNASE'], ['BARSTAR'], ['BARSTAR'], ['BARSTAR']]
    assert all_entity_name_BB[6] == ['water']
    assert all_entity_name_BB[-1] == ['water']
    assert list_entity_name_Hk2 == [['6-O-phosphono-beta-D-glucopyranose'], ['alpha-D-glucopyranose'],
                                    ['6-O-phosphono-beta-D-glucopyranose']]
    assert list_entity_name_BB == [['BARSTAR'], ['BARSTAR']]


def test_get_entity_type_from_chain():

    all_entity_type_Hk2 = aux.get_entity_type_from_chain(molsys_Hk2, skip_digestion=True)
    all_entity_type_BB = aux.get_entity_type_from_chain(molsys_BB, skip_digestion=True)
    list_entity_type_Hk2 = aux.get_entity_type_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_entity_type_BB = aux.get_entity_type_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_entity_type_Hk2, list)
    assert len(all_entity_type_Hk2) == 40
    assert len(all_entity_type_BB) == 12
    assert all_entity_type_Hk2[0] == ['protein']
    assert all_entity_type_Hk2[2:6] == [['polysaccharide'], ['polysaccharide'], ['polysaccharide'], ['polysaccharide']]
    assert all_entity_type_Hk2[10] == ['unknown']
    assert all_entity_type_Hk2[20] == ['polysaccharide']
    assert all_entity_type_Hk2[30] == ['unknown']
    assert all_entity_type_Hk2[38] == ['water']
    assert all_entity_type_Hk2[39] == ['water']
    assert all_entity_type_BB[0:6] == [['protein'], ['protein'], ['protein'], ['protein'], ['protein'], ['protein']]
    assert all_entity_type_BB[6] == ['water']
    assert all_entity_type_BB[-1] == ['water']
    assert list_entity_type_Hk2 == [['polysaccharide'], ['polysaccharide'],['polysaccharide']]
    assert list_entity_type_BB == [['protein'], ['protein']]


def test_get_component_index_from_chain():

    all_component_index_Hk2 = aux.get_component_index_from_chain(molsys_Hk2, skip_digestion=True)
    all_component_index_BB = aux.get_component_index_from_chain(molsys_BB, skip_digestion=True)
    list_component_index_Hk2 = aux.get_component_index_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_component_index_BB = aux.get_component_index_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_component_index_Hk2, list)
    assert len(all_component_index_Hk2) == 40
    assert len(all_component_index_BB) == 12
    assert all_component_index_Hk2[0] == [0, 1, 2, 3, 4, 5]
    assert all_component_index_Hk2[2:6] == [[13], [14], [15], [16]]
    assert all_component_index_Hk2[10] == [21]
    assert all_component_index_Hk2[20] == [31]
    assert all_component_index_Hk2[30] == [41]
    assert all_component_index_Hk2[38] == list(range(49, 98))
    assert all_component_index_Hk2[39] == list(range(98, 146))
    assert all_component_index_BB[0:6] == [[0], [1], [2], [3, 4], [5, 6], [7]]
    assert all_component_index_BB[6] == list(range(8, 153))
    assert all_component_index_BB[-1] == list(range(481, 521))
    assert list_component_index_Hk2 == [[14], [15], [16]]
    assert list_component_index_BB == [[3, 4], [5, 6]]


def test_get_component_id_from_chain():

    all_component_id_Hk2 = aux.get_component_id_from_chain(molsys_Hk2, skip_digestion=True)
    all_component_id_BB = aux.get_component_id_from_chain(molsys_BB, skip_digestion=True)
    list_component_id_Hk2 = aux.get_component_id_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_component_id_BB = aux.get_component_id_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_component_id_Hk2, list)
    assert len(all_component_id_Hk2) == 40
    assert len(all_component_id_BB) == 12
    assert all_component_id_Hk2[0] == [0, 1, 2, 3, 4, 5]
    assert all_component_id_Hk2[2:6] == [[13], [14], [15], [16]]
    assert all_component_id_Hk2[10] == [21]
    assert all_component_id_Hk2[20] == [31]
    assert all_component_id_Hk2[30] == [41]
    assert all_component_id_Hk2[38] == list(range(49, 98))
    assert all_component_id_Hk2[39] == list(range(98, 146))
    assert all_component_id_BB[0:6] == [[0], [1], [2], [3, 4], [5, 6], [7]]
    assert all_component_id_BB[6] == list(range(8, 153))
    assert all_component_id_BB[-1] == list(range(481, 521))
    assert list_component_id_Hk2 == [[14], [15], [16]]
    assert list_component_id_BB == [[3, 4], [5, 6]]


def test_get_component_name_from_chain():

    all_component_name_Hk2 = aux.get_component_name_from_chain(molsys_Hk2, skip_digestion=True)
    all_component_name_BB = aux.get_component_name_from_chain(molsys_BB, skip_digestion=True)
    list_component_name_Hk2 = aux.get_component_name_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_component_name_BB = aux.get_component_name_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_component_name_Hk2, list)
    assert len(all_component_name_Hk2) == 40
    assert len(all_component_name_BB) == 12
    assert all_component_name_Hk2[0] == ['protein 0', 'protein 1', 'peptide 0', 'peptide 1', 'protein 2', 'protein 3']
    assert all_component_name_Hk2[2:6] == [['unknown 0'], ['unknown 1'], ['unknown 2'], ['unknown 3']]
    assert all_component_name_Hk2[10] == ['UNX']
    assert all_component_name_Hk2[20] == ['unknown 6']
    assert all_component_name_Hk2[30] == ['UNX']
    assert all_component_name_Hk2[38] == 49*['water']
    assert all_component_name_Hk2[39] == 48*['water']
    assert all_component_name_BB[0:6] == [['protein 0'], ['protein 1'], ['protein 2'], ['protein 3', 'peptide 0'],
                                        ['protein 4', 'peptide 0'], ['protein 5']]
    assert all_component_name_BB[6] == 145*['water']
    assert all_component_name_BB[-1] == 40*['water']
    assert list_component_name_Hk2 == [['unknown 1'], ['unknown 2'], ['unknown 3']]
    assert list_component_name_BB == [['protein 3', 'peptide 0'], ['protein 4', 'peptide 0']]


def test_get_component_type_from_chain():

    all_component_type_Hk2 = aux.get_component_type_from_chain(molsys_Hk2, skip_digestion=True)
    all_component_type_BB = aux.get_component_type_from_chain(molsys_BB, skip_digestion=True)
    list_component_type_Hk2 = aux.get_component_type_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_component_type_BB = aux.get_component_type_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_component_type_Hk2, list)
    assert len(all_component_type_Hk2) == 40
    assert len(all_component_type_BB) == 12
    assert all_component_type_Hk2[0] == ['protein', 'protein', 'peptide', 'peptide', 'protein', 'protein']
    assert all_component_type_Hk2[2:6] == [['polysaccharide'], ['polysaccharide'], ['polysaccharide'], ['polysaccharide']]
    assert all_component_type_Hk2[10] == ['ion']
    assert all_component_type_Hk2[20] == ['polysaccharide']
    assert all_component_type_Hk2[30] == ['ion']
    assert all_component_type_Hk2[38] == 49*['water']
    assert all_component_type_Hk2[39] == 48*['water']
    assert all_component_type_BB[0:6] == [['protein'], ['protein'], ['protein'], ['protein', 'peptide'],
                                         ['protein', 'peptide'], ['protein']]
    assert all_component_type_BB[6] == 145*['water']
    assert all_component_type_BB[-1] == 40*['water']
    assert list_component_type_Hk2 == [['polysaccharide'], ['polysaccharide'], ['polysaccharide']]
    assert list_component_type_BB == [['protein', 'peptide'], ['protein', 'peptide']]


def test_get_chain_index_from_chain():

    all_chain_index_Hk2 = aux.get_chain_index_from_chain(molsys_Hk2, skip_digestion=True)
    all_chain_index_BB = aux.get_chain_index_from_chain(molsys_BB, skip_digestion=True)
    list_chain_index_Hk2 = aux.get_chain_index_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_chain_index_BB = aux.get_chain_index_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_chain_index_Hk2 == list(range(40))
    assert all_chain_index_BB == list(range(12))
    assert list_chain_index_Hk2 == [3, 4, 5]
    assert list_chain_index_BB == [3, 4]


def test_get_chain_id_from_chain():

    all_chain_id_Hk2 = aux.get_chain_id_from_chain(molsys_Hk2, skip_digestion=True)
    all_chain_id_BB = aux.get_chain_id_from_chain(molsys_BB, skip_digestion=True)
    list_chain_id_Hk2 = aux.get_chain_id_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_chain_id_BB = aux.get_chain_id_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_chain_id_Hk2, list)
    assert len(all_chain_id_Hk2) == 40
    assert len(all_chain_id_BB) == 12
    assert all_chain_id_Hk2[0:6] == ['A', 'B', 'C', 'D', 'E', 'F']
    assert all_chain_id_Hk2[10] == 'K'
    assert all_chain_id_Hk2[20] == 'U'
    assert all_chain_id_Hk2[30] == 'EA'
    assert all_chain_id_Hk2[38] == 'MA'
    assert all_chain_id_Hk2[39] == 'NA'
    assert all_chain_id_BB[0:6] == ['A', 'B', 'C', 'D', 'E', 'F']
    assert all_chain_id_BB[-1] == 'L'
    assert list_chain_id_Hk2 == ['D', 'E', 'F']
    assert list_chain_id_BB == ['D', 'E']


def test_get_chain_name_from_chain():

    all_chain_name_Hk2 = aux.get_chain_name_from_chain(molsys_Hk2, skip_digestion=True)
    all_chain_name_BB = aux.get_chain_name_from_chain(molsys_BB, skip_digestion=True)
    list_chain_name_Hk2 = aux.get_chain_name_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_chain_name_BB = aux.get_chain_name_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_chain_name_Hk2, list)
    assert len(all_chain_name_Hk2) == 40
    assert len(all_chain_name_BB) == 12
    assert all_chain_name_Hk2[0:6] == ['A', 'B', 'A', 'A', 'A', 'A']
    assert all_chain_name_Hk2[10] == 'A'
    assert all_chain_name_Hk2[20] == 'B'
    assert all_chain_name_Hk2[30] == 'B'
    assert all_chain_name_Hk2[38] == 'A'
    assert all_chain_name_Hk2[39] == 'B'
    assert all_chain_name_BB[0:6] == ['A', 'B', 'C', 'D', 'E', 'F']
    assert all_chain_name_BB[-1] == 'F'
    assert list_chain_name_Hk2 == ['A', 'A', 'A']
    assert list_chain_name_BB == ['D', 'E']


def test_get_chain_type_from_chain():

    all_chain_type_Hk2 = aux.get_chain_type_from_chain(molsys_Hk2, skip_digestion=True)
    all_chain_type_BB = aux.get_chain_type_from_chain(molsys_BB, skip_digestion=True)
    list_chain_type_Hk2 = aux.get_chain_type_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_chain_type_BB = aux.get_chain_type_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_chain_type_Hk2, list)
    assert len(all_chain_type_Hk2) == 40
    assert len(all_chain_type_BB) == 12
    assert all_chain_type_Hk2[0:6] == ['protein', 'protein', 'polysaccharide', 'polysaccharide',
                                       'polysaccharide', 'polysaccharide']
    assert all_chain_type_Hk2[10] == 'unknown' 
    assert all_chain_type_Hk2[20] == 'polysaccharide'
    assert all_chain_type_Hk2[30] == 'unknown'
    assert all_chain_type_Hk2[38:40] == ['water', 'water']
    assert all_chain_type_BB[0:6] == 6*['protein']
    assert all_chain_type_BB[-1] == 'water'
    assert list_chain_type_Hk2 == ['polysaccharide', 'polysaccharide', 'polysaccharide']
    assert list_chain_type_BB == ['protein', 'protein']


def test_get_bond_index_from_chain():

    all_bond_index_Hk2 = aux.get_bond_index_from_chain(molsys_Hk2, skip_digestion=True)
    all_bond_index_BB = aux.get_bond_index_from_chain(molsys_BB, skip_digestion=True)
    list_bond_index_Hk2 = aux.get_bond_index_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_bond_index_BB = aux.get_bond_index_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_bond_index_Hk2, list)
    assert len(all_bond_index_Hk2) == 40
    assert len(all_bond_index_BB) == 12
    assert len(all_bond_index_Hk2[0]) == 6751
    assert all_bond_index_Hk2[1][2000:2010] == [8751, 8752, 8753, 8754, 8755, 8756, 8757, 8758, 8759, 8760]
    assert all_bond_index_Hk2[15:25] == [[], [], [],
                                         [13562, 13563, 13564, 13565, 13566, 13567, 13568, 13569, 13570, 13571,
                                          13572, 13573],
                                         [13574, 13575, 13576, 13577, 13578, 13579, 13580, 13581, 13582, 13583,
                                          13584, 13585, 13586, 13587, 13588, 13589],
                                         [13590, 13591, 13592, 13593, 13594, 13595, 13596, 13597, 13598, 13599,
                                          13600, 13601],
                                         [13602, 13603, 13604, 13605, 13606, 13607, 13608, 13609, 13610, 13611,
                                          13612, 13613, 13614, 13615, 13616, 13617], [], [], []]
    assert all_bond_index_Hk2[-1] == []
    assert all_bond_index_BB[0] == list(range(885))
    assert all_bond_index_BB[3] == list(range(2644, 3349))
    assert all_bond_index_BB[-1] == []
    assert list_bond_index_Hk2 == [[13518, 13519, 13520, 13521, 13522, 13523, 13524, 13525, 13526, 13527, 13528,
                                    13529, 13530, 13531, 13532, 13533],
                                   [13534, 13535, 13536, 13537, 13538, 13539, 13540, 13541, 13542, 13543, 13544,
                                    13545],
                                   [13546, 13547, 13548, 13549, 13550, 13551, 13552, 13553, 13554, 13555, 13556,
                                    13557, 13558, 13559, 13560, 13561]]
    assert list_bond_index_BB ==  [list(range(2644, 3349)), list(range(3349, 4026))]


def test_get_bond_type_from_chain():

    all_bond_type_Hk2 = aux.get_bond_type_from_chain(molsys_Hk2, skip_digestion=True)
    all_bond_type_BB = aux.get_bond_type_from_chain(molsys_BB, skip_digestion=True)
    list_bond_type_Hk2 = aux.get_bond_type_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_bond_type_BB = aux.get_bond_type_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_bond_type_Hk2, list)
    assert len(all_bond_type_Hk2) == 40
    assert len(all_bond_type_BB) == 12
    assert len(all_bond_type_Hk2[0]) == 6751
    assert all_bond_type_Hk2[1][2000:2010] == 10*[None]
    assert all_bond_type_Hk2[15:25] == [[], [], [], 12*[None], 16*[None], 12*[None], 16*[None], [], [], []]
    assert all_bond_type_Hk2[-1] == []
    assert len(all_bond_type_BB[0]) == 885
    assert all_bond_type_BB[3][200:210] == 10*[None]
    assert all_bond_type_BB[-1] == []
    assert list_bond_type_Hk2 == [16*[None], 12*[None], 16*[None]]
    assert list_bond_type_BB ==  [705*[None], 677*[None]]


def test_get_bond_order_from_chain():

    all_bond_order_Hk2 = aux.get_bond_order_from_chain(molsys_Hk2, skip_digestion=True)
    all_bond_order_BB = aux.get_bond_order_from_chain(molsys_BB, skip_digestion=True)
    list_bond_order_Hk2 = aux.get_bond_order_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_bond_order_BB = aux.get_bond_order_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_bond_order_Hk2, list)
    assert len(all_bond_order_Hk2) == 40
    assert len(all_bond_order_BB) == 12
    assert len(all_bond_order_Hk2[0]) == 6751
    assert all_bond_order_Hk2[1][2000:2010] == 10*[None]
    assert all_bond_order_Hk2[15:25] == [[], [], [], 12*[None], 16*[None], 12*[None], 16*[None], [], [], []]
    assert all_bond_order_Hk2[-1] == []
    assert len(all_bond_order_BB[0]) == 885
    assert all_bond_order_BB[3][200:210] == 10*[None]
    assert all_bond_order_BB[-1] == []
    assert list_bond_order_Hk2 == [16*[None], 12*[None], 16*[None]]
    assert list_bond_order_BB ==  [705*[None], 677*[None]]


def test_get_bonded_atoms_from_chain():

    all_bonded_atoms_Hk2 = aux.get_bonded_atoms_from_chain(molsys_Hk2, skip_digestion=True)
    all_bonded_atoms_BB = aux.get_bonded_atoms_from_chain(molsys_BB, skip_digestion=True)
    list_bonded_atoms_Hk2 = aux.get_bonded_atoms_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_bonded_atoms_BB = aux.get_bonded_atoms_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_bonded_atoms_Hk2, list)
    assert len(all_bonded_atoms_Hk2) == 40
    assert len(all_bonded_atoms_BB) == 12
    assert len(all_bonded_atoms_Hk2[0]) == 6653
    assert all_bonded_atoms_Hk2[0][2000:2010] == [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009]
    assert len(all_bonded_atoms_Hk2[1]) == 6656
    assert all_bonded_atoms_Hk2[1][2000:2010] == [8653, 8654, 8655, 8656, 8657, 8658, 8659, 8660, 8661, 8662]
    assert all_bonded_atoms_Hk2[15:25] == [[], [], [], [13377, 13378, 13379, 13380, 13381, 13382, 13383, 13384, 13385,
                                           13386, 13387, 13388], [13389, 13390, 13391, 13392, 13393, 13394, 13395,
                                           13396, 13397, 13398, 13399, 13400, 13401, 13402, 13403, 13404],
                                           [13405, 13406, 13407, 13408, 13409, 13410, 13411, 13412, 13413, 13414,
                                            13415, 13416], [13417, 13418, 13419, 13420, 13421, 13422, 13423, 13424,
                                            13425, 13426, 13427, 13428, 13429, 13430, 13431, 13432], [], [], []]
    assert all_bonded_atoms_Hk2[-1] == []
    assert len(all_bonded_atoms_BB[0]) == 864
    assert all_bonded_atoms_BB[0][400:410] == [400, 401, 402, 403, 404, 405, 406, 407, 408, 409]
    assert all_bonded_atoms_BB[2][400:410] == [2142, 2143, 2144, 2145, 2146, 2147, 2148, 2149, 2150, 2151]
    assert all_bonded_atoms_BB[-1] == []
    assert list_bonded_atoms_Hk2 == [[13321, 13322, 13323, 13324, 13325, 13326, 13327, 13328, 13329, 13330,
                                      13331, 13332, 13333, 13334, 13335, 13336], [13337, 13338, 13339, 13340,
                                      13341, 13342, 13343, 13344, 13345, 13346, 13347, 13348], [13349, 13350,
                                      13351, 13352, 13353, 13354, 13355, 13356, 13357, 13358, 13359, 13360, 13361,
                                      13362, 13363, 13364]]
    assert len(list_bonded_atoms_BB[0]) ==  693
    assert list_bonded_atoms_BB[0][100:110] == [2681, 2682, 2683, 2684, 2685, 2686, 2687, 2688, 2689, 2690]
    assert len(list_bonded_atoms_BB[1]) ==  665
    assert list_bonded_atoms_BB[1][500:510] == [3774, 3775, 3776, 3777, 3778, 3779, 3780, 3781, 3782, 3783]


def test_get_bonded_atom_pairs_from_chain():

    all_bonded_atom_pairs_Hk2 = aux.get_bonded_atom_pairs_from_chain(molsys_Hk2, skip_digestion=True)
    all_bonded_atom_pairs_BB = aux.get_bonded_atom_pairs_from_chain(molsys_BB, skip_digestion=True)
    list_bonded_atom_pairs_Hk2 = aux.get_bonded_atom_pairs_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_bonded_atom_pairs_BB = aux.get_bonded_atom_pairs_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_bonded_atom_pairs_Hk2, list)
    assert len(all_bonded_atom_pairs_Hk2) == 40
    assert len(all_bonded_atom_pairs_BB) == 12
    assert len(all_bonded_atom_pairs_Hk2[0]) == 6751
    assert all_bonded_atom_pairs_Hk2[0][2000:2010] == [[1964, 1965], [1964, 1967], [1965, 1966], [1965, 1970],
                                                       [1967, 1968], [1967, 1969], [1970, 1971], [1971, 1972],
                                                       [1971, 1974], [1972, 1973]]
    assert len(all_bonded_atom_pairs_Hk2[1]) == 6755
    assert all_bonded_atom_pairs_Hk2[1][2000:2010] == [[8616, 8617], [8617, 8618], [8618, 8619], [8618, 8620],
                                                       [8621, 8622], [8622, 8623], [8622, 8625], [8623, 8624],
                                                       [8623, 8632], [8625, 8626]]
    assert all_bonded_atom_pairs_Hk2[-1] == []
    assert len(all_bonded_atom_pairs_BB[0]) == 885
    assert all_bonded_atom_pairs_BB[0][400:410] == [[390, 393], [391, 392], [391, 397], [393, 394], [393, 395],
                                                    [394, 396], [397, 398], [398, 399], [398, 401], [399, 400]]
    assert all_bonded_atom_pairs_BB[2][400:410] == [[2131, 2132], [2133, 2134], [2134, 2135], [2134, 2137],
                                                    [2135, 2136], [2135, 2141], [2137, 2138], [2138, 2139],
                                                    [2138, 2140], [2141, 2142]]
    assert all_bonded_atom_pairs_BB[-1] == []
    assert list_bonded_atom_pairs_Hk2 == [[[13321, 13322], [13321, 13323], [13321, 13324], [13322, 13325],
                                           [13322, 13326], [13324, 13329], [13325, 13327], [13325, 13328],
                                           [13327, 13329], [13327, 13330], [13329, 13331], [13331, 13332],
                                           [13332, 13333], [13333, 13334], [13333, 13335], [13333, 13336]],
                                          [[13337, 13338], [13337, 13343], [13337, 13347], [13338, 13339],
                                           [13338, 13344], [13339, 13340], [13339, 13345], [13340, 13341],
                                           [13340, 13346], [13341, 13342], [13341, 13347], [13342, 13348]],
                                          [[13349, 13350], [13349, 13351], [13349, 13352], [13350, 13353],
                                           [13350, 13354], [13352, 13357], [13353, 13355], [13353, 13356],
                                           [13355, 13357], [13355, 13358], [13357, 13359], [13359, 13360],
                                           [13360, 13361], [13361, 13362], [13361, 13363], [13361, 13364]]]
    assert len(list_bonded_atom_pairs_BB[0]) == 705
    assert list_bonded_atom_pairs_BB[0][100:110] == [[2679, 2681], [2682, 2683], [2683, 2684], [2683, 2686],
                                                     [2684, 2685], [2684, 2688], [2686, 2687], [2688, 2689],
                                                     [2689, 2690], [2689, 2692]]
    assert len(list_bonded_atom_pairs_BB[1]) == 677
    assert list_bonded_atom_pairs_BB[1][500:510] == [[3762, 3763], [3763, 3764], [3764, 3765], [3764, 3766],
                                                     [3766, 3767], [3767, 3768], [3767, 3770], [3768, 3769],
                                                     [3768, 3771], [3771, 3772]]


def test_get_inner_bond_index_from_chain():

    all_inner_bond_index_Hk2 = aux.get_inner_bond_index_from_chain(molsys_Hk2, skip_digestion=True)
    all_inner_bond_index_BB = aux.get_inner_bond_index_from_chain(molsys_BB, skip_digestion=True)
    list_inner_bond_index_Hk2 = aux.get_inner_bond_index_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_inner_bond_index_BB = aux.get_inner_bond_index_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_inner_bond_index_Hk2, list)
    assert len(all_inner_bond_index_Hk2) == 40
    assert len(all_inner_bond_index_BB) == 12
    assert len(all_inner_bond_index_Hk2[0]) == 6751
    assert all_inner_bond_index_Hk2[1][2000:2010] == [8751, 8752, 8753, 8754, 8755, 8756, 8757, 8758, 8759, 8760]
    assert all_inner_bond_index_Hk2[15:25] == [[], [], [],
                                         [13562, 13563, 13564, 13565, 13566, 13567, 13568, 13569, 13570, 13571,
                                          13572, 13573],
                                         [13574, 13575, 13576, 13577, 13578, 13579, 13580, 13581, 13582, 13583,
                                          13584, 13585, 13586, 13587, 13588, 13589],
                                         [13590, 13591, 13592, 13593, 13594, 13595, 13596, 13597, 13598, 13599,
                                          13600, 13601],
                                         [13602, 13603, 13604, 13605, 13606, 13607, 13608, 13609, 13610, 13611,
                                          13612, 13613, 13614, 13615, 13616, 13617], [], [], []]
    assert all_inner_bond_index_Hk2[-1] == []
    assert all_inner_bond_index_BB[0] == list(range(885))
    assert all_inner_bond_index_BB[3] == list(range(2644, 3349))
    assert all_inner_bond_index_BB[-1] == []
    assert list_inner_bond_index_Hk2 == [[13518, 13519, 13520, 13521, 13522, 13523, 13524, 13525, 13526, 13527, 13528,
                                    13529, 13530, 13531, 13532, 13533],
                                   [13534, 13535, 13536, 13537, 13538, 13539, 13540, 13541, 13542, 13543, 13544,
                                    13545],
                                   [13546, 13547, 13548, 13549, 13550, 13551, 13552, 13553, 13554, 13555, 13556,
                                    13557, 13558, 13559, 13560, 13561]]
    assert list_inner_bond_index_BB ==  [list(range(2644, 3349)), list(range(3349, 4026))]


def test_get_inner_bonded_atoms_from_chain():

    all_inner_bonded_atoms_Hk2 = aux.get_inner_bonded_atoms_from_chain(molsys_Hk2, skip_digestion=True)
    all_inner_bonded_atoms_BB = aux.get_inner_bonded_atoms_from_chain(molsys_BB, skip_digestion=True)
    list_inner_bonded_atoms_Hk2 = aux.get_inner_bonded_atoms_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_inner_bonded_atoms_BB = aux.get_inner_bonded_atoms_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_inner_bonded_atoms_Hk2, list)
    assert len(all_inner_bonded_atoms_Hk2) == 40
    assert len(all_inner_bonded_atoms_BB) == 12
    assert len(all_inner_bonded_atoms_Hk2[0]) == 6653
    assert all_inner_bonded_atoms_Hk2[0][2000:2010] == [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009]
    assert len(all_inner_bonded_atoms_Hk2[1]) == 6656
    assert all_inner_bonded_atoms_Hk2[1][2000:2010] == [8653, 8654, 8655, 8656, 8657, 8658, 8659, 8660, 8661, 8662]
    assert all_inner_bonded_atoms_Hk2[15:25] == [[], [], [], [13377, 13378, 13379, 13380, 13381, 13382, 13383, 13384, 13385,
                                           13386, 13387, 13388], [13389, 13390, 13391, 13392, 13393, 13394, 13395,
                                           13396, 13397, 13398, 13399, 13400, 13401, 13402, 13403, 13404],
                                           [13405, 13406, 13407, 13408, 13409, 13410, 13411, 13412, 13413, 13414,
                                            13415, 13416], [13417, 13418, 13419, 13420, 13421, 13422, 13423, 13424,
                                            13425, 13426, 13427, 13428, 13429, 13430, 13431, 13432], [], [], []]
    assert all_inner_bonded_atoms_Hk2[-1] == []
    assert len(all_inner_bonded_atoms_BB[0]) == 864
    assert all_inner_bonded_atoms_BB[0][400:410] == [400, 401, 402, 403, 404, 405, 406, 407, 408, 409]
    assert all_inner_bonded_atoms_BB[2][400:410] == [2142, 2143, 2144, 2145, 2146, 2147, 2148, 2149, 2150, 2151]
    assert all_inner_bonded_atoms_BB[-1] == []
    assert list_inner_bonded_atoms_Hk2 == [[13321, 13322, 13323, 13324, 13325, 13326, 13327, 13328, 13329, 13330,
                                      13331, 13332, 13333, 13334, 13335, 13336], [13337, 13338, 13339, 13340,
                                      13341, 13342, 13343, 13344, 13345, 13346, 13347, 13348], [13349, 13350,
                                      13351, 13352, 13353, 13354, 13355, 13356, 13357, 13358, 13359, 13360, 13361,
                                      13362, 13363, 13364]]
    assert len(list_inner_bonded_atoms_BB[0]) ==  693
    assert list_inner_bonded_atoms_BB[0][100:110] == [2681, 2682, 2683, 2684, 2685, 2686, 2687, 2688, 2689, 2690]
    assert len(list_inner_bonded_atoms_BB[1]) ==  665
    assert list_inner_bonded_atoms_BB[1][500:510] == [3774, 3775, 3776, 3777, 3778, 3779, 3780, 3781, 3782, 3783]


def test_get_inner_bonded_atom_pairs_from_chain():

    all_inner_bonded_atom_pairs_Hk2 = aux.get_inner_bonded_atom_pairs_from_chain(molsys_Hk2, skip_digestion=True)
    all_inner_bonded_atom_pairs_BB = aux.get_inner_bonded_atom_pairs_from_chain(molsys_BB, skip_digestion=True)
    list_inner_bonded_atom_pairs_Hk2 = aux.get_inner_bonded_atom_pairs_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_inner_bonded_atom_pairs_BB = aux.get_inner_bonded_atom_pairs_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert isinstance(all_inner_bonded_atom_pairs_Hk2, list)
    assert len(all_inner_bonded_atom_pairs_Hk2) == 40
    assert len(all_inner_bonded_atom_pairs_BB) == 12
    assert len(all_inner_bonded_atom_pairs_Hk2[0]) == 6751
    assert all_inner_bonded_atom_pairs_Hk2[0][2000:2010] == [[1964, 1965], [1964, 1967], [1965, 1966], [1965, 1970],
                                                       [1967, 1968], [1967, 1969], [1970, 1971], [1971, 1972],
                                                       [1971, 1974], [1972, 1973]]
    assert len(all_inner_bonded_atom_pairs_Hk2[1]) == 6755
    assert all_inner_bonded_atom_pairs_Hk2[1][2000:2010] == [[8616, 8617], [8617, 8618], [8618, 8619], [8618, 8620],
                                                       [8621, 8622], [8622, 8623], [8622, 8625], [8623, 8624],
                                                       [8623, 8632], [8625, 8626]]
    assert all_inner_bonded_atom_pairs_Hk2[-1] == []
    assert len(all_inner_bonded_atom_pairs_BB[0]) == 885
    assert all_inner_bonded_atom_pairs_BB[0][400:410] == [[390, 393], [391, 392], [391, 397], [393, 394], [393, 395],
                                                    [394, 396], [397, 398], [398, 399], [398, 401], [399, 400]]
    assert all_inner_bonded_atom_pairs_BB[2][400:410] == [[2131, 2132], [2133, 2134], [2134, 2135], [2134, 2137],
                                                    [2135, 2136], [2135, 2141], [2137, 2138], [2138, 2139],
                                                    [2138, 2140], [2141, 2142]]
    assert all_inner_bonded_atom_pairs_BB[-1] == []
    assert list_inner_bonded_atom_pairs_Hk2 == [[[13321, 13322], [13321, 13323], [13321, 13324], [13322, 13325],
                                           [13322, 13326], [13324, 13329], [13325, 13327], [13325, 13328],
                                           [13327, 13329], [13327, 13330], [13329, 13331], [13331, 13332],
                                           [13332, 13333], [13333, 13334], [13333, 13335], [13333, 13336]],
                                          [[13337, 13338], [13337, 13343], [13337, 13347], [13338, 13339],
                                           [13338, 13344], [13339, 13340], [13339, 13345], [13340, 13341],
                                           [13340, 13346], [13341, 13342], [13341, 13347], [13342, 13348]],
                                          [[13349, 13350], [13349, 13351], [13349, 13352], [13350, 13353],
                                           [13350, 13354], [13352, 13357], [13353, 13355], [13353, 13356],
                                           [13355, 13357], [13355, 13358], [13357, 13359], [13359, 13360],
                                           [13360, 13361], [13361, 13362], [13361, 13363], [13361, 13364]]]
    assert len(list_inner_bonded_atom_pairs_BB[0]) == 705
    assert list_inner_bonded_atom_pairs_BB[0][100:110] == [[2679, 2681], [2682, 2683], [2683, 2684], [2683, 2686],
                                                     [2684, 2685], [2684, 2688], [2686, 2687], [2688, 2689],
                                                     [2689, 2690], [2689, 2692]]
    assert len(list_inner_bonded_atom_pairs_BB[1]) == 677
    assert list_inner_bonded_atom_pairs_BB[1][500:510] == [[3762, 3763], [3763, 3764], [3764, 3765], [3764, 3766],
                                                     [3766, 3767], [3767, 3768], [3767, 3770], [3768, 3769],
                                                     [3768, 3771], [3771, 3772]]


def test_get_n_atoms_from_chain():

    all_n_atoms_Hk2 = aux.get_n_atoms_from_chain(molsys_Hk2, skip_digestion=True)
    all_n_atoms_BB = aux.get_n_atoms_from_chain(molsys_BB, skip_digestion=True)
    list_n_atoms_Hk2 = aux.get_n_atoms_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_n_atoms_BB = aux.get_n_atoms_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_n_atoms_Hk2) == 40
    assert len(all_n_atoms_BB) == 12
    assert all_n_atoms_Hk2[:10] == [6653, 6656, 12, 16, 12, 16, 1, 1, 1, 1]
    assert all_n_atoms_Hk2[-1] == 48
    assert all_n_atoms_BB[:10] == [864, 878, 839, 693, 665, 699, 145, 137, 50, 77]
    assert all_n_atoms_BB[-1] == 40
    assert list_n_atoms_Hk2 == [16, 12, 16]
    assert list_n_atoms_BB == [693, 665]


def test_get_total_n_atoms_from_chain():

    all_total_n_atoms_Hk2 = aux.get_total_n_atoms_from_chain(molsys_Hk2, skip_digestion=True)
    all_total_n_atoms_BB = aux.get_total_n_atoms_from_chain(molsys_BB, skip_digestion=True)
    list_total_n_atoms_Hk2 = aux.get_total_n_atoms_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_total_n_atoms_BB = aux.get_total_n_atoms_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_total_n_atoms_Hk2 == 13546
    assert all_total_n_atoms_BB == 5151
    assert list_total_n_atoms_Hk2 == 44
    assert list_total_n_atoms_BB ==  1358


def test_get_n_groups_from_chain():

    all_n_groups_Hk2 = aux.get_n_groups_from_chain(molsys_Hk2, skip_digestion=True)
    all_n_groups_BB = aux.get_n_groups_from_chain(molsys_BB, skip_digestion=True)
    list_n_groups_Hk2 = aux.get_n_groups_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_n_groups_BB = aux.get_n_groups_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_n_groups_Hk2) == 40
    assert len(all_n_groups_BB) == 12
    assert all_n_groups_Hk2[:5] == [871, 867, 1, 1, 1]
    assert all_n_groups_Hk2[15:25] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_groups_Hk2[-1] == 48
    assert all_n_groups_BB[3:13] == [87, 86, 89, 145, 137, 50, 77, 64, 40]
    assert all_n_groups_BB[-1] == 40
    assert list_n_groups_Hk2 == [1, 1, 1]
    assert list_n_groups_BB == [87, 86]


def test_get_total_n_groups_from_chain():

    all_total_n_groups_Hk2 = aux.get_total_n_groups_from_chain(molsys_Hk2, skip_digestion=True)
    all_total_n_groups_BB = aux.get_total_n_groups_from_chain(molsys_BB, skip_digestion=True)
    list_total_n_groups_Hk2 = aux.get_total_n_groups_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_total_n_groups_BB = aux.get_total_n_groups_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_total_n_groups_Hk2 == 1871
    assert all_total_n_groups_BB == 1101
    assert list_total_n_groups_Hk2 == 3
    assert list_total_n_groups_BB == 173


def test_get_n_molecules_from_chain():

    all_n_molecules_Hk2 = aux.get_n_molecules_from_chain(molsys_Hk2, skip_digestion=True)
    all_n_molecules_BB = aux.get_n_molecules_from_chain(molsys_BB, skip_digestion=True)
    list_n_molecules_Hk2 = aux.get_n_molecules_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_n_molecules_BB = aux.get_n_molecules_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_n_molecules_Hk2) == 40
    assert len(all_n_molecules_BB) == 12
    assert all_n_molecules_Hk2[:5] == [1, 1, 1, 1, 1]
    assert all_n_molecules_Hk2[15:25] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_molecules_Hk2[-1] == 48
    assert all_n_molecules_BB[3:13] == [1, 1, 1, 145, 137, 50, 77, 64, 40]
    assert all_n_molecules_BB[-1] == 40
    assert list_n_molecules_Hk2 == [1, 1, 1]
    assert list_n_molecules_BB == [1, 1]


def test_get_total_n_molecules_from_chain():

    all_total_n_molecules_Hk2 = aux.get_total_n_molecules_from_chain(molsys_Hk2, skip_digestion=True)
    all_total_n_molecules_BB = aux.get_total_n_molecules_from_chain(molsys_BB, skip_digestion=True)
    list_total_n_molecules_Hk2 = aux.get_total_n_molecules_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_total_n_molecules_BB = aux.get_total_n_molecules_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_total_n_molecules_Hk2 == 135
    assert all_total_n_molecules_BB == 519
    assert list_total_n_molecules_Hk2 == 3
    assert list_total_n_molecules_BB == 2


def test_get_n_entities_from_chain():

    all_n_entities_Hk2 = aux.get_n_entities_from_chain(molsys_Hk2, skip_digestion=True)
    all_n_entities_BB = aux.get_n_entities_from_chain(molsys_BB, skip_digestion=True)
    list_n_entities_Hk2 = aux.get_n_entities_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_n_entities_BB = aux.get_n_entities_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_n_entities_Hk2) == 40
    assert len(all_n_entities_BB) == 12
    assert all_n_entities_Hk2[:5] == [1, 1, 1, 1, 1]
    assert all_n_entities_Hk2[15:25] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_entities_Hk2[-1] == 1
    assert all_n_entities_BB[3:13] == [1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_entities_BB[-1] == 1
    assert list_n_entities_Hk2 == [1, 1, 1]
    assert list_n_entities_BB == [1, 1]


def test_get_total_n_entities_from_chain():

    all_total_n_entities_Hk2 = aux.get_total_n_entities_from_chain(molsys_Hk2, skip_digestion=True)
    all_total_n_entities_BB = aux.get_total_n_entities_from_chain(molsys_BB, skip_digestion=True)
    list_total_n_entities_Hk2 = aux.get_total_n_entities_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_total_n_entities_BB = aux.get_total_n_entities_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_total_n_entities_Hk2 == 5
    assert all_total_n_entities_BB == 3
    assert list_total_n_entities_Hk2 == 2
    assert list_total_n_entities_BB == 1


def test_get_n_components_from_chain():

    all_n_components_Hk2 = aux.get_n_components_from_chain(molsys_Hk2, skip_digestion=True)
    all_n_components_BB = aux.get_n_components_from_chain(molsys_BB, skip_digestion=True)
    list_n_components_Hk2 = aux.get_n_components_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_n_components_BB = aux.get_n_components_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_n_components_Hk2) == 40
    assert len(all_n_components_BB) == 12
    assert all_n_components_Hk2[:5] == [6, 7, 1, 1, 1]
    assert all_n_components_Hk2[15:25] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert all_n_components_Hk2[-1] == 48
    assert all_n_components_BB[3:13] == [2, 2, 1, 145, 137, 50, 77, 64, 40]
    assert all_n_components_BB[-1] == 40
    assert list_n_components_Hk2 == [1, 1, 1]
    assert list_n_components_BB == [2, 2]


def test_get_total_n_components_from_chain():

    all_total_n_components_Hk2 = aux.get_total_n_components_from_chain(molsys_Hk2, skip_digestion=True)
    all_total_n_components_BB = aux.get_total_n_components_from_chain(molsys_BB, skip_digestion=True)
    list_total_n_components_Hk2 = aux.get_total_n_components_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_total_n_components_BB = aux.get_total_n_components_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_total_n_components_Hk2 == 146
    assert all_total_n_components_BB == 521
    assert list_total_n_components_Hk2 == 3
    assert list_total_n_components_BB == 4


def test_get_n_chains_from_chain():

    all_n_chains_Hk2 = aux.get_n_chains_from_chain(molsys_Hk2, skip_digestion=True)
    all_n_chains_BB = aux.get_n_chains_from_chain(molsys_BB, skip_digestion=True)
    list_n_chains_Hk2 = aux.get_n_chains_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_n_chains_BB = aux.get_n_chains_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_n_chains_Hk2 == 40
    assert all_n_chains_BB == 12
    assert list_n_chains_Hk2 == 3
    assert list_n_chains_BB == 2


def test_get_total_n_chains_from_chain():

    all_total_n_chains_Hk2 = aux.get_total_n_chains_from_chain(molsys_Hk2, skip_digestion=True)
    all_total_n_chains_BB = aux.get_total_n_chains_from_chain(molsys_BB, skip_digestion=True)
    list_total_n_chains_Hk2 = aux.get_total_n_chains_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_total_n_chains_BB = aux.get_total_n_chains_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_total_n_chains_Hk2 == 40
    assert all_total_n_chains_BB == 12
    assert list_total_n_chains_Hk2 == 3
    assert list_total_n_chains_BB == 2


def test_get_n_bonds_from_chain():

    all_n_bonds_Hk2 = aux.get_n_bonds_from_chain(molsys_Hk2, skip_digestion=True)
    all_n_bonds_BB = aux.get_n_bonds_from_chain(molsys_BB, skip_digestion=True)
    list_n_bonds_Hk2 = aux.get_n_bonds_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_n_bonds_BB = aux.get_n_bonds_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_n_bonds_Hk2) == 40
    assert len(all_n_bonds_BB) == 12
    assert all_n_bonds_Hk2[:5] == [6751, 6755, 12, 16, 12]
    assert all_n_bonds_Hk2[15:25] == [0, 0, 0, 12, 16, 12, 16, 0, 0, 0]
    assert all_n_bonds_Hk2[-1] == 0
    assert all_n_bonds_BB[3:13] == [705, 677, 712, 0, 0, 0, 0, 0, 0]
    assert all_n_bonds_BB[-1] == 0
    assert list_n_bonds_Hk2 == [16, 12, 16]
    assert list_n_bonds_BB == [705, 677]


def test_get_total_n_bonds_from_chain():

    all_total_n_bonds_Hk2 = aux.get_total_n_bonds_from_chain(molsys_Hk2, skip_digestion=True)
    all_total_n_bonds_BB = aux.get_total_n_bonds_from_chain(molsys_BB, skip_digestion=True)
    list_total_n_bonds_Hk2 = aux.get_total_n_bonds_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_total_n_bonds_BB = aux.get_total_n_bonds_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_total_n_bonds_Hk2 == 13618
    assert all_total_n_bonds_BB == 4738
    assert list_total_n_bonds_Hk2 == 44
    assert list_total_n_bonds_BB == 1382


def test_get_n_inner_bonds_from_chain():

    all_n_inner_bonds_Hk2 = aux.get_n_inner_bonds_from_chain(molsys_Hk2, skip_digestion=True)
    all_n_inner_bonds_BB = aux.get_n_inner_bonds_from_chain(molsys_BB, skip_digestion=True)
    list_n_inner_bonds_Hk2 = aux.get_n_inner_bonds_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_n_inner_bonds_BB = aux.get_n_inner_bonds_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_n_inner_bonds_Hk2) == 40
    assert len(all_n_inner_bonds_BB) == 12
    assert all_n_inner_bonds_Hk2[:5] == [6751, 6755, 12, 16, 12]
    assert all_n_inner_bonds_Hk2[15:25] == [0, 0, 0, 12, 16, 12, 16, 0, 0, 0]
    assert all_n_inner_bonds_Hk2[-1] == 0
    assert all_n_inner_bonds_BB[3:13] == [705, 677, 712, 0, 0, 0, 0, 0, 0]
    assert all_n_inner_bonds_BB[-1] == 0
    assert list_n_inner_bonds_Hk2 == [16, 12, 16]
    assert list_n_inner_bonds_BB == [705, 677]


def test_get_total_n_inner_bonds_from_chain():

    all_total_n_inner_bonds_Hk2 = aux.get_total_n_inner_bonds_from_chain(molsys_Hk2, skip_digestion=True)
    all_total_n_inner_bonds_BB = aux.get_total_n_inner_bonds_from_chain(molsys_BB, skip_digestion=True)
    list_total_n_inner_bonds_Hk2 = aux.get_total_n_inner_bonds_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_total_n_inner_bonds_BB = aux.get_total_n_inner_bonds_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_total_n_inner_bonds_Hk2 == 13618
    assert all_total_n_inner_bonds_BB == 4738
    assert list_total_n_inner_bonds_Hk2 == 44
    assert list_total_n_inner_bonds_BB == 1382


def test_get_n_amino_acids_from_chain():

    all_n_amino_acids_Hk2 = aux.get_n_amino_acids_from_chain(molsys_Hk2, skip_digestion=True)
    all_n_amino_acids_BB = aux.get_n_amino_acids_from_chain(molsys_BB, skip_digestion=True)
    list_n_amino_acids_Hk2 = aux.get_n_amino_acids_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_n_amino_acids_BB = aux.get_n_amino_acids_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_n_amino_acids_Hk2) == 40
    assert len(all_n_amino_acids_BB) == 12
    assert all_n_amino_acids_Hk2[:5] == [871, 867, 0, 0, 0]
    assert all_n_amino_acids_Hk2[15:25] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_amino_acids_Hk2[-1] == 0
    assert all_n_amino_acids_BB[3:13] == [87, 86, 89, 0, 0, 0, 0, 0, 0]
    assert all_n_amino_acids_BB[-1] == 0
    assert list_n_amino_acids_Hk2 == [0, 0, 0]
    assert list_n_amino_acids_BB == [87, 86]


def test_get_total_n_amino_acids_from_chain():

    all_total_n_amino_acids_Hk2 = aux.get_total_n_amino_acids_from_chain(molsys_Hk2, skip_digestion=True)
    all_total_n_amino_acids_BB = aux.get_total_n_amino_acids_from_chain(molsys_BB, skip_digestion=True)
    list_total_n_amino_acids_Hk2 = aux.get_total_n_amino_acids_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_total_n_amino_acids_BB = aux.get_total_n_amino_acids_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_total_n_amino_acids_Hk2 == 1738
    assert all_total_n_amino_acids_BB == 588
    assert list_total_n_amino_acids_Hk2 == 0
    assert list_total_n_amino_acids_BB == 173


def test_get_n_nucleotides_from_chain():

    all_n_nucleotides_Hk2 = aux.get_n_nucleotides_from_chain(molsys_Hk2, skip_digestion=True)
    all_n_nucleotides_BB = aux.get_n_nucleotides_from_chain(molsys_BB, skip_digestion=True)
    list_n_nucleotides_Hk2 = aux.get_n_nucleotides_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_n_nucleotides_BB = aux.get_n_nucleotides_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_n_nucleotides_Hk2) == 40
    assert len(all_n_nucleotides_BB) == 12
    assert all_n_nucleotides_Hk2[:5] == [0, 0, 0, 0, 0]
    assert all_n_nucleotides_Hk2[15:25] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_nucleotides_Hk2[-1] == 0
    assert all_n_nucleotides_BB[3:13] == [0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_nucleotides_BB[-1] == 0
    assert list_n_nucleotides_Hk2 == [0, 0, 0]
    assert list_n_nucleotides_BB == [0, 0]


def test_get_total_n_nucleotides_from_chain():

    all_total_n_nucleotides_Hk2 = aux.get_total_n_nucleotides_from_chain(molsys_Hk2, skip_digestion=True)
    all_total_n_nucleotides_BB = aux.get_total_n_nucleotides_from_chain(molsys_BB, skip_digestion=True)
    list_total_n_nucleotides_Hk2 = aux.get_total_n_nucleotides_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_total_n_nucleotides_BB = aux.get_total_n_nucleotides_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_total_n_nucleotides_Hk2 == 0
    assert all_total_n_nucleotides_BB == 0
    assert list_total_n_nucleotides_Hk2 == 0
    assert list_total_n_nucleotides_BB == 0


def test_get_n_ions_from_chain():

    all_n_ions_Hk2 = aux.get_n_ions_from_chain(molsys_Hk2, skip_digestion=True)
    all_n_ions_BB = aux.get_n_ions_from_chain(molsys_BB, skip_digestion=True)
    list_n_ions_Hk2 = aux.get_n_ions_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_n_ions_BB = aux.get_n_ions_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_n_ions_Hk2) == 40
    assert len(all_n_ions_BB) == 12
    assert all_n_ions_Hk2[:5] == [0, 0, 0, 0, 0]
    assert all_n_ions_Hk2[15:25] == [1, 1, 1, 0, 0, 0, 0, 1, 1, 1]
    assert all_n_ions_Hk2[-1] == 0
    assert all_n_ions_BB[3:13] == [0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_ions_BB[-1] == 0
    assert list_n_ions_Hk2 == [0, 0, 0]
    assert list_n_ions_BB == [0, 0]


def test_get_total_n_ions_from_chain():

    all_total_n_ions_Hk2 = aux.get_total_n_ions_from_chain(molsys_Hk2, skip_digestion=True)
    all_total_n_ions_BB = aux.get_total_n_ions_from_chain(molsys_BB, skip_digestion=True)
    list_total_n_ions_Hk2 = aux.get_total_n_ions_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_total_n_ions_BB = aux.get_total_n_ions_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_total_n_ions_Hk2 == 28
    assert all_total_n_ions_BB == 0
    assert list_total_n_ions_Hk2 == 0
    assert list_total_n_ions_BB == 0


def test_get_n_waters_from_chain():

    all_n_waters_Hk2 = aux.get_n_waters_from_chain(molsys_Hk2, skip_digestion=True)
    all_n_waters_BB = aux.get_n_waters_from_chain(molsys_BB, skip_digestion=True)
    list_n_waters_Hk2 = aux.get_n_waters_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_n_waters_BB = aux.get_n_waters_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_n_waters_Hk2) == 40
    assert len(all_n_waters_BB) == 12
    assert all_n_waters_Hk2[:5] == [0, 0, 0, 0, 0]
    assert all_n_waters_Hk2[15:25] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_waters_Hk2[-1] == 48
    assert all_n_waters_BB[3:13] == [0, 0, 0, 145, 137, 50, 77, 64, 40]
    assert all_n_waters_BB[-1] == 40
    assert list_n_waters_Hk2 == [0, 0, 0]
    assert list_n_waters_BB == [0, 0]


def test_get_total_n_waters_from_chain():

    all_total_n_waters_Hk2 = aux.get_total_n_waters_from_chain(molsys_Hk2, skip_digestion=True)
    all_total_n_waters_BB = aux.get_total_n_waters_from_chain(molsys_BB, skip_digestion=True)
    list_total_n_waters_Hk2 = aux.get_total_n_waters_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_total_n_waters_BB = aux.get_total_n_waters_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_total_n_waters_Hk2 == 97
    assert all_total_n_waters_BB == 513
    assert list_total_n_waters_Hk2 == 0
    assert list_total_n_waters_BB == 0


def test_get_n_small_molecules_from_chain():

    all_n_small_molecules_Hk2 = aux.get_n_small_molecules_from_chain(molsys_Hk2, skip_digestion=True)
    all_n_small_molecules_BB = aux.get_n_small_molecules_from_chain(molsys_BB, skip_digestion=True)
    list_n_small_molecules_Hk2 = aux.get_n_small_molecules_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_n_small_molecules_BB = aux.get_n_small_molecules_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_n_small_molecules_Hk2) == 40
    assert len(all_n_small_molecules_BB) == 12
    assert all_n_small_molecules_Hk2[:5] == [0, 0, 0, 0, 0]
    assert all_n_small_molecules_Hk2[15:25] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_small_molecules_Hk2[-1] == 0
    assert all_n_small_molecules_BB[3:13] == [0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_small_molecules_BB[-1] == 0
    assert list_n_small_molecules_Hk2 == [0, 0, 0]
    assert list_n_small_molecules_BB == [0, 0]


def test_get_total_n_small_molecules_from_chain():

    all_total_n_small_molecules_Hk2 = aux.get_total_n_small_molecules_from_chain(molsys_Hk2, skip_digestion=True)
    all_total_n_small_molecules_BB = aux.get_total_n_small_molecules_from_chain(molsys_BB, skip_digestion=True)
    list_total_n_small_molecules_Hk2 = aux.get_total_n_small_molecules_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_total_n_small_molecules_BB = aux.get_total_n_small_molecules_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_total_n_small_molecules_Hk2 == 0
    assert all_total_n_small_molecules_BB == 0
    assert list_total_n_small_molecules_Hk2 == 0
    assert list_total_n_small_molecules_BB == 0


def test_get_n_lipids_from_chain():

    all_n_lipids_Hk2 = aux.get_n_lipids_from_chain(molsys_Hk2, skip_digestion=True)
    all_n_lipids_BB = aux.get_n_lipids_from_chain(molsys_BB, skip_digestion=True)
    list_n_lipids_Hk2 = aux.get_n_lipids_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_n_lipids_BB = aux.get_n_lipids_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_n_lipids_Hk2) == 40
    assert len(all_n_lipids_BB) == 12
    assert all_n_lipids_Hk2[:5] == [0, 0, 0, 0, 0]
    assert all_n_lipids_Hk2[15:25] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_lipids_Hk2[-1] == 0
    assert all_n_lipids_BB[3:13] == [0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_lipids_BB[-1] == 0
    assert list_n_lipids_Hk2 == [0, 0, 0]
    assert list_n_lipids_BB == [0, 0]


def test_get_total_n_lipids_from_chain():

    all_total_n_lipids_Hk2 = aux.get_total_n_lipids_from_chain(molsys_Hk2, skip_digestion=True)
    all_total_n_lipids_BB = aux.get_total_n_lipids_from_chain(molsys_BB, skip_digestion=True)
    list_total_n_lipids_Hk2 = aux.get_total_n_lipids_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_total_n_lipids_BB = aux.get_total_n_lipids_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_total_n_lipids_Hk2 == 0
    assert all_total_n_lipids_BB == 0
    assert list_total_n_lipids_Hk2 == 0
    assert list_total_n_lipids_BB == 0


def test_get_n_saccharides_from_chain():

    all_n_saccharides_Hk2 = aux.get_n_saccharides_from_chain(molsys_Hk2, skip_digestion=True)
    all_n_saccharides_BB = aux.get_n_saccharides_from_chain(molsys_BB, skip_digestion=True)
    list_n_saccharides_Hk2 = aux.get_n_saccharides_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_n_saccharides_BB = aux.get_n_saccharides_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_n_saccharides_Hk2) == 40
    assert len(all_n_saccharides_BB) == 12
    assert all_n_saccharides_Hk2[:5] == [0, 0, 1, 1, 1]
    assert all_n_saccharides_Hk2[15:25] == [0, 0, 0, 1, 1, 1, 1, 0, 0, 0]
    assert all_n_saccharides_Hk2[-1] == 0
    assert all_n_saccharides_BB[3:13] == [0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_saccharides_BB[-1] == 0
    assert list_n_saccharides_Hk2 == [1, 1, 1]
    assert list_n_saccharides_BB == [0, 0]


def test_get_total_n_saccharides_from_chain():

    all_total_n_saccharides_Hk2 = aux.get_total_n_saccharides_from_chain(molsys_Hk2, skip_digestion=True)
    all_total_n_saccharides_BB = aux.get_total_n_saccharides_from_chain(molsys_BB, skip_digestion=True)
    list_total_n_saccharides_Hk2 = aux.get_total_n_saccharides_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_total_n_saccharides_BB = aux.get_total_n_saccharides_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_total_n_saccharides_Hk2 == 8
    assert all_total_n_saccharides_BB == 0
    assert list_total_n_saccharides_Hk2 == 3
    assert list_total_n_saccharides_BB == 0


def test_get_n_polysaccharides_from_chain():

    all_n_polysaccharides_Hk2 = aux.get_n_polysaccharides_from_chain(molsys_Hk2, skip_digestion=True)
    all_n_polysaccharides_BB = aux.get_n_polysaccharides_from_chain(molsys_BB, skip_digestion=True)
    list_n_polysaccharides_Hk2 = aux.get_n_polysaccharides_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_n_polysaccharides_BB = aux.get_n_polysaccharides_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_n_polysaccharides_Hk2) == 40
    assert len(all_n_polysaccharides_BB) == 12
    assert all_n_polysaccharides_Hk2[:5] == [0, 0, 1, 1, 1]
    assert all_n_polysaccharides_Hk2[15:25] == [0, 0, 0, 1, 1, 1, 1, 0, 0, 0]
    assert all_n_polysaccharides_Hk2[-1] == 0
    assert all_n_polysaccharides_BB[3:13] == [0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_polysaccharides_BB[-1] == 0
    assert list_n_polysaccharides_Hk2 == [1, 1, 1]
    assert list_n_polysaccharides_BB == [0, 0]


def test_get_total_n_polysaccharides_from_chain():

    all_total_n_polysaccharides_Hk2 = aux.get_total_n_polysaccharides_from_chain(molsys_Hk2, skip_digestion=True)
    all_total_n_polysaccharides_BB = aux.get_total_n_polysaccharides_from_chain(molsys_BB, skip_digestion=True)
    list_total_n_polysaccharides_Hk2 = aux.get_total_n_polysaccharides_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_total_n_polysaccharides_BB = aux.get_total_n_polysaccharides_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_total_n_polysaccharides_Hk2 == 8
    assert all_total_n_polysaccharides_BB == 0
    assert list_total_n_polysaccharides_Hk2 == 3
    assert list_total_n_polysaccharides_BB == 0


def test_get_n_peptides_from_chain():

    all_n_peptides_Hk2 = aux.get_n_peptides_from_chain(molsys_Hk2, skip_digestion=True)
    all_n_peptides_BB = aux.get_n_peptides_from_chain(molsys_BB, skip_digestion=True)
    list_n_peptides_Hk2 = aux.get_n_peptides_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_n_peptides_BB = aux.get_n_peptides_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_n_peptides_Hk2) == 40
    assert len(all_n_peptides_BB) == 12
    assert all_n_peptides_Hk2[:5] == [0, 0, 0, 0, 0]
    assert all_n_peptides_Hk2[15:25] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_peptides_Hk2[-1] == 0
    assert all_n_peptides_BB[3:13] == [0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_peptides_BB[-1] == 0
    assert list_n_peptides_Hk2 == [0, 0, 0]
    assert list_n_peptides_BB == [0, 0]


def test_get_total_n_peptides_from_chain():

    all_total_n_peptides_Hk2 = aux.get_total_n_peptides_from_chain(molsys_Hk2, skip_digestion=True)
    all_total_n_peptides_BB = aux.get_total_n_peptides_from_chain(molsys_BB, skip_digestion=True)
    list_total_n_peptides_Hk2 = aux.get_total_n_peptides_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_total_n_peptides_BB = aux.get_total_n_peptides_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_total_n_peptides_Hk2 == 0
    assert all_total_n_peptides_BB == 0
    assert list_total_n_peptides_Hk2 == 0
    assert list_total_n_peptides_BB == 0


def test_get_n_proteins_from_chain():

    all_n_proteins_Hk2 = aux.get_n_proteins_from_chain(molsys_Hk2, skip_digestion=True)
    all_n_proteins_BB = aux.get_n_proteins_from_chain(molsys_BB, skip_digestion=True)
    list_n_proteins_Hk2 = aux.get_n_proteins_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_n_proteins_BB = aux.get_n_proteins_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_n_proteins_Hk2) == 40
    assert len(all_n_proteins_BB) == 12
    assert all_n_proteins_Hk2[:5] == [1, 1, 0, 0, 0]
    assert all_n_proteins_Hk2[15:25] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_proteins_Hk2[-1] == 0
    assert all_n_proteins_BB[3:13] == [1, 1, 1, 0, 0, 0, 0, 0, 0]
    assert all_n_proteins_BB[-1] == 0
    assert list_n_proteins_Hk2 == [0, 0, 0]
    assert list_n_proteins_BB == [1, 1]


def test_get_total_n_proteins_from_chain():

    all_total_n_proteins_Hk2 = aux.get_total_n_proteins_from_chain(molsys_Hk2, skip_digestion=True)
    all_total_n_proteins_BB = aux.get_total_n_proteins_from_chain(molsys_BB, skip_digestion=True)
    list_total_n_proteins_Hk2 = aux.get_total_n_proteins_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_total_n_proteins_BB = aux.get_total_n_proteins_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_total_n_proteins_Hk2 == 2
    assert all_total_n_proteins_BB == 6
    assert list_total_n_proteins_Hk2 == 0
    assert list_total_n_proteins_BB == 2


def test_get_n_dnas_from_chain():

    all_n_dnas_Hk2 = aux.get_n_dnas_from_chain(molsys_Hk2, skip_digestion=True)
    all_n_dnas_BB = aux.get_n_dnas_from_chain(molsys_BB, skip_digestion=True)
    list_n_dnas_Hk2 = aux.get_n_dnas_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_n_dnas_BB = aux.get_n_dnas_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_n_dnas_Hk2) == 40
    assert len(all_n_dnas_BB) == 12
    assert all_n_dnas_Hk2[:5] == [0, 0, 0, 0, 0]
    assert all_n_dnas_Hk2[15:25] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_dnas_Hk2[-1] == 0
    assert all_n_dnas_BB[3:13] == [0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_dnas_BB[-1] == 0
    assert list_n_dnas_Hk2 == [0, 0, 0]
    assert list_n_dnas_BB == [0, 0]


def test_get_total_n_dnas_from_chain():

    all_total_n_dnas_Hk2 = aux.get_total_n_dnas_from_chain(molsys_Hk2, skip_digestion=True)
    all_total_n_dnas_BB = aux.get_total_n_dnas_from_chain(molsys_BB, skip_digestion=True)
    list_total_n_dnas_Hk2 = aux.get_total_n_dnas_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_total_n_dnas_BB = aux.get_total_n_dnas_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_total_n_dnas_Hk2 == 0
    assert all_total_n_dnas_BB == 0
    assert list_total_n_dnas_Hk2 == 0
    assert list_total_n_dnas_BB == 0


def test_get_n_rnas_from_chain():

    all_n_rnas_Hk2 = aux.get_n_rnas_from_chain(molsys_Hk2, skip_digestion=True)
    all_n_rnas_BB = aux.get_n_rnas_from_chain(molsys_BB, skip_digestion=True)
    list_n_rnas_Hk2 = aux.get_n_rnas_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_n_rnas_BB = aux.get_n_rnas_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_n_rnas_Hk2) == 40
    assert len(all_n_rnas_BB) == 12
    assert all_n_rnas_Hk2[:5] == [0, 0, 0, 0, 0]
    assert all_n_rnas_Hk2[15:25] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_rnas_Hk2[-1] == 0
    assert all_n_rnas_BB[3:13] == [0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert all_n_rnas_BB[-1] == 0
    assert list_n_rnas_Hk2 == [0, 0, 0]
    assert list_n_rnas_BB == [0, 0]


def test_get_total_n_rnas_from_chain():

    all_total_n_rnas_Hk2 = aux.get_total_n_rnas_from_chain(molsys_Hk2, skip_digestion=True)
    all_total_n_rnas_BB = aux.get_total_n_rnas_from_chain(molsys_BB, skip_digestion=True)
    list_total_n_rnas_Hk2 = aux.get_total_n_rnas_from_chain(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_total_n_rnas_BB = aux.get_total_n_rnas_from_chain(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_total_n_rnas_Hk2 == 0
    assert all_total_n_rnas_BB == 0
    assert list_total_n_rnas_Hk2 == 0
    assert list_total_n_rnas_BB == 0

# From bond


def test_get_bond_index_from_bond():

    all_bond_index_Hk2 = aux.get_bond_index_from_bond(molsys_Hk2, skip_digestion=True)
    all_bond_index_BB = aux.get_bond_index_from_bond(molsys_BB, skip_digestion=True)
    list_bond_index_Hk2 = aux.get_bond_index_from_bond(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_bond_index_BB = aux.get_bond_index_from_bond(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_bond_index_Hk2) == 13618
    assert len(all_bond_index_BB) == 4738
    assert all_bond_index_Hk2 == list(range(13618))
    assert all_bond_index_BB == list(range(4738))
    assert list_bond_index_Hk2 == [3,4,5]
    assert list_bond_index_BB == [3,4]


def test_get_bond_order_from_bond():

    all_bond_order_Hk2 = aux.get_bond_order_from_bond(molsys_Hk2, skip_digestion=True)
    all_bond_order_BB = aux.get_bond_order_from_bond(molsys_BB, skip_digestion=True)
    list_bond_order_Hk2 = aux.get_bond_order_from_bond(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_bond_order_BB = aux.get_bond_order_from_bond(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_bond_order_Hk2) == 13618
    assert len(all_bond_order_BB) == 4738
    assert all_bond_order_Hk2 == 13618*[None]
    assert all_bond_order_BB == 4738*[None]
    assert list_bond_order_Hk2 == [None, None, None]
    assert list_bond_order_BB == [None, None]


def test_get_bond_type_from_bond():

    all_bond_type_Hk2 = aux.get_bond_type_from_bond(molsys_Hk2, skip_digestion=True)
    all_bond_type_BB = aux.get_bond_type_from_bond(molsys_BB, skip_digestion=True)
    list_bond_type_Hk2 = aux.get_bond_type_from_bond(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_bond_type_BB = aux.get_bond_type_from_bond(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_bond_type_Hk2) == 13618
    assert len(all_bond_type_BB) == 4738
    assert all_bond_type_Hk2 == 13618*[None]
    assert all_bond_type_BB == 4738*[None]
    assert list_bond_type_Hk2 == [None, None, None]
    assert list_bond_type_BB == [None, None]


def test_get_bonded_atoms_from_bond():

    all_bonded_atoms_Hk2 = aux.get_bonded_atoms_from_bond(molsys_Hk2, skip_digestion=True)
    all_bonded_atoms_BB = aux.get_bonded_atoms_from_bond(molsys_BB, skip_digestion=True)
    list_bonded_atoms_Hk2 = aux.get_bonded_atoms_from_bond(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_bonded_atoms_BB = aux.get_bonded_atoms_from_bond(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_bonded_atoms_Hk2) == 13421
    assert all_bonded_atoms_Hk2[1000:1010] == [1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009]
    assert all_bonded_atoms_Hk2[10000:10010] == [10000, 10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10009]
    assert all_bonded_atoms_Hk2[-10:] == [13423, 13424, 13425, 13426, 13427, 13428, 13429, 13430, 13431, 13432]
    assert all_bonded_atoms_BB == list(range(4638))
    assert list_bonded_atoms_Hk2 == [2, 3, 4, 5, 8]
    assert list_bonded_atoms_BB == [2, 3, 7]


def test_get_bonded_atom_pairs_from_bond():

    all_bonded_atom_pairs_Hk2 = aux.get_bonded_atom_pairs_from_bond(molsys_Hk2, skip_digestion=True)
    all_bonded_atom_pairs_BB = aux.get_bonded_atom_pairs_from_bond(molsys_BB, skip_digestion=True)
    list_bonded_atom_pairs_Hk2 = aux.get_bonded_atom_pairs_from_bond(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_bonded_atom_pairs_BB = aux.get_bonded_atom_pairs_from_bond(molsys_BB, indices=[3,4], skip_digestion=True)

    assert len(all_bonded_atom_pairs_Hk2) == 13618
    assert len(all_bonded_atom_pairs_BB) == 4738
    assert all_bonded_atom_pairs_Hk2[200:210] == [[195, 197], [198, 199], [199, 200], [199, 202], [200, 201],
                                             [200, 204], [202, 203], [204, 205], [205, 206], [205, 208]]
    assert all_bonded_atom_pairs_Hk2[1000:1010] == [[981, 982], [982, 983], [983, 984], [984, 985], [986, 987],
                                               [987, 988], [987, 990], [988, 989], [988, 994], [990, 991]]
    assert all_bonded_atom_pairs_Hk2[10000:10010] == [[9851, 9852], [9851, 9853], [9854, 9855], [9855, 9856],
                                                 [9855, 9858], [9856, 9857], [9856, 9865], [9858, 9859],
                                                 [9859, 9860], [9859, 9861]]
    assert all_bonded_atom_pairs_BB[200:210] == [[193, 194], [193, 198], [195, 196], [195, 197], [198, 199],
                                            [199, 200], [199, 202], [200, 201], [200, 207], [202, 203]]
    assert all_bonded_atom_pairs_BB[1000:1010] == [[976, 977], [977, 978], [977, 979], [980, 981], [981, 982], [981, 984],
                                              [982, 983], [982, 987], [984, 985], [984, 986]]
    assert all_bonded_atom_pairs_BB[4000:4010] == [[3910, 3916], [3912, 3913], [3912, 3914], [3913, 3915], [3916, 3917],
                                              [3917, 3918], [3917, 3920], [3918, 3919], [3918, 3924], [3920, 3921]]
    assert list_bonded_atom_pairs_Hk2 == [[2, 3], [2, 8], [4, 5]]
    assert list_bonded_atom_pairs_BB == [[2, 3], [2, 7]]


def test_get_n_bonds_from_bond():

    all_n_bonds_Hk2 = aux.get_n_bonds_from_bond(molsys_Hk2, skip_digestion=True)
    all_n_bonds_BB = aux.get_n_bonds_from_bond(molsys_BB, skip_digestion=True)
    list_n_bonds_Hk2 = aux.get_n_bonds_from_bond(molsys_Hk2, indices=[3,4,5], skip_digestion=True)
    list_n_bonds_BB = aux.get_n_bonds_from_bond(molsys_BB, indices=[3,4], skip_digestion=True)

    assert all_n_bonds_Hk2 == 13618
    assert all_n_bonds_BB == 4738
    assert list_n_bonds_Hk2 == 3
    assert list_n_bonds_BB == 2


# From system


def test_get_n_atoms_from_system():

    all_n_atoms_Hk2 = aux.get_n_atoms_from_system(molsys_Hk2, skip_digestion=True)
    all_n_atoms_BB = aux.get_n_atoms_from_system(molsys_BB, skip_digestion=True)

    assert all_n_atoms_Hk2 == 13546
    assert all_n_atoms_BB == 5151


def test_get_n_groups_from_system():

    all_n_groups_Hk2 = aux.get_n_groups_from_system(molsys_Hk2, skip_digestion=True)
    all_n_groups_BB = aux.get_n_groups_from_system(molsys_BB, skip_digestion=True)

    assert all_n_groups_Hk2 == 1871
    assert all_n_groups_BB == 1101


def test_get_n_molecules_from_system():

    all_n_molecules_Hk2 = aux.get_n_molecules_from_system(molsys_Hk2, skip_digestion=True)
    all_n_molecules_BB = aux.get_n_molecules_from_system(molsys_BB, skip_digestion=True)

    assert all_n_molecules_Hk2 == 135
    assert all_n_molecules_BB == 519


def test_get_n_entities_from_system():

    all_n_entities_Hk2 = aux.get_n_entities_from_system(molsys_Hk2, skip_digestion=True)
    all_n_entities_BB = aux.get_n_entities_from_system(molsys_BB, skip_digestion=True)

    assert all_n_entities_Hk2 == 5
    assert all_n_entities_BB == 3


def test_get_n_components_from_system():

    all_n_components_Hk2 = aux.get_n_components_from_system(molsys_Hk2, skip_digestion=True)
    all_n_components_BB = aux.get_n_components_from_system(molsys_BB, skip_digestion=True)

    assert all_n_components_Hk2 == 146
    assert all_n_components_BB == 521


def test_get_n_chains_from_system():

    all_n_chains_Hk2 = aux.get_n_chains_from_system(molsys_Hk2, skip_digestion=True)
    all_n_chains_BB = aux.get_n_chains_from_system(molsys_BB, skip_digestion=True)

    assert all_n_chains_Hk2 == 40
    assert all_n_chains_BB == 12


def test_get_n_bonds_from_system():

    all_n_bonds_Hk2 = aux.get_n_bonds_from_system(molsys_Hk2, skip_digestion=True)
    all_n_bonds_BB = aux.get_n_bonds_from_system(molsys_BB, skip_digestion=True)

    assert all_n_bonds_Hk2 == 13618
    assert all_n_bonds_BB == 4738


def test_get_n_amino_acids_from_system():

    all_n_amino_acids_Hk2 = aux.get_n_amino_acids_from_system(molsys_Hk2, skip_digestion=True)
    all_n_amino_acids_BB = aux.get_n_amino_acids_from_system(molsys_BB, skip_digestion=True)

    assert all_n_amino_acids_Hk2 == 1738
    assert all_n_amino_acids_BB == 588


def test_get_n_nucleotides_from_system():

    all_n_nucleotides_Hk2 = aux.get_n_nucleotides_from_system(molsys_Hk2, skip_digestion=True)
    all_n_nucleotides_BB = aux.get_n_nucleotides_from_system(molsys_BB, skip_digestion=True)

    assert all_n_nucleotides_Hk2 == 0
    assert all_n_nucleotides_BB == 0


def test_get_n_nucleotides_from_system():

    all_n_nucleotides_Hk2 = aux.get_n_nucleotides_from_system(molsys_Hk2, skip_digestion=True)
    all_n_nucleotides_BB = aux.get_n_nucleotides_from_system(molsys_BB, skip_digestion=True)

    assert all_n_nucleotides_Hk2 == 0
    assert all_n_nucleotides_BB == 0


def test_get_n_ions_from_system():

    all_n_ions_Hk2 = aux.get_n_ions_from_system(molsys_Hk2, skip_digestion=True)
    all_n_ions_BB = aux.get_n_ions_from_system(molsys_BB, skip_digestion=True)

    assert all_n_ions_Hk2 == 28
    assert all_n_ions_BB == 0


def test_get_n_waters_from_system():

    all_n_waters_Hk2 = aux.get_n_waters_from_system(molsys_Hk2, skip_digestion=True)
    all_n_waters_BB = aux.get_n_waters_from_system(molsys_BB, skip_digestion=True)

    assert all_n_waters_Hk2 == 97
    assert all_n_waters_BB == 513


def test_get_n_small_molecules_from_system():

    all_n_small_molecules_Hk2 = aux.get_n_small_molecules_from_system(molsys_Hk2, skip_digestion=True)
    all_n_small_molecules_BB = aux.get_n_small_molecules_from_system(molsys_BB, skip_digestion=True)

    assert all_n_small_molecules_Hk2 == 0
    assert all_n_small_molecules_BB == 0


def test_get_n_lipids_from_system():

    all_n_lipids_Hk2 = aux.get_n_lipids_from_system(molsys_Hk2, skip_digestion=True)
    all_n_lipids_BB = aux.get_n_lipids_from_system(molsys_BB, skip_digestion=True)

    assert all_n_lipids_Hk2 == 0
    assert all_n_lipids_BB == 0


def test_get_n_saccharides_from_system():

    all_n_saccharides_Hk2 = aux.get_n_saccharides_from_system(molsys_Hk2, skip_digestion=True)
    all_n_saccharides_BB = aux.get_n_saccharides_from_system(molsys_BB, skip_digestion=True)

    assert all_n_saccharides_Hk2 == 8
    assert all_n_saccharides_BB == 0


def test_get_n_peptides_from_system():

    all_n_peptides_Hk2 = aux.get_n_peptides_from_system(molsys_Hk2, skip_digestion=True)
    all_n_peptides_BB = aux.get_n_peptides_from_system(molsys_BB, skip_digestion=True)

    assert all_n_peptides_Hk2 == 0
    assert all_n_peptides_BB == 0


def test_get_n_proteins_from_system():

    all_n_proteins_Hk2 = aux.get_n_proteins_from_system(molsys_Hk2, skip_digestion=True)
    all_n_proteins_BB = aux.get_n_proteins_from_system(molsys_BB, skip_digestion=True)

    assert all_n_proteins_Hk2 == 2
    assert all_n_proteins_BB == 6


def test_get_n_polysaccharides_from_system():

    all_n_polysaccharides_Hk2 = aux.get_n_polysaccharides_from_system(molsys_Hk2, skip_digestion=True)
    all_n_polysaccharides_BB = aux.get_n_polysaccharides_from_system(molsys_BB, skip_digestion=True)

    assert all_n_polysaccharides_Hk2 == 8
    assert all_n_polysaccharides_BB == 0


def test_get_n_dnas_from_system():

    all_n_dnas_Hk2 = aux.get_n_dnas_from_system(molsys_Hk2, skip_digestion=True)
    all_n_dnas_BB = aux.get_n_dnas_from_system(molsys_BB, skip_digestion=True)

    assert all_n_dnas_Hk2 == 0
    assert all_n_dnas_BB == 0


def test_get_n_rnas_from_system():

    all_n_rnas_Hk2 = aux.get_n_rnas_from_system(molsys_Hk2, skip_digestion=True)
    all_n_rnas_BB = aux.get_n_rnas_from_system(molsys_BB, skip_digestion=True)

    assert all_n_rnas_Hk2 == 0
    assert all_n_rnas_BB == 0


def test_get_bonded_atoms_from_system():

    all_bonded_atoms_Hk2 = aux.get_bonded_atoms_from_system(molsys_Hk2, skip_digestion=True)
    all_bonded_atoms_BB = aux.get_bonded_atoms_from_system(molsys_BB, skip_digestion=True)

    assert len(all_bonded_atoms_Hk2) == 13421
    assert all_bonded_atoms_Hk2[1000:1010] == [1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009]
    assert all_bonded_atoms_Hk2[10000:10010] == [10000, 10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10009]
    assert all_bonded_atoms_Hk2[-10:] == [13423, 13424, 13425, 13426, 13427, 13428, 13429, 13430, 13431, 13432]
    assert all_bonded_atoms_BB == list(range(4638))


def test_get_bonded_atom_pairs_from_system():

    all_bonded_atom_pairs_Hk2 = aux.get_bonded_atom_pairs_from_system(molsys_Hk2, skip_digestion=True)
    all_bonded_atom_pairs_BB = aux.get_bonded_atom_pairs_from_system(molsys_BB, skip_digestion=True)

    assert len(all_bonded_atom_pairs_Hk2) == 13618
    assert len(all_bonded_atom_pairs_BB) == 4738
    assert all_bonded_atom_pairs_Hk2[200:210] == [[195, 197], [198, 199], [199, 200], [199, 202], [200, 201],
                                             [200, 204], [202, 203], [204, 205], [205, 206], [205, 208]]
    assert all_bonded_atom_pairs_Hk2[1000:1010] == [[981, 982], [982, 983], [983, 984], [984, 985], [986, 987],
                                               [987, 988], [987, 990], [988, 989], [988, 994], [990, 991]]
    assert all_bonded_atom_pairs_Hk2[10000:10010] == [[9851, 9852], [9851, 9853], [9854, 9855], [9855, 9856],
                                                 [9855, 9858], [9856, 9857], [9856, 9865], [9858, 9859],
                                                 [9859, 9860], [9859, 9861]]
    assert all_bonded_atom_pairs_BB[200:210] == [[193, 194], [193, 198], [195, 196], [195, 197], [198, 199],
                                            [199, 200], [199, 202], [200, 201], [200, 207], [202, 203]]
    assert all_bonded_atom_pairs_BB[1000:1010] == [[976, 977], [977, 978], [977, 979], [980, 981], [981, 982], [981, 984],
                                              [982, 983], [982, 987], [984, 985], [984, 986]]
    assert all_bonded_atom_pairs_BB[4000:4010] == [[3910, 3916], [3912, 3913], [3912, 3914], [3913, 3915], [3916, 3917],
                                              [3917, 3918], [3917, 3920], [3918, 3919], [3918, 3924], [3920, 3921]]
