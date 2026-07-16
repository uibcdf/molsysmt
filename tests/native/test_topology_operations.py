import numpy as np
import pandas as pd
import pickle
import pytest

from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.native.topology import Bonds_DataFrame, Topology


def build_minimal_topology():
    topology = Topology(n_atoms=4, n_groups=2, n_components=2, n_molecules=2, n_entities=2, n_chains=2)

    topology.atoms['atom_id'] = ['0', '1', '2', '3']
    topology.atoms['atom_name'] = ['N', 'CA', 'O', 'H']
    topology.atoms['atom_type'] = ['N', 'C', 'O', 'H']
    topology.atoms['group_index'] = pd.Series([0, 0, 1, 1], dtype='Int64')
    topology._set_component_indices(pd.Series([0, 0, 1, 1], dtype='Int64'))
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

    topology._append_chemical_state_bonds(
        [[0, 1]], bond_order=1, bond_type='covalent'
    )

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


def test_bonds_and_components_use_reference_chemical_state_storage():
    topology = build_minimal_topology()

    assert topology.bonds is topology._reference_chemical_state.bonds
    assert topology.components is topology._reference_chemical_state.components

    topology.reset_bonds(2)
    topology.reset_components(1)

    assert topology.bonds is topology._reference_chemical_state.bonds
    assert topology.components is topology._reference_chemical_state.components
    assert topology.n_bonds == 2
    assert topology.n_components == 1


def test_component_membership_has_no_duplicate_storage_in_stable_atoms():
    topology = build_minimal_topology()

    assert 'component_index' not in topology.atoms.columns
    assert topology._get_component_indices().tolist() == [0, 0, 1, 1]


def test_default_topology_has_one_private_implicit_reference_state():
    topology = Topology(n_atoms=2)

    assert len(topology._chemical_states) == 1
    assert topology._reference_chemical_state_index == 0
    assert topology._reference_chemical_state is topology._chemical_states[0]
    assert topology._reference_chemical_state.atom_attributes.shape == (2, 0)


def test_private_chemical_state_metadata_is_validated():
    state = Topology()._reference_chemical_state

    state.connectivity_completeness = 'partial'
    state.component_completeness = 'complete'
    state.component_evidence = 'inferred'
    state.provenance_index = 3

    assert state.connectivity_completeness == 'partial'
    assert state.component_completeness == 'complete'
    assert state.component_evidence == 'inferred'
    assert state.provenance_index == 3

    with pytest.raises(StructuralInconsistencyError, match='connectivity completeness'):
        state.connectivity_completeness = 'guessed'
    with pytest.raises(StructuralInconsistencyError, match='component evidence'):
        state.component_evidence = 'automatic'
    with pytest.raises(StructuralInconsistencyError, match='provenance_index'):
        state.provenance_index = -1


def test_optional_atom_state_columns_preserve_nullable_dtypes_and_values():
    topology = Topology(n_atoms=3)

    topology._set_chemical_state_atom_attribute('formal_charge', [-1, 0, 1])
    topology._set_chemical_state_atom_attribute('is_aromatic', [True, False, pd.NA])
    topology._set_chemical_state_atom_attribute('n_unpaired_electrons', [0, 1, pd.NA])
    topology._set_chemical_state_atom_attribute('n_implicit_hydrogens', [3, 0, pd.NA])
    topology._set_chemical_state_atom_attribute('allows_implicit_hydrogens', [True, False, pd.NA])
    topology._set_chemical_state_atom_attribute('stereochemistry', ['R', 'unspecified', pd.NA])

    atom_attributes = topology._reference_chemical_state.atom_attributes
    assert atom_attributes.columns.tolist() == [
        'formal_charge',
        'is_aromatic',
        'n_unpaired_electrons',
        'n_implicit_hydrogens',
        'allows_implicit_hydrogens',
        'stereochemistry',
    ]
    assert str(atom_attributes['formal_charge'].dtype) == 'Int16'
    assert str(atom_attributes['is_aromatic'].dtype) == 'boolean'
    assert str(atom_attributes['n_unpaired_electrons'].dtype) == 'UInt8'
    assert str(atom_attributes['n_implicit_hydrogens'].dtype) == 'UInt8'
    assert str(atom_attributes['allows_implicit_hydrogens'].dtype) == 'boolean'
    assert str(atom_attributes['stereochemistry'].dtype) == 'string'
    assert atom_attributes['formal_charge'].tolist() == [-1, 0, 1]
    assert atom_attributes['stereochemistry'].tolist() == ['R', 'unspecified', pd.NA]


