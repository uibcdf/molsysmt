from molsysmt._private_tools.exceptions import BadCallError

argument_synonyms = {}
attributes_required = {}
reverse_search = {}

# atom_index

argument_synonyms['atom_indices'] = 'atom_index'
attributes_required['atom_index'] = ['atom_index']
reverse_search['atom_index'] = False

# atom_name

argument_synonyms['atom_names'] = 'atom_name'
attributes_required['atom_name'] = ['atom_name']
reverse_search['atom_index'] = False

# atom_id

argument_synonyms['atom_ids'] = 'atom_id'
attributes_required['atom_id'] = ['atom_id']
reverse_search['atom_id'] = False

# atom_type

argument_synonyms['atom_types'] = 'atom_type'
attributes_required['atom_type'] = ['atom_type']
reverse_search['atom_type'] = False

# group_index

argument_synonyms['group_indices'] = 'group_index'
argument_synonyms['residue_indices':] 'group_index',
argument_synonyms['residue_index':] 'group_index',
attributes_required['group_index'] = ['group_index']
reverse_search['group_index'] = False

# group_name

argument_synonyms['group_names'] = 'group_name'
argument_synonyms['residue_names'] = 'group_name'
argument_synonyms['residue_name'] = 'group_name'
attributes_required['group_name'] = ['group_name']
reverse_search['group_name'] = False

# group_id

argument_synonyms['group_ids'] = 'group_id'
argument_synonyms['residue_ids'] = 'group_id'
argument_synonyms['residue_id'] = 'group_id'
attributes_required['group_id'] = ['group_id']
reverse_search['group_id'] = False

# group_type

argument_synonyms['group_types'] = 'group_type'
argument_synonyms['residue_types'] = 'group_type'
argument_synonyms['residue_type'] = 'group_type'
attributes_required['group_type'] = ['group_type']
reverse_search['group_type'] = False

# component_index

argument_synonyms['component_indices'] = 'component_index'
attributes_required['component_index'] = ['component_index']
reverse_search['component_index'] = False

# component_name

argument_synonyms['component_names'] = 'component_name'
attributes_required['component_name'] = ['component_name']
reverse_search['component_name'] = False

# component_id

argument_synonyms['component_ids'] = 'component_id'
attributes_required['component_id'] = ['component_id']
reverse_search['component_id'] = False

# component_type

argument_synonyms['component_types'] = 'component_type'
attributes_required['component_type'] = ['component_type']
reverse_search['component_type'] = False

# chain_index

argument_synonyms['chain_indices'] = 'chain_index'
attributes_required['chain_index'] = ['chain_index']
reverse_search['chain_index'] = False

# chain_name

argument_synonyms['chain_names'] = 'chain_name'
attributes_required['chain_index'] = ['chain_index']
reverse_search['chain_index'] = False

# chain_id

argument_synonyms['chain_ids'] = 'chain_id'
attributes_required['chain_id'] = ['chain_id']
reverse_search['chain_id'] = False

# chain_type

argument_synonyms['chain_types'] = 'chain_type'
attributes_required['chain_type'] = ['chain_type']
reverse_search['chain_type'] = False

# molecule_index

argument_synonyms['molecule_indices'] = 'molecule_index'
attributes_required['molecule_index'] = ['molecule_index']
reverse_search['molecule_index'] = False

# molecule_name

argument_synonyms['molecule_names'] = 'molecule_name'
attributes_required['molecule_name'] = ['molecule_name']
reverse_search['molecule_name'] = False

# molecule_id

argument_synonyms['molecule_ids'] = 'molecule_id'
attributes_required['molecule_id'] = ['molecule_id']
reverse_search['molecule_id'] = False

# molecule_type

argument_synonyms['molecule_types'] = 'molecule_type'
attributes_required['molecule_type'] = ['molecule_type']
reverse_search['molecule_type'] = False

# entity_index

argument_synonyms['entity_indices'] = 'entity_index'
attributes_required['entity_index'] = ['entity_index']
reverse_search['entity_index'] = False

# entity_name

