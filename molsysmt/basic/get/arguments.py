from molsysmt._private_tools.exceptions import BadCallError

where_argument = {

    'atom_index' : ['elements'],
    'atom_name' : ['elements'],
    'atom_id' : ['elements'],
    'atom_type' : ['elements'],
    'group_index' : ['elements'],
    'group_name' : ['elements'],
    'group_id' : ['elements'],
    'group_type' : ['elements'],
    'component_index' : ['elements'],
    'component_name' : ['elements'],
    'component_id' : ['elements'],
    'component_type' : ['elements'],
    'chain_index' : ['elements'],
    'chain_name' : ['elements'],
    'chain_id' : ['elements'],
    'chain_type' : ['elements'],
    'molecule_index' : ['elements'],
    'molecule_name' : ['elements'],
    'molecule_id' : ['elements'],
    'molecule_type' : ['elements'],
    'entity_index' : ['elements'],
    'entity_name' : ['elements'],
    'entity_id' : ['elements'],
    'entity_type' : ['elements'],

    'n_atoms' : ['elements', 'coordinates'],
    'n_groups' : ['elements'],
    'n_components' : ['elements'],
    'n_chains' : ['elements'],
    'n_molecules' : ['elements'],
    'n_entities' : ['elements'],

    'bond_index' : ['bonds'],
    'bond_name' : ['bonds'],
    'bond_id' : ['bonds'],
    'bond_type' : ['bonds'],
    'bond_order' : ['bonds'],
    'bonded_atoms' : ['bonds'],
    'inner_bonded_atoms' : ['bonds'],
    'inner_bond_index' : ['bonds'],
    'n_bonds' : ['bonds'],
    'n_inner_bonds' : ['bonds'],

    'n_aminoacids' : ['elements'],
    'n_nucleotides' : ['elements'],
    'n_ions' : ['elements'],
    'n_waters' : ['elements'],
    'n_cosolutes' : ['elements'],
    'n_small_molecules' : ['elements'],
    'n_peptides' : ['elements'],
    'n_proteins' : ['elements'],
    'n_dnas' : ['elements'],
    'n_rnas' : ['elements'],
    'n_lipids' : ['elements'],

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


argument_synonyms = {
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
    'bonds_order': 'bond_order',
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
    'n_lipid': 'n_lipids',
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


arguments = list(where_argument.keys())

def digest_argument(argument, target):

    output_argument = output_argument.lower()
    if output_argument in ['index', 'indices', 'name', 'names', 'id', 'ids', 'type', 'types', 'order']:
        output_argument = ('_').join([target, output_argument])
    if output_argument in argument_synonyms:
        output_argument = argument_synonyms[output_argument]
    if output_argument in arguments:
        return output_argument
    else:
        raise BadCallError()