def test_partial_atom_state_assignment_materializes_missing_values():
    topology = Topology(n_atoms=3)

    topology._set_chemical_state_atom_attribute('stereochemistry', 'S', atom_indices=[1])

    values = topology._get_chemical_state_atom_attribute('stereochemistry')
    assert values.tolist() == [pd.NA, 'S', pd.NA]
    assert topology._has_chemical_state_atom_attribute('stereochemistry')

    topology._set_chemical_state_atom_attribute('formal_charge', pd.NA)
    assert not topology._has_chemical_state_atom_attribute('formal_charge')
    assert topology._has_chemical_state_atom_attribute('formal_charge', include_none=True)


def test_atom_state_assignment_rejects_invalid_names_values_lengths_and_indices():
    topology = Topology(n_atoms=3)

    with pytest.raises(StructuralInconsistencyError, match='Unknown chemical-state atom attribute'):
        topology._set_chemical_state_atom_attribute('partial_charge', [0, 0, 0])
    with pytest.raises(StructuralInconsistencyError, match='Invalid atom stereochemistry'):
        topology._set_chemical_state_atom_attribute('stereochemistry', ['CW', 'S', 'R'])
    with pytest.raises(StructuralInconsistencyError, match='accepts only boolean'):
        topology._set_chemical_state_atom_attribute('is_aromatic', [1, 0, 1])
    with pytest.raises(StructuralInconsistencyError, match='cannot be represented as UInt8'):
        topology._set_chemical_state_atom_attribute('n_implicit_hydrogens', [0, -1, 2])
    with pytest.raises(StructuralInconsistencyError, match='received 2 values; expected 3'):
        topology._set_chemical_state_atom_attribute('formal_charge', [0, 1])
    with pytest.raises(StructuralInconsistencyError, match='must not contain duplicates'):
        topology._set_chemical_state_atom_attribute('formal_charge', [0, 1], atom_indices=[1, 1])
    with pytest.raises(StructuralInconsistencyError, match='outside the valid range'):
        topology._set_chemical_state_atom_attribute('formal_charge', 0, atom_indices=[3])


def test_optional_atom_state_column_can_be_removed():
    topology = Topology(n_atoms=2)
    topology._set_chemical_state_atom_attribute('formal_charge', [0, 1])

    topology._remove_chemical_state_atom_attribute('formal_charge')

    assert topology._get_chemical_state_atom_attribute('formal_charge') is None
    assert not topology._has_chemical_state_atom_attribute('formal_charge', include_none=True)


def test_zero_state_reads_fail_but_explicit_mutation_creates_reference_state():
    topology = Topology(n_atoms=2)
    topology._clear_chemical_states()

    with pytest.raises(StructuralInconsistencyError, match='no chemical state'):
        _ = topology.bonds

    replacement = Bonds_DataFrame(n_bonds=0)
    topology.bonds = replacement

    assert len(topology._chemical_states) == 1
    assert topology._reference_chemical_state_index == 0
    assert topology.bonds is topology._reference_chemical_state.bonds
    assert topology.bonds is not replacement


def test_multiple_states_require_an_unambiguous_reference():
    topology = Topology(n_atoms=2)
    second_index = topology._append_chemical_state(state_id='product')
    topology._set_reference_chemical_state_index(None)

    with pytest.raises(StructuralInconsistencyError, match='ambiguous'):
        _ = topology.components

    topology._set_reference_chemical_state_index(second_index)

    assert topology._reference_chemical_state.state_id == 'product'


