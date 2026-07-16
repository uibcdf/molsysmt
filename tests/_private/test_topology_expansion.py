import numpy as np
import pandas as pd

from molsysmt._private.topology_expansion import expand_atom_dataframe
from molsysmt.native import Topology


def _topology_with_all_hierarchy_levels():
    topology = Topology(
        n_atoms=4,
        n_groups=2,
        n_components=2,
        n_molecules=2,
        n_entities=2,
        n_chains=2,
        skip_digestion=True,
    )
    topology.atoms['atom_name'] = ['N', 'CA', 'O', 'H']
    topology.atoms['group_index'] = [0, 0, 1, 1]
    topology._set_component_indices([0, 0, 1, 1])
    topology.atoms['chain_index'] = [0, 0, 1, 1]
    topology.groups['group_name'] = ['ALA', 'HOH']
    topology.groups['molecule_index'] = [0, 1]
    topology.components['component_name'] = ['protein', 'solvent']
    topology.molecules['molecule_name'] = ['peptide', 'water']
    topology.molecules['entity_index'] = [0, 1]
    topology.entities['entity_name'] = ['peptide entity', 'water entity']
    topology.chains['chain_name'] = ['A', 'B']
    return topology


def _legacy_merge_expansion(topology):
    molecule_columns = ['molecule_name', 'entity_index']
    group_columns = ['group_name', 'molecule_index']
    atom_columns = ['atom_name', 'group_index', 'component_index', 'chain_index']

    output = pd.merge(
        topology.molecules[molecule_columns],
        topology.entities[['entity_name']],
        left_on='entity_index',
        right_index=True,
    )
    output = pd.merge(
        topology.groups[group_columns],
        output,
        left_on='molecule_index',
        right_index=True,
    )
    atom_table = topology.atoms.copy()
    atom_table['component_index'] = topology._get_component_indices()
    output = pd.merge(
        atom_table[atom_columns],
        output,
        left_on='group_index',
        right_index=True,
    )
    output = pd.merge(
        output,
        topology.components[['component_name']],
        left_on='component_index',
        right_index=True,
    )
    return pd.merge(
        output,
        topology.chains[['chain_name']],
        left_on='chain_index',
        right_index=True,
    )


def test_direct_gathers_match_the_legacy_merge_pipeline():
    topology = _topology_with_all_hierarchy_levels()
    expected = _legacy_merge_expansion(topology)

    observed = expand_atom_dataframe(
        topology,
        atom_columns=['atom_name', 'group_index', 'component_index', 'chain_index'],
        group_columns=['group_name', 'molecule_index'],
        component_columns=['component_name'],
        molecule_columns=['molecule_name', 'entity_index'],
        entity_columns=['entity_name'],
        chain_columns=['chain_name'],
    )

    pd.testing.assert_frame_equal(observed, expected)


def test_direct_gathers_preserve_inner_join_semantics_for_null_links():
    topology = _topology_with_all_hierarchy_levels()
    topology.atoms.loc[3, 'group_index'] = pd.NA
    topology._set_component_indices(99, atom_indices=2)

    expected = _legacy_merge_expansion(topology)
    observed = expand_atom_dataframe(
        topology,
        atom_columns=['atom_name', 'group_index', 'component_index', 'chain_index'],
        group_columns=['group_name', 'molecule_index'],
        component_columns=['component_name'],
        molecule_columns=['molecule_name', 'entity_index'],
        entity_columns=['entity_name'],
        chain_columns=['chain_name'],
    )

    assert observed.index.tolist() == [0, 1]
    pd.testing.assert_frame_equal(observed, expected)


def test_get_atom_indices_uses_direct_gathers_across_levels():
    topology = _topology_with_all_hierarchy_levels()

    assert topology.get_atom_indices(
        group_name='ALA',
        component_name='protein',
        molecule_name='peptide',
        entity_name='peptide entity',
        chain_name='A',
    ) == [0, 1]


def test_selection_output_order_remains_atom_order():
    topology = _topology_with_all_hierarchy_levels()
    topology.atoms['group_index'] = [1, 0, 1, 0]

    output = topology.get_atom_indices(group_name=['ALA', 'HOH'])

    assert output == [0, 1, 2, 3]
