import numpy as np

from molsysmt.lib.topology.get_component_index_from_bonded_atom_pairs import get_component_index_from_bonded_atom_pairs


def test_component_indices_cover_isolated_atoms_and_merges():
    bonded = np.array([[0, 1], [1, 2], [4, 5], [7, 8], [8, 9]], dtype=np.int64)
    comp = get_component_index_from_bonded_atom_pairs(bonded, 11)
    assert comp.shape == (11,)
    assert len(np.unique(comp)) == 6
    # 0-1-2 together
    assert len(set(comp[[0, 1, 2]])) == 1
    # 3 isolated
    assert comp[3] not in set(comp[[0,1,2,4,5,7,8,9,10]])
    # 4-5 together
    assert len(set(comp[[4, 5]])) == 1
    # 6 isolated
    assert comp[6] not in set(comp[[0,1,2,4,5,7,8,9,10]])
    # 7-8-9 together
    assert len(set(comp[[7, 8, 9]])) == 1
    # 10 isolated
    assert comp[10] not in set(comp[:10])


def test_component_indices_are_stable_for_empty_bond_list():
    comp = get_component_index_from_bonded_atom_pairs(np.empty((0, 2), dtype=np.int64), 4)
    assert np.array_equal(comp, np.array([0, 1, 2, 3], dtype=np.int64))