def test_duplicate_state_labels_do_not_replace_internal_row_identity():
    topology = Topology(n_atoms=1)
    topology._chemical_states[0].state_id = 'state'
    second_index = topology._append_chemical_state(state_id='state')

    assert len(topology._chemical_states) == 2
    assert topology._chemical_states[0].state_id == topology._chemical_states[second_index].state_id
    assert topology._chemical_states[0] is not topology._chemical_states[second_index]


def test_explicit_state_index_allows_atom_attribute_access_without_reference():
    topology = Topology(n_atoms=2)
    second_index = topology._append_chemical_state(state_id='product')
    topology._set_reference_chemical_state_index(None)

    topology._set_chemical_state_atom_attribute(
        'formal_charge', [0, -1], state_index=second_index
    )

    assert topology._get_chemical_state_atom_attribute(
        'formal_charge', state_index=second_index
    ).tolist() == [0, -1]


def test_private_bond_seam_resolves_explicit_state_without_reference():
    topology = Topology(n_atoms=3)
    second_index = topology._append_chemical_state(state_id='product')
    topology._set_reference_chemical_state_index(None)

    topology._append_chemical_state_bonds(
        [[2, 1]], orders='aromatic', types='dative', state_index=second_index
    )

    bonds = topology._get_chemical_state_bonds(state_index=second_index)
    assert bonds[['atom1_index', 'atom2_index']].values.tolist() == [[1, 2]]
    assert bonds['is_aromatic'].tolist() == [True]
    assert bonds['bond_type'].tolist() == ['dative']
    assert bonds['joins_components'].tolist() == [False]
    with pytest.raises(StructuralInconsistencyError, match='ambiguous'):
        topology._get_chemical_state_bonds()


def test_private_bond_mutation_creates_first_state_but_read_does_not():
    topology = Topology(n_atoms=2)
    topology._clear_chemical_states()

    with pytest.raises(StructuralInconsistencyError, match='no chemical state'):
        topology._get_chemical_state_bonds()

    topology._append_chemical_state_bonds([[0, 1]], orders='1')

    assert len(topology._chemical_states) == 1
    assert topology._reference_chemical_state_index == 0
    assert topology._get_chemical_state_bonds()['bond_order'].tolist() == [1]


def test_private_bond_seam_normalizes_unambiguous_legacy_columns():
    topology = Topology(n_atoms=2)
    plain_table = pd.DataFrame(
        {
            'atom1_index': [0],
            'atom2_index': [1],
            'order': ['1.5'],
            'type': ['dative'],
        }
    )

    topology._set_chemical_state_bonds(plain_table)

    bonds = topology._get_chemical_state_bonds()
    assert isinstance(bonds, Bonds_DataFrame)
    assert str(bonds['atom1_index'].dtype) == 'Int64'
    assert str(bonds['atom2_index'].dtype) == 'Int64'
    assert bonds['fractional_bond_order'].tolist() == [1.5]
    assert bonds['bond_type'].tolist() == ['dative']
    assert bonds['joins_components'].tolist() == [False]


def test_private_bond_seam_rejects_opaque_legacy_metadata():
    topology = Topology(n_atoms=2)
    plain_table = pd.DataFrame(
        {
            'atom1_index': [0],
            'atom2_index': [1],
            'type': ['amide'],
        }
    )

    with pytest.raises(StructuralInconsistencyError, match='no unambiguous mapping'):
        topology._set_chemical_state_bonds(plain_table)


