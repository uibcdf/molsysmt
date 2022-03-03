from molsysmt._private_tools.exceptions import WrongGetArgumentError

argument_synonyms = {}
required_attributes = {}
required_indices = {}
reverse_search = {}

# atom_index

argument_synonyms['atom_indices'] = 'atom_index'
required_attributes['atom_index'] = ['atom_index']
required_indices['atom_index'] = ['indices']
reverse_search['atom_index'] = False

# atom_name

argument_synonyms['atom_names'] = 'atom_name'
required_attributes['atom_name'] = ['atom_name']
required_indices['atom_name'] = ['indices']
reverse_search['atom_name'] = False

# atom_id

argument_synonyms['atom_ids'] = 'atom_id'
required_attributes['atom_id'] = ['atom_id']
required_indices['atom_id'] = ['indices']
reverse_search['atom_id'] = False

# atom_type

argument_synonyms['atom_types'] = 'atom_type'
required_attributes['atom_type'] = ['atom_type']
required_indices['atom_type'] = ['indices']
reverse_search['atom_type'] = False

# group_index

argument_synonyms['group_indices'] = 'group_index'
argument_synonyms['residue_indices'] = 'group_index'
argument_synonyms['residue_index'] = 'group_index'
required_attributes['group_index'] = ['group_index']
required_indices['group_index'] = ['indices']
reverse_search['group_index'] = False

# group_name

argument_synonyms['group_names'] = 'group_name'
argument_synonyms['residue_names'] = 'group_name'
argument_synonyms['residue_name'] = 'group_name'
required_attributes['group_name'] = ['group_name']
required_indices['group_name'] = ['indices']
reverse_search['group_name'] = False

# group_id

argument_synonyms['group_ids'] = 'group_id'
argument_synonyms['residue_ids'] = 'group_id'
argument_synonyms['residue_id'] = 'group_id'
required_attributes['group_id'] = ['group_id']
required_indices['group_id'] = ['indices']
reverse_search['group_id'] = False

# group_type

argument_synonyms['group_types'] = 'group_type'
argument_synonyms['residue_types'] = 'group_type'
argument_synonyms['residue_type'] = 'group_type'
required_attributes['group_type'] = ['group_type']
required_indices['group_type'] = ['indices']
reverse_search['group_type'] = False

# component_index

argument_synonyms['component_indices'] = 'component_index'
required_attributes['component_index'] = ['component_index']
required_indices['component_index'] = ['indices']
reverse_search['component_index'] = False

# component_name

argument_synonyms['component_names'] = 'component_name'
required_attributes['component_name'] = ['component_name']
required_indices['component_name'] = ['indices']
reverse_search['component_name'] = False

# component_id

argument_synonyms['component_ids'] = 'component_id'
required_attributes['component_id'] = ['component_id']
required_indices['component_id'] = ['indices']
reverse_search['component_id'] = False

# component_type

argument_synonyms['component_types'] = 'component_type'
required_attributes['component_type'] = ['component_type']
required_indices['component_type'] = ['indices']
reverse_search['component_type'] = False

# chain_index

argument_synonyms['chain_indices'] = 'chain_index'
required_attributes['chain_index'] = ['chain_index']
required_indices['chain_index'] = ['indices']
reverse_search['chain_index'] = False

# chain_name

argument_synonyms['chain_names'] = 'chain_name'
required_attributes['chain_name'] = ['chain_name']
required_indices['chain_name'] = ['indices']
reverse_search['chain_name'] = False

# chain_id

argument_synonyms['chain_ids'] = 'chain_id'
required_attributes['chain_id'] = ['chain_id']
required_indices['chain_id'] = ['indices']
reverse_search['chain_id'] = False

# chain_type

argument_synonyms['chain_types'] = 'chain_type'
required_attributes['chain_type'] = ['chain_type']
required_indices['chain_type'] = ['indices']
reverse_search['chain_type'] = False

# molecule_index

argument_synonyms['molecule_indices'] = 'molecule_index'
required_attributes['molecule_index'] = ['molecule_index']
required_indices['molecule_index'] = ['indices']
reverse_search['molecule_index'] = False

# molecule_name

argument_synonyms['molecule_names'] = 'molecule_name'
required_attributes['molecule_name'] = ['molecule_name']
required_indices['molecule_name'] = ['indices']
reverse_search['molecule_name'] = False

# molecule_id

argument_synonyms['molecule_ids'] = 'molecule_id'
required_attributes['molecule_id'] = ['molecule_id']
required_indices['molecule_id'] = ['indices']
reverse_search['molecule_id'] = False

# molecule_type

