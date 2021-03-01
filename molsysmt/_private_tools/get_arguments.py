from molsysmt._private_tools.exceptions import BadCallError

where_get_argument = {

    'atom_index' : ['topology'],
    'atom_name' : ['topology'],
    'atom_id' : ['topology'],
    'atom_type' : ['topology'],
    'group_index' : ['topology'],
    'group_name' : ['topology'],
    'group_id' : ['topology'],
    'group_type' : ['topology'],
    'component_index' : ['topology'],
    'component_name' : ['topology'],
    'component_id' : ['topology'],
    'component_type' : ['topology'],
    'chain_index' : ['topology'],
    'chain_name' : ['topology'],
    'chain_id' : ['topology'],
    'chain_type' : ['topology'],
    'molecule_index' : ['topology'],
    'molecule_name' : ['topology'],
    'molecule_id' : ['topology'],
    'molecule_type' : ['topology'],
    'entity_index' : ['topology'],
    'entity_name' : ['topology'],
    'entity_id' : ['topology'],
    'entity_type' : ['topology'],

    'n_atoms' : ['topology', 'coordinates'],
    'n_groups' : ['topology'],
    'n_components' : ['topology'],
    'n_chains' : ['topology'],
    'n_molecules' : ['topology'],
    'n_entities' : ['topology'],

    'bond_index' : ['bonds'],
    'bond_name' : ['bonds'],
    'bond_id' : ['bonds'],
    'bond_type' : ['bonds'],
    'bonded_atoms' : ['bonds'],
    'inner_bonded_atoms' : ['bonds'],
    'inner_bond_index' : ['bonds'],
    'n_bonds' : ['bonds'],
    'n_inner_bonds' : ['bonds'],

    'n_aminoacids' : ['topology'],
    'n_nucleotides' : ['topology'],
    'n_ions' : ['topology'],
    'n_waters' : ['topology'],
    'n_cosolutes' : ['topology'],
    'n_small_molecules' : ['topology'],
    'n_peptides' : ['topology'],
    'n_proteins' : ['topology'],
    'n_dnas' : ['topology'],
    'n_rnas' : ['topology'],

    'step' : ['coordinates'],
    'time' : ['coordinates'],
    'frame' : ['coordinates'],
    'n_frames' : ['coordinates', 'box'],
    'coordinates' : ['coordinates'],

    'box' : ['box'],
    'box_shape' : ['box'],
    'box_angles' : ['box'],
    'box_lengths' : ['box'],
    'box_volume' : ['box'],

}


get_argument_synonym = {
    'atom_indices': 'atom_index',
    'atom_names': 'atom_name',
    'atom_ids': 'atom_id',
    'atom_types': 'atom_type',
    'group_indices': 'group_index',
    'group_names': 'group_name',
    'group_ids': 'group_id',
    'group_types': 'group_type',
    'component_indices': 'component_index',
    'component_names': 'component_name',
    'component_ids': 'component_id',
    'component_types': 'component_type',
    'chain_indices': 'chain_index',
    'chain_names': 'chain_name',
    'chain_ids': 'chain_id',
    'chain_types': 'chain_type',
    'molecule_indices': 'molecule_index',
    'molecule_names': 'molecule_name',
    'molecule_ids': 'molecule_id',
    'molecule_types': 'molecule_type',
    'entity_indices': 'entity_index',
    'entity_names': 'entity_name',
    'entity_ids': 'entity_id',
    'entity_types': 'entity_type',
    'bond_indices': 'bond_index',
    'bond_ids': 'bond_id',
    'bond_types': 'bond_type',
    'bonded_atom': 'bonded_atoms',
    'inner_bonded_atom': 'inner_bonded_atoms',
    'inner_bond_indices': 'inner_bond_index',
    'n_atom': 'n_atoms',
    'n_group': 'n_groups',
    'n_component': 'n_components',
    'n_chain': 'n_chains',
    'n_molecule': 'n_molecules',
    'n_entity': 'n_entities',
    'n_bond': 'n_bonds',
    'n_inner_bond': 'n_inner_bonds',
    'n_aminoacid': 'n_aminoacids',
    'n_nucleotide': 'n_nucleotides',
    'n_ion': 'n_ions',
    'n_water': 'n_waters',
    'n_cosolute': 'n_cosolutes',
    'n_small_molecule': 'n_small_molecules',
    'n_peptide': 'n_peptides',
    'n_protein': 'n_proteins',
    'n_dna': 'n_dnas',
    'n_rna': 'n_rnas',
    'residue_indices': 'group_index',
    'residue_index': 'group_index',
    'residue_names': 'group_name',
    'residue_name': 'group_name',
    'residue_ids': 'group_id',
    'residue_id': 'group_id',
    'residue_types': 'group_type',
    'residue_type': 'group_type',
    'n_residues': 'n_groups',
    'n_residue': 'n_groups',
    'steps': 'step',
    'times': 'time',
    'frames': 'frame',
    'n_frame': 'n_frames',
}


get_arguments = list(where_get_argument.keys())

def digest_get_argument(get_argument, target):

    tmp_get_argument = get_argument.lower()
    if tmp_get_argument in ['index', 'indices', 'name', 'names', 'id', 'ids', 'type', 'types']:
        tmp_get_argument = ('_').join([target, get_argument])
    if tmp_get_argument in get_argument_synonym:
        tmp_get_argument = get_argument_synonymn[tmp_get_argument]
    if tmp_get_argument in get_arguments:
        return tmp_get_argument
    else:
        raise BadCallError()