def test_normalized_bond_table_uses_nullable_canonical_dtypes():
    topology = Topology(n_atoms=4)
    topology._append_chemical_state_bonds(
        [[1, 0]],
        bond_id='external-7',
        bond_order=2,
        fractional_bond_order=1.75,
        bond_type='dative',
        is_aromatic=False,
        is_conjugated=True,
        stereochemistry='E',
        stereo_atom1_index=2,
        stereo_atom2_index=3,
        donor_atom_index=0,
        acceptor_atom_index=1,
        evidence='explicit',
        provenance_index=4,
    )

    bonds = topology._get_chemical_state_bonds()
    assert bonds[['atom1_index', 'atom2_index']].values.tolist() == [[0, 1]]
    assert str(bonds['bond_id'].dtype) == 'string'
    assert str(bonds['bond_order'].dtype) == 'UInt8'
    assert str(bonds['fractional_bond_order'].dtype) == 'Float64'
    assert str(bonds['bond_type'].dtype) == 'string'
    assert str(bonds['is_aromatic'].dtype) == 'boolean'
    assert str(bonds['is_conjugated'].dtype) == 'boolean'
    assert str(bonds['stereo_atom1_index'].dtype) == 'Int64'
    assert str(bonds['donor_atom_index'].dtype) == 'Int64'
    assert bonds['joins_components'].tolist() == [False]


def test_normalized_bond_table_rejects_malformed_graph_edges():
    topology = Topology(n_atoms=3)

    with pytest.raises(StructuralInconsistencyError, match='Self-bonds'):
        topology._append_chemical_state_bonds([[1, 1]])

    topology._append_chemical_state_bonds([[0, 1]])
    with pytest.raises(StructuralInconsistencyError, match='Only one bond'):
        topology._append_chemical_state_bonds([[1, 0]])

    with pytest.raises(StructuralInconsistencyError, match='one of the bond endpoints'):
        Topology(n_atoms=3)._append_chemical_state_bonds(
            [[0, 1]], donor_atom_index=2
        )


def test_non_default_component_participation_requires_evidence():
    topology = Topology(n_atoms=2)

    with pytest.raises(StructuralInconsistencyError, match='requires explicit bond evidence'):
        topology._append_chemical_state_bonds(
            [[0, 1]], bond_type='dative', joins_components=True
        )

    topology._append_chemical_state_bonds(
        [[0, 1]], bond_type='dative', joins_components=True,
        evidence='explicit'
    )
    assert topology.bonds['joins_components'].tolist() == [True]


def test_component_inference_excludes_explicit_non_participating_bonds():
    topology = Topology(n_atoms=3)
    topology._append_chemical_state_bonds(
        [[0, 1]], bond_type='covalent'
    )
    topology._append_chemical_state_bonds(
        [[1, 2]], bond_type='dative'
    )

    topology.rebuild_components(
        redefine_indices=True,
        redefine_ids=True,
        redefine_types=False,
        redefine_names=False,
    )

    assert topology._get_component_indices().tolist() == [0, 0, 1]
    assert topology._reference_chemical_state.component_evidence == 'inferred'
    assert topology._reference_chemical_state.component_completeness == 'partial'


def test_extract_remaps_all_bond_atom_references_together():
    topology = build_minimal_topology()
    topology.reset_bonds(0)
    topology._append_chemical_state_bonds(
        [[1, 3]], bond_type='dative', donor_atom_index=3,
        acceptor_atom_index=1, stereochemistry='E',
        stereo_atom1_index=0, stereo_atom2_index=2,
    )

    extracted = topology.extract(atom_indices=[3, 1, 2], skip_digestion=True)
    bonds = extracted._get_chemical_state_bonds()

    assert bonds[['atom1_index', 'atom2_index']].values.tolist() == [[0, 2]]
    assert bonds['donor_atom_index'].tolist() == [2]
    assert bonds['acceptor_atom_index'].tolist() == [0]
    assert 'stereochemistry' not in bonds
    assert 'stereo_atom1_index' not in bonds
    assert 'stereo_atom2_index' not in bonds


def test_native_add_offsets_all_bond_atom_references():
    left = build_minimal_topology()
    right = build_minimal_topology()
    right.reset_bonds(0)
    right._append_chemical_state_bonds(
        [[1, 3]], bond_type='dative', donor_atom_index=3,
        acceptor_atom_index=1, stereochemistry='E',
        stereo_atom1_index=0, stereo_atom2_index=2,
    )

    left.add(right, skip_digestion=True)
    added_bond = left.bonds.loc[left.bonds['donor_atom_index'].notna()].iloc[0]

    assert [added_bond['atom1_index'], added_bond['atom2_index']] == [5, 7]
    assert added_bond['donor_atom_index'] == 7
    assert added_bond['acceptor_atom_index'] == 5
    assert added_bond['stereo_atom1_index'] == 4
    assert added_bond['stereo_atom2_index'] == 6