argument_synonyms['molecule_types'] = 'molecule_type'
required_attributes['molecule_type'] = ['molecule_type']
required_indices['molecule_type'] = ['indices']
reverse_search['molecule_type'] = False

# entity_index

argument_synonyms['entity_indices'] = 'entity_index'
required_attributes['entity_index'] = ['entity_index']
required_indices['entity_index'] = ['indices']
reverse_search['entity_index'] = False

# entity_name

argument_synonyms['entity_names'] = 'entity_name'
required_attributes['entity_name'] = ['entity_name']
required_indices['entity_name'] = ['indices']
reverse_search['entity_name'] = False

# entity_id

argument_synonyms['entity_ids'] = 'entity_id'
required_attributes['entity_id'] = ['entity_id']
required_indices['entity_id'] = ['indices']
reverse_search['entity_id'] = False

# entity_type

argument_synonyms['entity_types'] = 'entity_type'
required_attributes['entity_type'] = ['entity_type']
required_indices['entity_type'] = ['indices']
reverse_search['entity_type'] = False

# bond_index

argument_synonyms['bond_indices'] = 'bond_index'
required_attributes['bond_index'] = ['bond_index']
required_indices['bond_index'] = ['indices']
reverse_search['bond_index'] = False

# bond_id

argument_synonyms['bond_ids'] = 'bond_id'
required_attributes['bond_id'] = ['bond_id']
required_indices['bond_id'] = ['indices']
reverse_search['bond_id'] = False

# bond_type

argument_synonyms['bond_types'] = 'bond_type'
required_attributes['bond_type'] = ['bond_type']
required_indices['bond_type'] = ['indices']
reverse_search['bond_type'] = False

# bonds_order

argument_synonyms['bonds_order'] = 'bond_order'
required_attributes['bonds_order'] = ['bond_order']
required_indices['bond_order'] = ['indices']
reverse_search['bond_order'] = False

# bonded_atoms

argument_synonyms['bonded_atom'] = 'bond_atoms'
required_attributes['bonded_atoms'] = ['bonded_atoms']
required_indices['bonded_atoms'] = ['indices']
reverse_search['bonded_atoms'] = False

# inner_bonded_atoms
argument_synonyms['inner_bonded_atom'] = 'inner_bonded_atoms'
required_attributes['inner_bonded_atoms'] = ['bonded_atoms']
required_indices['inner_bonded_atoms'] = ['indices']
reverse_search['inner_bonded_atoms'] = False

# inner_bond_index

argument_synonyms['inner_bond_indices'] = 'inner_bond_index'
required_attributes['inner_bond_index'] = ['bond_index']
required_indices['inner_bond_index'] = ['indices']
reverse_search['inner_bond_index'] = False

# n_atoms

argument_synonyms['n_atom'] = 'n_atoms'
required_attributes['n_atoms'] = ['atom_index', 'coordinates']
required_indices['n_atoms'] = ['indices']
reverse_search['n_atoms'] = False

# n_groups

argument_synonyms['n_group'] = 'n_groups'
argument_synonyms['n_residues'] = 'n_groups'
argument_synonyms['n_residue'] = 'n_groups'
required_attributes['n_groups'] = ['group_index']
required_indices['n_groups'] = ['indices']
reverse_search['n_groups'] = False

# n_components

argument_synonyms['n_component'] = 'n_components'
required_attributes['n_components'] = ['component_index']
required_indices['n_components'] = ['indices']
reverse_search['n_components'] = False

# n_chains

argument_synonyms['n_chain'] = 'n_chains'
required_attributes['n_chains'] = ['chain_index']
required_indices['n_chains'] = ['indices']
reverse_search['n_chains'] = False

# n_molecules

argument_synonyms['n_molecule'] = 'n_molecules'
required_attributes['n_molecules'] = ['molecule_index']
required_indices['n_molecules'] = ['indices']
reverse_search['n_molecules'] = False

# n_entities

argument_synonyms['n_entity'] = 'n_entities'
required_attributes['n_entities'] = ['entity_index']
required_indices['n_entities'] = ['indices']
reverse_search['n_entities'] = False

# n_bonds

argument_synonyms['n_bond'] = 'n_bonds'
required_attributes['n_bonds'] = ['bond_index']
required_indices['n_bonds'] = ['indices']
reverse_search['n_bonds'] = False

# n_inner_bonds

argument_synonyms['n_inner_bond'] = 'n_inner_bonds'
required_attributes['n_inner_bonds'] = ['bond_index']
required_indices['n_inner_bonds'] = ['indices']
reverse_search['n_inner_bonds'] = False

# n_aminoacids

