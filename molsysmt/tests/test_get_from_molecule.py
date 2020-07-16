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
    convert('data/1tcd.pdb', to_form='openmm.PDBFile'),
    convert('data/1tcd.pdb', to_form='pdbfixer.PDBFixer')
]


# Molecule

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_index_from_molecule_1(item):
    output = get(item, target='molecule', atom_index=True)
    assert np.all( np.all(output[ii]==expected_values['atom_index_from_molecule_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_index_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), atom_index=True)
    assert np.all( np.all(output[ii]==expected_values['atom_index_from_molecule_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_name_from_molecule_1(item):
    output = get(item, target='molecule', atom_name=True)
    assert np.all( np.all(output[ii]==expected_values['atom_name_from_molecule_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_name_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), atom_name=True)
    assert np.all( np.all(output[ii]==expected_values['atom_name_from_molecule_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_id_from_molecule_1(item):
    output = get(item, target='molecule', atom_id=True)
    assert np.all( np.all(output[ii]==expected_values['atom_id_from_molecule_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_id_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), atom_id=True)
    assert np.all( np.all(output[ii]==expected_values['atom_id_from_molecule_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_type_from_molecule_1(item):
    output = get(item, target='molecule', atom_type=True)
    assert np.all( np.all(output[ii]==expected_values['atom_type_from_molecule_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_type_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), atom_type=True)
    assert np.all( np.all(output[ii]==expected_values['atom_type_from_molecule_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_index_from_molecule_1(item):
    output = get(item, target='molecule', group_index=True)
    assert np.all( np.all(output[ii]==expected_values['group_index_from_molecule_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_index_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), group_index=True)
    assert np.all( np.all(output[ii]==expected_values['group_index_from_molecule_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_name_from_molecule_1(item):
    output = get(item, target='molecule', group_name=True)
    assert np.all( np.all(output[ii]==expected_values['group_index_from_molecule_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_name_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), group_name=True)
    assert np.all( np.all(output[ii]==expected_values['group_index_from_molecule_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_id_from_molecule_1(item):
    output = get(item, target='molecule', group_id=True)
    assert np.all( np.all(output[ii]==expected_values['group_index_from_molecule_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_id_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), group_id=True)
    assert np.all( np.all(output[ii]==expected_values['group_index_from_molecule_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_type_from_molecule_1(item):
    output = get(item, target='molecule', group_type=True)
    assert np.all( np.all(output[ii]==expected_values['group_index_from_molecule_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_type_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), group_type=True)
    assert np.all( np.all(output[ii]==expected_values['group_index_from_molecule_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_index_from_molecule_1(item):
    output = get(item, target='molecule', component_index=True)
    assert np.all( np.all(output[ii]==expected_values['component_index_from_molecule_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_index_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), component_index=True)
    assert np.all( np.all(output[ii]==expected_values['component_index_from_molecule_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_name_from_molecule_1(item):
    output = get(item, target='molecule', component_name=True)
    assert np.all( np.all(output[ii]==expected_values['component_name_from_molecule_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_name_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), component_name=True)
    assert np.all( np.all(output[ii]==expected_values['component_name_from_molecule_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_id_from_molecule_1(item):
    output = get(item, target='molecule', component_id=True)
    assert np.all( np.all(output[ii]==expected_values['component_id_from_molecule_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_id_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), component_id=True)
    assert np.all( np.all(output[ii]==expected_values['component_id_from_molecule_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_type_from_molecule_1(item):
    output = get(item, target='molecule', component_type=True)
    assert np.all( np.all(output[ii]==expected_values['component_type_from_molecule_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_type_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), component_type=True)
    assert np.all( np.all(output[ii]==expected_values['component_type_from_molecule_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_index_from_molecule_1(item):
    output = get(item, target='molecule', molecule_index=True)
    assert np.all(output==expected_values['molecule_index_from_molecule_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_index_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), molecule_index=True)
    assert np.all(output==expected_values['molecule_index_from_molecule_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_name_from_molecule_1(item):
    output = get(item, target='molecule', molecule_name=True)
    assert np.all(output==expected_values['molecule_name_from_molecule_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_name_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), molecule_name=True)
    assert np.all(output==expected_values['molecule_name_from_molecule_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_id_from_molecule_1(item):
    output = get(item, target='molecule', molecule_id=True)
    assert np.all(output==expected_values['molecule_id_from_molecule_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_id_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), molecule_id=True)
    assert np.all(output==expected_values['molecule_id_from_molecule_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_type_from_molecule_1(item):
    output = get(item, target='molecule', molecule_type=True)
    assert np.all(output==expected_values['molecule_type_from_molecule_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_type_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), molecule_type=True)
    assert np.all(output==expected_values['molecule_type_from_molecule_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_index_from_molecule_1(item):
    output = get(item, target='molecule', chain_index=True)
    assert np.all( np.all(output[ii]==expected_values['chain_index_from_molecule_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_index_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), chain_index=True)
    assert np.all( np.all(output[ii]==expected_values['chain_index_from_molecule_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_name_from_molecule_1(item):
    output = get(item, target='molecule', chain_name=True)
    assert np.all( np.all(output[ii]==expected_values['chain_name_from_molecule_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_name_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), chain_name=True)
    assert np.all( np.all(output[ii]==expected_values['chain_name_from_molecule_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_id_from_molecule_1(item):
    output = get(item, target='molecule', chain_id=True)
    assert np.all( np.all(output[ii]==expected_values['chain_id_from_molecule_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_id_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), chain_id=True)
    assert np.all( np.all(output[ii]==expected_values['chain_id_from_molecule_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_type_from_molecule_1(item):
    output = get(item, target='molecule', chain_type=True)
    assert np.all( np.all(output[ii]==expected_values['chain_type_from_molecule_1'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_type_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), chain_type=True)
    assert np.all( np.all(output[ii]==expected_values['chain_type_from_molecule_2'][ii]) for ii in range(output.shape[0]))

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_index_from_molecule_1(item):
    output = get(item, target='molecule', entity_index=True)
    assert np.all(output==expected_values['entity_index_from_molecule_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_index_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), entity_index=True)
    assert np.all(output==expected_values['entity_index_from_molecule_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_name_from_molecule_1(item):
    output = get(item, target='molecule', entity_name=True)
    assert np.all(output==expected_values['entity_name_from_molecule_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_name_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), entity_name=True)
    assert np.all(output==expected_values['entity_name_from_molecule_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_id_from_molecule_1(item):
    output = get(item, target='molecule', entity_id=True)
    assert np.all(output==expected_values['entity_id_from_molecule_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_id_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), entity_id=True)
    assert np.all(output==expected_values['entity_id_from_molecule_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_type_from_molecule_1(item):
    output = get(item, target='molecule', entity_type=True)
    assert np.all(output==expected_values['entity_type_from_molecule_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_type_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), entity_type=True)
    assert np.all(output==expected_values['entity_type_from_molecule_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_atoms_from_molecule_1(item):
    output = get(item, target='molecule', n_atoms=True)
    assert np.all(output==expected_values['n_atoms_from_molecule_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_atoms_type_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), n_atoms=True)
    assert np.all(output==expected_values['n_atoms_from_molecule_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_groups_from_molecule_1(item):
    output = get(item, target='molecule', n_groups=True)
    assert np.all(output==expected_values['n_groups_from_molecule_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_groups_type_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), n_groups=True)
    assert np.all(output==expected_values['n_groups_from_molecule_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_components_from_molecule_1(item):
    output = get(item, target='molecule', n_components=True)
    assert np.all(output==expected_values['n_components_from_molecule_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_components_type_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), n_components=True)
    assert np.all(output==expected_values['n_components_from_molecule_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_molecules_from_molecule_1(item):
    output = get(item, target='molecule', n_molecules=True)
    assert np.all(output==expected_values['n_molecules_from_molecule_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_molecules_type_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), n_molecules=True)
    assert np.all(output==expected_values['n_molecules_from_molecule_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_chains_from_molecule_1(item):
    output = get(item, target='molecule', n_chains=True)
    assert np.all(output==expected_values['n_chains_from_molecule_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_chains_type_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), n_chains=True)
    assert np.all(output==expected_values['n_chains_from_molecule_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_entities_from_molecule_1(item):
    output = get(item, target='molecule', n_entities=True)
    assert np.all(output==expected_values['n_entities_from_molecule_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_entities_type_from_molecule_2(item):
    output = get(item, target='molecule', indices=range(6), n_entities=True)
    assert np.all(output==expected_values['n_entities_from_molecule_2'])