def test_private_bond_append_validates_shape_bounds_and_metadata_lengths():
    topology = Topology(n_atoms=3)

    with pytest.raises(StructuralInconsistencyError, match=r'shape \(n_bonds, 2\)'):
        topology._append_chemical_state_bonds([0, 1])
    with pytest.raises(StructuralInconsistencyError, match='between 0 and 2'):
        topology._append_chemical_state_bonds([[0, 3]])
    with pytest.raises(StructuralInconsistencyError, match='received 1 values; expected 2'):
        topology._append_chemical_state_bonds([[0, 1], [1, 2]], orders=['1'])


def test_private_bond_removal_isolated_to_explicit_state():
    topology = Topology(n_atoms=3)
    topology._append_chemical_state_bonds([[0, 1]], orders='1')
    second_index = topology._append_chemical_state(state_id='product')
    topology._append_chemical_state_bonds(
        [[0, 2], [1, 2]], orders=['1', '2'], state_index=second_index
    )

    topology._remove_chemical_state_bonds([0], state_index=second_index)

    assert topology._get_chemical_state_bonds()['bond_order'].tolist() == [1]
    assert topology._get_chemical_state_bonds(state_index=second_index)['bond_order'].tolist() == [2]


def test_multistate_extract_preserves_and_remaps_each_state_independently():
    topology = build_minimal_topology()
    topology._set_chemical_state_atom_attribute('formal_charge', [0, 0, -1, 1])
    second_index = topology._append_chemical_state(state_id='product')
    topology._set_component_indices([0, 1, 1, 1], state_index=second_index)
    topology._chemical_states[second_index].components = topology.components.copy()
    topology._chemical_states[second_index].components.loc[0, 'component_name'] = 'reactant fragment'
    topology._append_chemical_state_bonds(
        [[0, 2], [2, 3]], orders=[1, 2], state_index=second_index
    )
    topology._set_reference_chemical_state_index(None)

    extracted = topology.extract(atom_indices=[0, 2, 3], skip_digestion=True)

    assert len(extracted._chemical_states) == 2
    assert extracted._reference_chemical_state_index is None
    assert extracted._get_component_indices(state_index=0).tolist() == [0, 1, 1]
    assert extracted._get_component_indices(state_index=second_index).tolist() == [0, 1, 1]
    assert extracted._chemical_states[0].components['component_name'].tolist() == ['peptide 0', 'water']
    assert extracted._chemical_states[second_index].components['component_name'].tolist() == [
        'reactant fragment', 'water'
    ]
    assert extracted._get_chemical_state_bonds(state_index=0).shape[0] == 0
    assert extracted._get_chemical_state_bonds(state_index=second_index)[
        ['atom1_index', 'atom2_index']
    ].values.tolist() == [[0, 1], [1, 2]]
    assert extracted._chemical_states[0].atom_attributes['formal_charge'].tolist() == [0, -1, 1]


def test_component_membership_seam_supports_full_and_partial_updates():
    topology = Topology(n_atoms=3)

    assert topology._component_indices_are_missing()

    topology._set_component_indices([0, 0, 1])

    assert topology._get_component_indices().tolist() == [0, 0, 1]
    assert not topology._component_indices_are_missing()

    topology._set_component_indices(pd.NA, atom_indices=1)

    assert topology._get_component_indices().tolist() == [0, pd.NA, 1]
    assert topology._component_indices_are_missing()

    with pytest.raises(StructuralInconsistencyError, match='must be non-negative'):
        topology._set_component_indices([0, -1, 1])


def test_copy_keeps_reference_chemical_state_storage_independent():
    topology = build_minimal_topology()
    cloned = topology.copy()

    cloned.bonds.at[0, 'bond_order'] = 2
    cloned.components.at[0, 'component_name'] = 'changed'

    assert topology.bonds.at[0, 'bond_order'] == 1
    assert topology.components.at[0, 'component_name'] == 'peptide 0'