argument_synonyms['n_aminoacid'] = 'n_aminoacids'
required_attributes['n_aminoacids'] = ['group_type']
required_indices['n_aminoacids'] = ['indices']
reverse_search['n_aminoacids'] = False

# n_nucleotides

argument_synonyms['n_nucleotide'] = 'n_nucleotides'
required_attributes['n_nucleotides'] = ['group_type']
required_indices['n_nucleotides'] = ['indices']
reverse_search['n_nucleotides'] = False

# n_ions

argument_synonyms['n_ion'] = 'n_ions'
required_attributes['n_ions'] = ['group_type']
required_indices['n_ions'] = ['indices']
reverse_search['n_ions'] = False

# n_waters

argument_synonyms['n_water'] = 'n_waters'
required_attributes['n_waters'] = ['group_type']
required_indices['n_waters'] = ['indices']
reverse_search['n_waters'] = False

# n_cosolutes

argument_synonyms['n_cosolute'] = 'n_cosolute'
required_attributes['n_cosolutes'] = ['group_type']
required_indices['n_cosolutes'] = ['indices']
reverse_search['n_cosolutes'] = False

# n_small_molecules

argument_synonyms['n_small_molecule'] = 'n_small_molecules'
required_attributes['n_small_molecules'] = ['group_type']
required_indices['n_small_molecules'] = ['indices']
reverse_search['n_small_molecules'] = False

# n_peptides

argument_synonyms['n_peptide'] = 'n_peptides'
required_attributes['n_peptides'] = ['molecule_type']
required_indices['n_peptides'] = ['indices']
reverse_search['n_peptides'] = False

# n_proteins

argument_synonyms['n_protein'] = 'n_proteins'
required_attributes['n_proteins'] = ['molecule_type']
required_indices['n_proteins'] = ['indices']
reverse_search['n_proteins'] = False

# n_dnas

argument_synonyms['n_dna'] = 'n_dnas'
required_attributes['n_dnas'] = ['molecule_type']
required_indices['n_dnas'] = ['indices']
reverse_search['n_dnas'] = False

# n_rnas

argument_synonyms['n_rna'] = 'n_rnas'
required_attributes['n_rnas'] = ['molecule_type']
required_indices['n_rnas'] = ['indices']
reverse_search['n_rnas'] = False

# n_lipids

argument_synonyms['n_lipid'] = 'n_lipids'
required_attributes['n_lipids'] = ['group_type']
required_indices['n_lipids'] = ['indices']
reverse_search['n_lipids'] = False

# step

argument_synonyms['steps'] = 'step'
required_attributes['step'] = ['step']
required_indices['step'] = ['structure_indices']
reverse_search['step'] = True

# time

argument_synonyms['times'] = 'time'
required_attributes['time'] = ['time']
required_indices['time'] = ['structure_indices']
reverse_search['time'] = True

# box

argument_synonyms['boxes'] = 'box'
required_attributes['box'] = ['box']
required_indices['box'] = ['structure_indices']
reverse_search['box'] = True

# box_shape

required_attributes['box_shape'] = ['box']
required_indices['box_shape'] = ['structure_indices']
reverse_search['box_shape'] = True

# box_angles

required_attributes['box_angles'] = ['box']
required_indices['box_angles'] = ['structure_indices']
reverse_search['box_angles'] = True

# box_lengths

required_attributes['box_lengths'] = ['box']
required_indices['box_lengths'] = ['structure_indices']
reverse_search['box_lengths'] = True

# box_volume

required_attributes['box_volume'] = ['box']
required_indices['box_volume'] = ['structure_indices']
reverse_search['box_volume'] = True

# coordinates
argument_synonyms['coordinate'] = 'coordinates'
argument_synonyms['positions'] = 'coordinates'
argument_synonyms['position'] = 'coordinates'
required_attributes['coordinates'] = ['coordinates']
required_indices['coordinates'] = ['indices', 'structure_indices']
reverse_search['coordinates'] = True

# n_structures
argument_synonyms['n_structure'] = 'n_structures'
required_attributes['n_structures'] = ['coordinates', 'box']
required_indices['n_structures'] = []
reverse_search['n_structures'] = True


arguments = required_attributes.keys()

def digest_argument(argument, target):

    output_argument = argument.lower()
    if output_argument in ['index', 'indices', 'name', 'names', 'id', 'ids', 'type', 'types', 'order']:
        output_argument = ('_').join([target, output_argument])
    if output_argument in argument_synonyms:
        output_argument = argument_synonyms[output_argument]
    if output_argument in arguments:
        return output_argument
    else:
        raise WrongGetArgumentError()

