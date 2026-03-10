import numpy as np
import pandas as pd

from molsysmt.native.topology import Topology


def build_minimal_topology():
    topology = Topology(n_atoms=4, n_groups=2, n_components=2, n_molecules=2, n_entities=2, n_chains=2, n_bonds=1)

    topology.atoms['atom_id'] = ['0', '1', '2', '3']
    topology.atoms['atom_name'] = ['N', 'CA', 'O', 'H']
    topology.atoms['atom_type'] = ['N', 'C', 'O', 'H']
    topology.atoms['group_index'] = pd.Series([0, 0, 1, 1], dtype='Int64')
    topology.atoms['component_index'] = pd.Series([0, 0, 1, 1], dtype='Int64')
    topology.atoms['chain_index'] = pd.Series([0, 0, 1, 1], dtype='Int64')

    topology.groups['group_id'] = ['10', '11']
    topology.groups['group_name'] = ['ALA', 'HOH']
    topology.groups['group_type'] = ['amino acid', 'water']
    topology.groups['molecule_index'] = pd.Series([0, 1], dtype='Int64')

    topology.components['component_id'] = ['20', '21']
    topology.components['component_name'] = ['peptide 0', 'water']
    topology.components['component_type'] = ['peptide', 'water']

    topology.molecules['molecule_id'] = ['30', '31']
    topology.molecules['molecule_name'] = ['peptide 0', 'water']
    topology.molecules['molecule_type'] = ['peptide', 'water']
    topology.molecules['entity_index'] = pd.Series([0, 1], dtype='Int64')

    topology.entities['entity_id'] = ['40', '41']
    topology.entities['entity_name'] = ['peptide 0', 'water']
    topology.entities['entity_type'] = ['peptide', 'water']

    topology.chains['chain_id'] = ['A', 'B']
    topology.chains['chain_name'] = ['A', 'B']
    topology.chains['chain_type'] = ['protein', 'water']

    topology.bonds['atom1_index'] = pd.Series([0], dtype='Int64')
    topology.bonds['atom2_index'] = pd.Series([1], dtype='Int64')
    topology.bonds['order'] = ['1']
    topology.bonds['type'] = ['single']

    return topology


def test_reset_dataframe_sizes_and_id_dtypes():
    topology = Topology()

    topology.reset_atoms(3)
    topology.reset_groups(2)
    topology.reset_components(1)
    topology.reset_molecules(1)
    topology.reset_entities(1)
    topology.reset_chains(1)
    topology.reset_bonds(2)

    assert topology.n_atoms == 3
    assert topology.n_groups == 2
    assert topology.n_components == 1
    assert topology.n_molecules == 1
    assert topology.n_entities == 1
    assert topology.n_chains == 1
    assert topology.n_bonds == 2

    assert str(topology.atoms['atom_id'].dtype) == 'string'
    assert str(topology.groups['group_id'].dtype) == 'string'
    assert str(topology.components['component_id'].dtype) == 'string'
    assert str(topology.molecules['molecule_id'].dtype) == 'string'
    assert str(topology.entities['entity_id'].dtype) == 'string'
    assert str(topology.chains['chain_id'].dtype) == 'string'


def test_copy_returns_independent_topology():
    topology = build_minimal_topology()
    cloned = topology.copy()

    cloned.atoms.at[0, 'atom_name'] = 'X'
    cloned.groups.at[0, 'group_name'] = 'GLY'

    assert topology.atoms.at[0, 'atom_name'] == 'N'
    assert topology.groups.at[0, 'group_name'] == 'ALA'


def test_extract_reindexes_hierarchy_and_bonds():
    topology = build_minimal_topology()
    extracted = topology.extract(atom_indices=[0, 1], skip_digestion=True)

    assert extracted.n_atoms == 2
    assert extracted.n_groups == 1
    assert extracted.n_components == 1
    assert extracted.n_molecules == 1
    assert extracted.n_entities == 1
    assert extracted.n_chains == 1
    assert extracted.bonds[['atom1_index', 'atom2_index']].values.tolist() == [[0, 1]]
    assert extracted.atoms['group_index'].tolist() == [0, 0]
    assert extracted.atoms['component_index'].tolist() == [0, 0]
    assert extracted.atoms['chain_index'].tolist() == [0, 0]


def test_remove_returns_topology_without_removed_atoms():
    topology = build_minimal_topology()
    trimmed = topology.remove(atom_indices=[2, 3], skip_digestion=True)

    assert trimmed.n_atoms == 2
    assert trimmed.atoms['atom_id'].tolist() == ['0', '1']
    assert trimmed.n_groups == 1