def test_copy_preserves_all_private_states_and_reference_independently():
    topology = build_minimal_topology()
    topology._set_chemical_state_atom_attribute('formal_charge', [0, 0, -1, 1])
    topology._reference_chemical_state.connectivity_completeness = 'complete'
    second_index = topology._append_chemical_state(state_id='product', set_as_reference=True)
    topology._chemical_states[second_index].connectivity_completeness = 'partial'

    cloned = topology.copy()
    cloned._chemical_states[0].bonds.at[0, 'bond_order'] = 2
    cloned._chemical_states[0].atom_attributes.at[0, 'formal_charge'] = 1
    cloned._chemical_states[second_index].state_id = 'changed'

    assert cloned._reference_chemical_state_index == second_index
    assert topology._chemical_states[0].bonds.at[0, 'bond_order'] == 1
    assert topology._chemical_states[0].atom_attributes.at[0, 'formal_charge'] == 0
    assert topology._chemical_states[second_index].state_id == 'product'


def test_pickle_roundtrip_preserves_reference_chemical_state_storage():
    topology = build_minimal_topology()

    restored = pickle.loads(pickle.dumps(topology))

    assert restored.bonds is restored._reference_chemical_state.bonds
    assert restored.components is restored._reference_chemical_state.components
    assert restored.bonds[['atom1_index', 'atom2_index']].values.tolist() == [[0, 1]]
    assert restored.components['component_name'].tolist() == ['peptide 0', 'water']


def test_pickle_roundtrip_preserves_private_state_collection_and_metadata():
    topology = build_minimal_topology()
    topology._set_chemical_state_atom_attribute('formal_charge', [0, 0, -1, 1])
    topology._reference_chemical_state.connectivity_completeness = 'complete'
    second_index = topology._append_chemical_state(state_id='product', set_as_reference=True)
    topology._chemical_states[second_index].component_evidence = 'user_defined'

    restored = pickle.loads(pickle.dumps(topology))

    assert len(restored._chemical_states) == 2
    assert restored._reference_chemical_state_index == second_index
    assert restored._chemical_states[0].connectivity_completeness == 'complete'
    assert restored._chemical_states[0].atom_attributes['formal_charge'].tolist() == [0, 0, -1, 1]
    assert restored._reference_chemical_state.component_evidence == 'user_defined'


def test_legacy_direct_table_state_migrates_on_restore():
    topology = build_minimal_topology()
    legacy_state = topology.__dict__.copy()
    reference_state = topology._reference_chemical_state
    legacy_state.pop('_chemical_states')
    legacy_state.pop('_reference_chemical_state_index')
    legacy_state['bonds'] = reference_state.bonds
    legacy_state['components'] = reference_state.components

    restored = Topology.__new__(Topology)
    restored.__setstate__(legacy_state)

    assert restored.bonds is restored._reference_chemical_state.bonds
    assert restored.components is restored._reference_chemical_state.components
    assert restored.n_bonds == 1
    assert restored.n_components == 2


def test_legacy_atom_component_column_migrates_to_reference_state_on_restore():
    topology = build_minimal_topology()
    legacy_state = topology.__dict__.copy()
    reference_state = topology._reference_chemical_state
    legacy_state.pop('_chemical_states')
    legacy_state.pop('_reference_chemical_state_index')
    legacy_atoms = pd.DataFrame(topology.atoms.copy())
    legacy_atoms['component_index'] = [0, 0, 1, 1]
    legacy_state['atoms'] = legacy_atoms
    legacy_state['bonds'] = reference_state.bonds
    legacy_state['components'] = reference_state.components

    restored = Topology.__new__(Topology)
    restored.__setstate__(legacy_state)

    assert 'component_index' not in restored.atoms.columns
    assert restored._get_component_indices().tolist() == [0, 0, 1, 1]


