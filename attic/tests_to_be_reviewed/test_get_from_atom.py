import pytest
from molsysmt.multitool import get_form as get_form
from molsysmt import get
from molsysmt import convert
import numpy as np
import pickle

with open('data/1tcd.pickle', 'rb') as f:
    expected_values = pickle.load(f)

args = [
#    'data/1tcd.pdb',
#    convert('data/1tcd.pdb', to_form='molsysmt.MolSys'),
#    convert('data/1tcd.pdb', to_form='molsysmt.Topology'),
#    convert('data/1tcd.pdb', to_form='openmm.Topology'),
#    convert('data/1tcd.pdb', to_form='openmm.Modeller'),
#    convert('data/1tcd.pdb', to_form='openmm.PDBFile'),
#    convert('data/1tcd.pdb', to_form='pdbfixer.PDBFixer'),
    convert('data/1tcd.pdb', to_form='mdtraj.Topology'),
    convert('data/1tcd.pdb', to_form='mdtraj.Trajectory')
]


# Atom

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_index_from_atom_1(item):
    output = get(item, target='atom', index=True)
    assert np.all(output==expected_values['atom_index_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_index_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), index=True)
    assert np.all(output==expected_values['atom_index_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_name_from_atom_1(item):
    output = get(item, target='atom', name=True)
    assert np.all(output==expected_values['atom_name_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_name_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), name=True)
    assert np.all(output==expected_values['atom_name_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_id_from_atom_1(item):
    output = get(item, target='atom', id=True)
    assert np.all(output==expected_values['atom_id_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_id_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), id=True)
    assert np.all(output==expected_values['atom_id_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_type_from_atom_1(item):
    output = get(item, target='atom', type=True)
    assert np.all(output==expected_values['atom_type_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_atom_type_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), type=True)
    assert np.all(output==expected_values['atom_type_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_index_from_atom_1(item):
    output = get(item, target='atom', group_index=True)
    assert np.all(output==expected_values['group_index_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_index_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), group_index=True)
    assert np.all(output==expected_values['group_index_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_name_from_atom_1(item):
    output = get(item, target='atom', group_name=True)
    assert np.all(output==expected_values['group_name_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_name_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), group_name=True)
    assert np.all(output==expected_values['group_name_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_id_from_atom_1(item):
    output = get(item, target='atom', group_id=True)
    assert np.all(output==expected_values['group_id_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_id_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), group_id=True)
    assert np.all(output==expected_values['group_id_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_type_from_atom_1(item):
    output = get(item, target='atom', group_type=True)
    assert np.all(output==expected_values['group_type_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_group_type_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), group_type=True)
    assert np.all(output==expected_values['group_type_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_index_from_atom_1(item):
    output = get(item, target='atom', component_index=True)
    assert np.all(output==expected_values['component_index_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_index_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), component_index=True)
    assert np.all(output==expected_values['component_index_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_name_from_atom_1(item):
    output = get(item, target='atom', component_name=True)
    assert np.all(output==expected_values['component_name_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_name_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), component_name=True)
    assert np.all(output==expected_values['component_name_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_id_from_atom_1(item):
    output = get(item, target='atom', component_id=True)
    assert np.all(output==expected_values['component_id_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_id_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), component_id=True)
    assert np.all(output==expected_values['component_id_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_type_from_atom_1(item):
    output = get(item, target='atom', component_type=True)
    assert np.all(output==expected_values['component_type_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_component_type_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), component_type=True)
    assert np.all(output==expected_values['component_type_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_index_from_atom_1(item):
    output = get(item, target='atom', molecule_index=True)
    assert np.all(output==expected_values['molecule_index_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_index_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), molecule_index=True)
    assert np.all(output==expected_values['molecule_index_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_name_from_atom_1(item):
    output = get(item, target='atom', molecule_name=True)
    assert np.all(output==expected_values['molecule_name_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_name_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), molecule_name=True)
    assert np.all(output==expected_values['molecule_name_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_id_from_atom_1(item):
    output = get(item, target='atom', molecule_id=True)
    assert np.all(output==expected_values['molecule_id_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_id_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), molecule_id=True)
    assert np.all(output==expected_values['molecule_id_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_type_from_atom_1(item):
    output = get(item, target='atom', molecule_type=True)
    assert np.all(output==expected_values['molecule_type_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_molecule_type_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), molecule_type=True)
    assert np.all(output==expected_values['molecule_type_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_index_from_atom_1(item):
    output = get(item, target='atom', chain_index=True)
    assert np.all(output==expected_values['chain_index_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_index_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), chain_index=True)
    assert np.all(output==expected_values['chain_index_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_name_from_atom_1(item):
    output = get(item, target='atom', chain_name=True)
    assert np.all(output==expected_values['chain_name_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_name_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), chain_name=True)
    assert np.all(output==expected_values['chain_name_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_id_from_atom_1(item):
    output = get(item, target='atom', chain_id=True)
    assert np.all(output==expected_values['chain_id_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_id_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), chain_id=True)
    assert np.all(output==expected_values['chain_id_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_type_from_atom_1(item):
    output = get(item, target='atom', chain_type=True)
    assert np.all(output==expected_values['chain_type_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_chain_type_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), chain_type=True)
    assert np.all(output==expected_values['chain_type_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_index_from_atom_1(item):
    output = get(item, target='atom', entity_index=True)
    assert np.all(output==expected_values['entity_index_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_index_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), entity_index=True)
    assert np.all(output==expected_values['entity_index_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_name_from_atom_1(item):
    output = get(item, target='atom', entity_name=True)
    assert np.all(output==expected_values['entity_name_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_name_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), entity_name=True)
    assert np.all(output==expected_values['entity_name_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_id_from_atom_1(item):
    output = get(item, target='atom', entity_id=True)
    assert np.all(output==expected_values['entity_id_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_id_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), entity_id=True)
    assert np.all(output==expected_values['entity_id_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_type_from_atom_1(item):
    output = get(item, target='atom', entity_type=True)
    assert np.all(output==expected_values['entity_type_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_entity_type_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), entity_type=True)
    assert np.all(output==expected_values['entity_type_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_atoms_from_atom_1(item):
    output = get(item, target='atom', n_atoms=True)
    assert np.all(output==expected_values['n_atoms_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_atoms_type_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), n_atoms=True)
    assert np.all(output==expected_values['n_atoms_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_groups_from_atom_1(item):
    output = get(item, target='atom', n_groups=True)
    assert np.all(output==expected_values['n_groups_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_groups_type_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), n_groups=True)
    assert np.all(output==expected_values['n_groups_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_components_from_atom_1(item):
    output = get(item, target='atom', n_components=True)
    assert np.all(output==expected_values['n_components_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_components_type_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), n_components=True)
    assert np.all(output==expected_values['n_components_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_molecules_from_atom_1(item):
    output = get(item, target='atom', n_molecules=True)
    assert np.all(output==expected_values['n_molecules_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_molecules_type_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), n_molecules=True)
    assert np.all(output==expected_values['n_molecules_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_chains_from_atom_1(item):
    output = get(item, target='atom', n_chains=True)
    assert np.all(output==expected_values['n_chains_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_chains_type_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), n_chains=True)
    assert np.all(output==expected_values['n_chains_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_entities_from_atom_1(item):
    output = get(item, target='atom', n_entities=True)
    assert np.all(output==expected_values['n_entities_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_entities_type_from_atom_2(item):
    output = get(item, target='atom', indices=range(40,80), n_entities=True)
    assert np.all(output==expected_values['n_entities_from_atom_2'])