def test_add_offsets_indices_and_can_rebuild_ids():
    left = build_minimal_topology()
    right = build_minimal_topology()

    left.add(right, keep_ids=False, skip_digestion=True)

    assert left.n_atoms == 8
    assert left.n_groups == 4
    assert left.n_components == 6
    assert left.n_molecules == 4
    assert left.n_entities == 3
    assert left.n_chains == 4
    assert left.n_bonds == 2
    assert left.atoms['group_index'].tolist() == [0, 0, 1, 1, 2, 2, 3, 3]
    assert left.atoms['component_index'].tolist() == [0, 0, 1, 2, 3, 3, 4, 5]
    assert left.bonds[['atom1_index', 'atom2_index']].values.tolist() == [[0, 1], [4, 5]]
    assert left.atoms['atom_id'].map(type).eq(str).all()
    assert left.groups['group_id'].map(type).eq(str).all()
    assert left.molecules['entity_index'].tolist() == [0, 1, 2, 1]


def test_add_bonds_sorts_pairs_and_rebuilds_components():
    topology = build_minimal_topology()
    topology.add_bonds([[3, 2], [2, 1]], skip_digestion=True)

    assert topology.n_bonds == 3
    assert topology.bonds[['atom1_index', 'atom2_index']].values.tolist() == [[0, 1], [1, 2], [2, 3]]
    assert topology.atoms['component_index'].tolist() == [0, 0, 0, 0]


def test_remove_bonds_all_resets_connectivity():
    topology = build_minimal_topology()
    topology.add_bonds([[2, 3]], skip_digestion=True)

    topology.remove_bonds('all', skip_digestion=True)

    assert topology.n_bonds == 0
    assert topology.components.shape[0] == 4
    assert topology.atoms['component_index'].tolist() == [0, 1, 2, 3]


def test_remove_specific_bond_keeps_remaining_bonds():
    topology = build_minimal_topology()
    topology.add_bonds([[2, 3]], skip_digestion=True)

    topology.remove_bonds([0], skip_digestion=True)

    assert topology.bonds[['atom1_index', 'atom2_index']].values.tolist() == [[2, 3]]


def test_fix_null_values_normalizes_id_columns_to_string_dtype():
    topology = build_minimal_topology()
    topology.atoms.at[0, 'atom_id'] = None
    topology.groups.at[0, 'group_id'] = None
    topology.components.at[0, 'component_id'] = None
    topology.molecules.at[0, 'molecule_id'] = None
    topology.entities.at[0, 'entity_id'] = None
    topology.chains.at[0, 'chain_id'] = None

    topology._fix_null_values()

    assert str(topology.atoms['atom_id'].dtype) == 'string'
    assert str(topology.groups['group_id'].dtype) == 'string'
    assert str(topology.components['component_id'].dtype) == 'string'
    assert str(topology.molecules['molecule_id'].dtype) == 'string'
    assert str(topology.entities['entity_id'].dtype) == 'string'
    assert str(topology.chains['chain_id'].dtype) == 'string'


def test_sort_bonds_orders_atom_pairs_in_place():
    topology = build_minimal_topology()
    topology.reset_bonds(2)
    topology.bonds['atom1_index'] = pd.Series([3, 1], dtype='Int64')
    topology.bonds['atom2_index'] = pd.Series([2, 0], dtype='Int64')
    topology.bonds['order'] = ['1', '1']
    topology.bonds['type'] = ['single', 'single']

    topology._sort_bonds()

    assert topology.bonds[['atom1_index', 'atom2_index']].values.tolist() == [[0, 1], [2, 3]]


def test_compare_supports_boolean_and_dictionary_outputs():
    left = build_minimal_topology()
    right = build_minimal_topology()

    result = left.compare(
        right,
        rule='equal',
        output_type='dictionary',
        n_atoms=True,
        atom_id=True,
        atom_name=True,
        atom_type=True,
        n_groups=True,
        group_index=True,
        group_id=True,
        group_name=True,
        group_type=True,
        component_index=True,
        component_id=True,
        component_name=True,
        component_type=True,
        molecule_index=True,
        molecule_id=True,
        molecule_name=True,
        molecule_type=True,
        entity_index=True,
        entity_id=True,
        entity_name=True,
        entity_type=True,
        chain_index=True,
        chain_id=True,
        chain_name=True,
        chain_type=True,
        n_bonds=True,
        bonded_atom_pairs=True,
        skip_digestion=True,
    )

    assert all(result.values())
    assert left.compare(right, rule='equal', output_type='boolean', atom_name=True, group_name=True, skip_digestion=True) is True

    right.atoms.at[0, 'atom_name'] = 'X'
    mismatch = left.compare(right, rule='equal', output_type='dictionary', atom_name=True, skip_digestion=True)
    assert mismatch == {'atom_name': False}


def test_get_atom_indices_filters_across_hierarchy_levels():
    topology = build_minimal_topology()

    assert topology.get_atom_indices(atom_name='N') == [0]
    assert topology.get_atom_indices(group_name='HOH') == [2, 3]
    assert topology.get_atom_indices(component_type='peptide') == [0, 1]
    assert topology.get_atom_indices(molecule_name='water') == [2, 3]
    assert topology.get_atom_indices(entity_name='peptide 0') == [0, 1]
    assert topology.get_atom_indices(chain_name='B') == [2, 3]
    assert topology.get_atom_indices(atom_id=['0', '1'], entity_id='40') == [0, 1]
