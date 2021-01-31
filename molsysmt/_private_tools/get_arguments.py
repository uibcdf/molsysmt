from .exceptions import BadCallError

list_topology_get_arguments = [
    'index', 'name', 'id', 'type',
    'atom_index', 'atom_name', 'atom_id', 'atom_type',
    'group_index', 'group_name', 'group_id', 'group_type',
    'component_index', 'component_name', 'component_id', 'component_type',
    'chain_index', 'chain_name', 'chain_id', 'chain_type',
    'molecule_index', 'molecule_name', 'molecule_id', 'molecule_type',
    'entity_index', 'entity_name', 'entity_id', 'entity_type',
    'bond_index', 'bond_id', 'bond_type', 'order', 'bonde_order',
    'bonded_atoms', 'inner_bonded_atoms', 'inner_bond_index',
    'n_atoms', 'n_groups', 'n_components', 'n_chains', 'n_molecules', 'n_entities', 'n_bonds', 'n_inner_bonds',
    'n_aminoacids', 'n_nucleotides', 'n_ions', 'n_waters', 'n_cosolutes', 'n_small_molecules',
    'n_peptides', 'n_proteins', 'n_dnas', 'n_rnas'
]

_normalize = {
    'indices': 'index', 'names': 'name', 'ids': 'id', 'types': 'type',
    'atom_indices': 'atom_index', 'atom_names': 'atom_name', 'atom_ids': 'atom_id', 'atom_types': 'atom_type',
    'group_indices': 'group_index', 'group_names': 'group_name', 'group_ids': 'group_id', 'group_types': 'group_type',
    'component_indices': 'component_index', 'component_names': 'component_name', 'component_ids': 'component_id', 'component_types': 'component_type',
    'chain_indices': 'chain_index', 'chain_names': 'chain_name', 'chain_ids': 'chain_id', 'chain_types': 'chain_type',
    'molecule_indices': 'molecule_index', 'molecule_names': 'molecule_name', 'molecule_ids': 'molecule_id', 'molecule_types': 'molecule_type',
    'entity_indices': 'entity_index', 'entity_names': 'entity_name', 'entity_ids': 'entity_id', 'entity_types': 'entity_type',
    'bond_indices': 'bond_index', 'bond_ids': 'bond_id', 'bond_types': 'bond_type',
    'bonded_atom': 'bonded_atoms', 'inner_bonded_atom': 'inner_bonded_atoms', 'inner_bond_indices': 'inner_bond_index',
    'n_atom': 'n_atoms', 'n_group': 'n_groups', 'n_component': 'n_components', 'n_chain': 'n_chains',
    'n_molecule': 'n_molecules', 'n_entity': 'n_entities', 'n_bond': 'n_bonds', 'n_inner_bond': 'n_inner_bonds',
    'n_aminoacid': 'n_aminoacids', 'n_nucleotide': 'n_nucleotides', 'n_ion': 'n_ions', 'n_water': 'n_waters',
    'n_cosolute': 'n_cosolutes', 'n_small_molecules': 'n_small_molecules', 'n_peptide': 'n_peptides', 'n_protein': 'n_proteins',
    'n_dna': 'n_dnas', 'n_rna': 'n_rnas',
    'residue_indices': 'group_index', 'residue_index': 'group_index', 'residue_names': 'group_name', 'residue_name': 'group_name',
    'residue_ids': 'group_id', 'residue_id': 'group_id', 'residue_types': 'group_type', 'residue_type': 'group_type',
    'n_residues': 'n_groups', 'n_residue': 'n_groups',
}


list_trajectory_get_arguments = [
    'step', 'time', 'frame', 'n_frames', 'n_atoms'
]

_normalize.update({
    'steps': 'step',
    'times': 'time',
    'frames': 'frame',
    'n_frame': 'n_frames',

})

list_coordinates_get_arguments = [
    'coordinates', 'n_frames', 'n_atoms'
]

list_box_get_arguments = [
    'box', 'box_shape', 'box_angles', 'box_lengths', 'box_volume', 'n_frames'
]

list_get_arguments = list_topology_get_arguments + list_trajectory_get_arguments + list_coordinates_get_arguments +\
        list_box_get_arguments

def digest_get_argument(argument):

    tmp_argument = argument.lower()
    if tmp_argument in _normalize:
        tmp_argument = _normalize[tmp_argument]
    if tmp_argument in list_get_arguments:
        return tmp_argument
    else:
        raise BadCallError()