def test_intermediate_reference_state_storage_migrates_on_restore():
    topology = build_minimal_topology()
    legacy_state = topology.__dict__.copy()
    reference_state = topology._reference_chemical_state
    legacy_state.pop('_chemical_states')
    legacy_state.pop('_reference_chemical_state_index')
    legacy_state['_reference_chemical_state'] = reference_state

    restored = Topology.__new__(Topology)
    restored.__setstate__(legacy_state)

    assert len(restored._chemical_states) == 1
    assert restored._reference_chemical_state is restored._chemical_states[0]
    assert restored.bonds[['atom1_index', 'atom2_index']].values.tolist() == [[0, 1]]


def test_extract_reindexes_hierarchy_and_bonds():
    topology = build_minimal_topology()
    topology._set_chemical_state_atom_attribute('formal_charge', [0, 1, -1, 0])
    extracted = topology.extract(atom_indices=[0, 1], skip_digestion=True)

    assert extracted.n_atoms == 2
    assert extracted.n_groups == 1
    assert extracted.n_components == 1
    assert extracted.n_molecules == 1
    assert extracted.n_entities == 1
    assert extracted.n_chains == 1
    assert extracted.bonds[['atom1_index', 'atom2_index']].values.tolist() == [[0, 1]]
    assert extracted.atoms['group_index'].tolist() == [0, 0]
    assert extracted._get_component_indices().tolist() == [0, 0]
    assert extracted.atoms['chain_index'].tolist() == [0, 0]
    assert extracted._get_chemical_state_atom_attribute('formal_charge').tolist() == [0, 1]


def test_remove_returns_topology_without_removed_atoms():
    topology = build_minimal_topology()
    trimmed = topology.remove(atom_indices=[2, 3], skip_digestion=True)

    assert trimmed.n_atoms == 2
    assert trimmed.atoms['atom_id'].tolist() == ['0', '1']
    assert trimmed.n_groups == 1


def test_add_offsets_indices_and_can_rebuild_ids():
    left = build_minimal_topology()
    right = build_minimal_topology()
    left._set_chemical_state_atom_attribute('formal_charge', [0, 1, 0, -1])
    right._set_chemical_state_atom_attribute('formal_charge', [-1, 0, 1, 0])

    left.add(right, keep_ids=False, skip_digestion=True)

    assert left.n_atoms == 8
    assert left.n_groups == 4
    assert left.n_components == 6
    assert left.n_molecules == 4
    assert left.n_entities == 2
    assert left.n_chains == 4
    assert left.n_bonds == 2
    assert left.atoms['group_index'].tolist() == [0, 0, 1, 1, 2, 2, 3, 3]
    assert left._get_component_indices().tolist() == [0, 0, 1, 2, 3, 3, 4, 5]
    assert left.bonds[['atom1_index', 'atom2_index']].values.tolist() == [[0, 1], [4, 5]]
    assert left.atoms['atom_id'].map(type).eq(str).all()
    assert left.groups['group_id'].map(type).eq(str).all()
    assert left.molecules['entity_index'].tolist() == [0, 1, 0, 1]
    assert left._get_chemical_state_atom_attribute('formal_charge').tolist() == [
        0, 1, 0, -1, -1, 0, 1, 0
    ]


def test_add_bonds_sorts_pairs_and_rebuilds_components():
    topology = build_minimal_topology()
    topology.add_bonds([[3, 2], [2, 1]], skip_digestion=True)

    assert topology.n_bonds == 3
    assert topology.bonds[['atom1_index', 'atom2_index']].values.tolist() == [[0, 1], [1, 2], [2, 3]]
    assert topology._get_component_indices().tolist() == [0, 0, 0, 0]


def test_remove_bonds_all_resets_connectivity():
    topology = build_minimal_topology()
    topology.add_bonds([[2, 3]], skip_digestion=True)

    topology.remove_bonds('all', skip_digestion=True)

    assert topology.n_bonds == 0
    assert topology.components.shape[0] == 4
    assert topology._get_component_indices().tolist() == [0, 1, 2, 3]


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
    topology.bonds['bond_order'] = pd.array([1, 1], dtype='UInt8')
    topology.bonds['bond_type'] = pd.array(['covalent', 'covalent'], dtype='string')

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
