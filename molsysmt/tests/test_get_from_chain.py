import pytest
from molsysmt.multitool import _get_form as get_form
from molsysmt import get
from molsysmt import convert
import numpy as np
import pickle

with open('data/1tcd.pickle', 'rb') as f:
    expected_values = pickle.load(f)

args = [
    'data/1tcd.pdb',
    convert('data/1tcd.pdb', to_form='molsysmt.MolSys'),
    convert('data/1tcd.pdb', to_form='molsysmt.Topology'),
    convert('data/1tcd.pdb', to_form='openmm.Topology'),
    convert('data/1tcd.pdb', to_form='openmm.Modeller'),
    convert('data/1tcd.pdb', to_form='pdbfixer.PDBFixer')
]


# Chain

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_index_from_chain_1(item):
    output = get(item, target='chain', atom_index=True)
    assert np.all( np.all(output[ii]==expected_values['atom_index_from_chain_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_index_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), atom_index=True)
    assert np.all( np.all(output[ii]==expected_values['atom_index_from_chain_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_name_from_chain_1(item):
    output = get(item, target='chain', atom_name=True)
    assert np.all( np.all(output[ii]==expected_values['atom_name_from_chain_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_name_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), atom_name=True)
    assert np.all( np.all(output[ii]==expected_values['atom_name_from_chain_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_id_from_chain_1(item):
    output = get(item, target='chain', atom_id=True)
    assert np.all( np.all(output[ii]==expected_values['atom_id_from_chain_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_id_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), atom_id=True)
    assert np.all( np.all(output[ii]==expected_values['atom_id_from_chain_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_type_from_chain_1(item):
    output = get(item, target='chain', atom_type=True)
    assert np.all( np.all(output[ii]==expected_values['atom_type_from_chain_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_type_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), atom_type=True)
    assert np.all( np.all(output[ii]==expected_values['atom_type_from_chain_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_index_from_chain_1(item):
    output = get(item, target='chain', group_index=True)
    assert np.all( np.all(output[ii]==expected_values['group_index_from_chain_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_index_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), group_index=True)
    assert np.all( np.all(output[ii]==expected_values['group_index_from_chain_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_name_from_chain_1(item):
    output = get(item, target='chain', group_name=True)
    assert np.all( np.all(output[ii]==expected_values['group_index_from_chain_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_name_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), group_name=True)
    assert np.all( np.all(output[ii]==expected_values['group_index_from_chain_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_id_from_chain_1(item):
    output = get(item, target='chain', group_id=True)
    assert np.all( np.all(output[ii]==expected_values['group_index_from_chain_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_id_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), group_id=True)
    assert np.all( np.all(output[ii]==expected_values['group_index_from_chain_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_type_from_chain_1(item):
    output = get(item, target='chain', group_type=True)
    assert np.all( np.all(output[ii]==expected_values['group_index_from_chain_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_type_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), group_type=True)
    assert np.all( np.all(output[ii]==expected_values['group_index_from_chain_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_index_from_chain_1(item):
    output = get(item, target='chain', component_index=True)
    assert np.all( np.all(output[ii]==expected_values['component_index_from_chain_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_index_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), component_index=True)
    assert np.all( np.all(output[ii]==expected_values['component_index_from_chain_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_name_from_chain_1(item):
    output = get(item, target='chain', component_name=True)
    assert np.all( np.all(output[ii]==expected_values['component_name_from_chain_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_name_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), component_name=True)
    assert np.all( np.all(output[ii]==expected_values['component_name_from_chain_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_id_from_chain_1(item):
    output = get(item, target='chain', component_id=True)
    assert np.all( np.all(output[ii]==expected_values['component_id_from_chain_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_id_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), component_id=True)
    assert np.all( np.all(output[ii]==expected_values['component_id_from_chain_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_type_from_chain_1(item):
    output = get(item, target='chain', component_type=True)
    assert np.all( np.all(output[ii]==expected_values['component_type_from_chain_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_type_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), component_type=True)
    assert np.all( np.all(output[ii]==expected_values['component_type_from_chain_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_index_from_chain_1(item):
    output = get(item, target='chain', molecule_index=True)
    assert np.all( np.all(output[ii]==expected_values['molecule_index_from_chain_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_index_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), molecule_index=True)
    assert np.all( np.all(output[ii]==expected_values['molecule_index_from_chain_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_name_from_chain_1(item):
    output = get(item, target='chain', molecule_name=True)
    assert np.all( np.all(output[ii]==expected_values['molecule_name_from_chain_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_name_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), molecule_name=True)
    assert np.all( np.all(output[ii]==expected_values['molecule_name_from_chain_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_id_from_chain_1(item):
    output = get(item, target='chain', molecule_id=True)
    assert np.all( np.all(output[ii]==expected_values['molecule_id_from_chain_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_id_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), molecule_id=True)
    assert np.all( np.all(output[ii]==expected_values['molecule_id_from_chain_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_type_from_chain_1(item):
    output = get(item, target='chain', molecule_type=True)
    assert np.all( np.all(output[ii]==expected_values['molecule_type_from_chain_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_type_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), molecule_type=True)
    assert np.all( np.all(output[ii]==expected_values['molecule_type_from_chain_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_index_from_chain_1(item):
    output = get(item, target='chain', chain_index=True)
    assert np.all(output==expected_values['chain_index_from_chain_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_index_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), chain_index=True)
    assert np.all(output==expected_values['chain_index_from_chain_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_name_from_chain_1(item):
    output = get(item, target='chain', chain_name=True)
    assert np.all(output==expected_values['chain_name_from_chain_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_name_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), chain_name=True)
    assert np.all(output==expected_values['chain_name_from_chain_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_id_from_chain_1(item):
    output = get(item, target='chain', chain_id=True)
    assert np.all(output==expected_values['chain_id_from_chain_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_id_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), chain_id=True)
    assert np.all(output==expected_values['chain_id_from_chain_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_type_from_chain_1(item):
    output = get(item, target='chain', chain_type=True)
    assert np.all(output==expected_values['chain_type_from_chain_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_type_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), chain_type=True)
    assert np.all(output==expected_values['chain_type_from_chain_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_index_from_chain_1(item):
    output = get(item, target='chain', entity_index=True)
    assert np.all(output==expected_values['entity_index_from_chain_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_index_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), entity_index=True)
    assert np.all(output==expected_values['entity_index_from_chain_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_name_from_chain_1(item):
    output = get(item, target='chain', entity_name=True)
    assert np.all(output==expected_values['entity_name_from_chain_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_name_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), entity_name=True)
    assert np.all(output==expected_values['entity_name_from_chain_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_id_from_chain_1(item):
    output = get(item, target='chain', entity_id=True)
    assert np.all(output==expected_values['entity_id_from_chain_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_id_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), entity_id=True)
    assert np.all(output==expected_values['entity_id_from_chain_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_type_from_chain_1(item):
    output = get(item, target='chain', entity_type=True)
    assert np.all(output==expected_values['entity_type_from_chain_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_type_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), entity_type=True)
    assert np.all(output==expected_values['entity_type_from_chain_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_atoms_from_chain_1(item):
    output = get(item, target='chain', n_atoms=True)
    assert np.all(output==expected_values['n_atoms_from_chain_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_atoms_type_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), n_atoms=True)
    assert np.all(output==expected_values['n_atoms_from_chain_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_groups_from_chain_1(item):
    output = get(item, target='chain', n_groups=True)
    assert np.all(output==expected_values['n_groups_from_chain_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_groups_type_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), n_groups=True)
    assert np.all(output==expected_values['n_groups_from_chain_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_components_from_chain_1(item):
    output = get(item, target='chain', n_components=True)
    assert np.all(output==expected_values['n_components_from_chain_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_components_type_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), n_components=True)
    assert np.all(output==expected_values['n_components_from_chain_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_molecules_from_chain_1(item):
    output = get(item, target='chain', n_molecules=True)
    assert np.all(output==expected_values['n_molecules_from_chain_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_molecules_type_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), n_molecules=True)
    assert np.all(output==expected_values['n_molecules_from_chain_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_chains_from_chain_1(item):
    output = get(item, target='chain', n_chains=True)
    assert np.all(output==expected_values['n_chains_from_chain_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_chains_type_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), n_chains=True)
    assert np.all(output==expected_values['n_chains_from_chain_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_entities_from_chain_1(item):
    output = get(item, target='chain', n_entities=True)
    assert np.all(output==expected_values['n_entities_from_chain_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_entities_type_from_chain_2(item):
    output = get(item, target='chain', indices=range(2), n_entities=True)
    assert np.all(output==expected_values['n_entities_from_chain_2'])

