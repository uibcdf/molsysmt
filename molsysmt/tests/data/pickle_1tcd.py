import pickle
from molsysmt import convert, get


expected_values={}

molecular_system = convert('1tcd.pdb')

# Atom

expected_values['atom_index_from_atom_1'] = get(molecular_system, target='atom', index=True)
expected_values['atom_index_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), index=True)
expected_values['atom_name_from_atom_1'] = get(molecular_system, target='atom', name=True)
expected_values['atom_name_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), name=True)
expected_values['atom_id_from_atom_1'] = get(molecular_system, target='atom', id=True)
expected_values['atom_id_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), id=True)
expected_values['atom_type_from_atom_1'] = get(molecular_system, target='atom', type=True)
expected_values['atom_type_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), type=True)

expected_values['group_index_from_atom_1'] = get(molecular_system, target='atom', group_index=True)
expected_values['group_index_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), group_index=True)
expected_values['group_name_from_atom_1'] = get(molecular_system, target='atom', group_name=True)
expected_values['group_name_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), group_name=True)
expected_values['group_id_from_atom_1'] = get(molecular_system, target='atom', group_id=True)
expected_values['group_id_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), group_id=True)
expected_values['group_type_from_atom_1'] = get(molecular_system, target='atom', group_type=True)
expected_values['group_type_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), group_type=True)

expected_values['component_index_from_atom_1'] = get(molecular_system, target='atom', component_index=True)
expected_values['component_index_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), component_index=True)
expected_values['component_name_from_atom_1'] = get(molecular_system, target='atom', component_name=True)
expected_values['component_name_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), component_name=True)
expected_values['component_id_from_atom_1'] = get(molecular_system, target='atom', component_id=True)
expected_values['component_id_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), component_id=True)
expected_values['component_type_from_atom_1'] = get(molecular_system, target='atom', component_type=True)
expected_values['component_type_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), component_type=True)

expected_values['molecule_index_from_atom_1'] = get(molecular_system, target='atom', molecule_index=True)
expected_values['molecule_index_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), molecule_index=True)
expected_values['molecule_name_from_atom_1'] = get(molecular_system, target='atom', molecule_name=True)
expected_values['molecule_name_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), molecule_name=True)
expected_values['molecule_id_from_atom_1'] = get(molecular_system, target='atom', molecule_id=True)
expected_values['molecule_id_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), molecule_id=True)
expected_values['molecule_type_from_atom_1'] = get(molecular_system, target='atom', molecule_type=True)
expected_values['molecule_type_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), molecule_type=True)

expected_values['chain_index_from_atom_1'] = get(molecular_system, target='atom', chain_index=True)
expected_values['chain_index_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), chain_index=True)
expected_values['chain_name_from_atom_1'] = get(molecular_system, target='atom', chain_name=True)
expected_values['chain_name_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), chain_name=True)
expected_values['chain_id_from_atom_1'] = get(molecular_system, target='atom', chain_id=True)
expected_values['chain_id_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), chain_id=True)
expected_values['chain_type_from_atom_1'] = get(molecular_system, target='atom', chain_type=True)
expected_values['chain_type_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), chain_type=True)

expected_values['entity_index_from_atom_1'] = get(molecular_system, target='atom', entity_index=True)
expected_values['entity_index_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), entity_index=True)
expected_values['entity_name_from_atom_1'] = get(molecular_system, target='atom', entity_name=True)
expected_values['entity_name_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), entity_name=True)
expected_values['entity_id_from_atom_1'] = get(molecular_system, target='atom', entity_id=True)
expected_values['entity_id_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), entity_id=True)
expected_values['entity_type_from_atom_1'] = get(molecular_system, target='atom', entity_type=True)
expected_values['entity_type_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), entity_type=True)

expected_values['n_atoms_from_atom_1'] = get(molecular_system, target='atom', n_atoms=True)
expected_values['n_atoms_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), n_atoms=True)
expected_values['n_groups_from_atom_1'] = get(molecular_system, target='atom', n_groups=True)
expected_values['n_groups_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), n_groups=True)
expected_values['n_components_from_atom_1'] = get(molecular_system, target='atom', n_components=True)
expected_values['n_components_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), n_components=True)
expected_values['n_molecules_from_atom_1'] = get(molecular_system, target='atom', n_molecules=True)
expected_values['n_molecules_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), n_molecules=True)
expected_values['n_chains_from_atom_1'] = get(molecular_system, target='atom', n_chains=True)
expected_values['n_chains_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), n_chains=True)
expected_values['n_entities_from_atom_1'] = get(molecular_system, target='atom', n_entities=True)
expected_values['n_entities_from_atom_2'] = get(molecular_system, target='atom', indices=range(40,80), n_entities=True)



### Pickle ###

with open('1tcd.pickle', 'wb') as f:
    pickle.dump(expected_values, f)