argument_synonyms['entity_names'] = 'entity_name'
attributes_required['entity_name'] = ['entity_name']
reverse_search['entity_name'] = False

# entity_id

argument_synonyms['entity_ids'] = 'entity_id'
attributes_required['entity_id'] = ['entity_id']
reverse_search['entity_id'] = False

# entity_type

argument_synonyms['entity_types'] = 'entity_type'
attributes_required['entity_type'] = ['entity_type']
reverse_search['entity_type'] = False

# bond_index

argument_synonyms['bond_indices'] = 'bond_index'
attributes_required['bond_index'] = ['bond_index']
reverse_search['bond_index'] = False

# bond_id

argument_synonyms['bond_ids'] = 'bond_id'
attributes_required['bond_id'] = ['bond_id']
reverse_search['bond_id'] = False

# bond_type

argument_synonyms['bond_types'] = 'bond_type'

# bonded_atoms

argument_synonyms['bonded_atom'] = 'bond_atoms'

# bonds_order

argument_synonyms['bonds_order'] = 'bond_order'

# inner_bonded_atoms

argument_synonyms['inner_bonded_atom'] = 'inner_bonded_atoms'

# inner_bond_index

argument_synonyms['inner_bond_indices'] = 'inner_bond_index'

# n_atoms

argument_synonyms['n_atom'] = 'n_atoms'

# n_groups

argument_synonyms['n_group'] = 'n_groups'
argument_synonyms['n_residues'] = 'n_groups'
argument_synonyms['n_residue'] = 'n_groups'

# n_components

argument_synonyms['n_component'] = 'n_components'

# n_chains

argument_synonyms['n_chain'] = 'n_chains'

# n_molecules

argument_synonyms['n_molecule'] = 'n_molecules'

# n_bonds

argument_synonyms['n_bond'] = 'n_bonds'

# n_inner_bonds

argument_synonyms['n_inner_bond'] = 'n_inner_bonds'

# n_aminoacids

argument_synonyms['n_aminoacid'] = 'n_aminoacids'

# n_nucleotides

argument_synonyms['n_nucleotide'] = 'n_nucleotides'

# n_ions

argument_synonyms['n_ion'] = 'n_ions'

# n_waters

argument_synonyms['n_water'] = 'n_waters'

# n_cosolutes

argument_synonyms['n_cosolute'] = 'n_cosolute'

# n_small_molecules

argument_synonyms['n_small_molecule'] = 'n_small_molecules'

# n_small_peptides

argument_synonyms['n_small_peptide'] = 'n_small_peptides'

# n_peptides

argument_synonyms['n_peptide'] = 'n_peptides'

# n_proteins

argument_synonyms['n_protein'] = 'n_proteins'

# n_dnas

argument_synonyms['n_dna'] = 'n_dnas'

# n_rnas

argument_synonyms['n_rna'] = 'n_rnas'

# n_lipids

argument_synonyms['n_lipid'] = 'n_lipids'

# step

argument_synonyms['steps'] = 'step'

# time

argument_synonyms['times'] = 'time'

# box

argument_synonyms['boxes'] = 'box'







def digest_argument(argument, target):

    output_argument = argument.lower()
    if output_argument in ['index', 'indices', 'name', 'names', 'id', 'ids', 'type', 'types', 'order']:
        output_argument = ('_').join([target, output_argument])
    if output_argument in argument_synonyms:
        output_argument = argument_synonyms[output_argument]
    if output_argument in arguments:
        return output_argument
    else:
        raise BadCallError()

attributes_required = {

    'n_atoms' : ['elements', 'coordinates'],
    'n_groups' : ['elements'],
    'n_components' : ['elements'],
    'n_chains' : ['elements'],
    'n_molecules' : ['elements'],
    'n_entities' : ['elements'],

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


reverse_search = {

    'n_atoms' : ['elements', 'coordinates'],
    'n_groups' : ['elements'],
    'n_components' : ['elements'],
    'n_chains' : ['elements'],
    'n_molecules' : ['elements'],
    'n_entities' : ['elements'],

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

