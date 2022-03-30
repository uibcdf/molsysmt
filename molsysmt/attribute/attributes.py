attributes = []
attribute_synonyms = {}
_required_attributes = {}
_required_indices = {}
_reverse_search_in_molecular_system = {}

# atom_index

attributes.append('atom_index')
attribute_synonyms['atom_indices'] = 'atom_index'

_required_attributes['atom_index'] = ['atom_index']
_required_indices['atom_index'] = ['indices']
_reverse_search_in_molecular_system['atom_index'] = False

# atom_name

attributes.append('atom_name')
attribute_synonyms['atom_names'] = 'atom_name'

_required_attributes['atom_name'] = ['atom_name']
_required_indices['atom_name'] = ['indices']
_reverse_search_in_molecular_system['atom_name'] = False

# atom_id

attributes.append('atom_id')
attribute_synonyms['atom_ids'] = 'atom_id'

_required_attributes['atom_id'] = ['atom_id']
_required_indices['atom_id'] = ['indices']
_reverse_search_in_molecular_system['atom_id'] = False

# atom_type

attributes.append('atom_type')
attribute_synonyms['atom_types'] = 'atom_type'

_required_attributes['atom_type'] = ['atom_type']
_required_indices['atom_type'] = ['indices']
_reverse_search_in_molecular_system['atom_type'] = False

# group_index

attributes.append('group_index')
attribute_synonyms['group_indices'] = 'group_index'
attribute_synonyms['residue_indices'] = 'group_index'
attribute_synonyms['residue_index'] = 'group_index'

_required_attributes['group_index'] = ['group_index']
_required_indices['group_index'] = ['indices']
_reverse_search_in_molecular_system['group_index'] = False

# group_name

attributes.append('group_name')
attribute_synonyms['group_names'] = 'group_name'
attribute_synonyms['residue_names'] = 'group_name'
attribute_synonyms['residue_name'] = 'group_name'

_required_attributes['group_name'] = ['group_name']
_required_indices['group_name'] = ['indices']
_reverse_search_in_molecular_system['group_name'] = False

# group_id

attributes.append('group_id')
attribute_synonyms['group_ids'] = 'group_id'
attribute_synonyms['residue_ids'] = 'group_id'
attribute_synonyms['residue_id'] = 'group_id'

_required_attributes['group_id'] = ['group_id']
_required_indices['group_id'] = ['indices']
_reverse_search_in_molecular_system['group_id'] = False

# group_type

attributes.append('group_type')
attribute_synonyms['group_types'] = 'group_type'
attribute_synonyms['residue_types'] = 'group_type'
attribute_synonyms['residue_type'] = 'group_type'

_required_attributes['group_type'] = ['group_type']
_required_indices['group_type'] = ['indices']
_reverse_search_in_molecular_system['group_type'] = False

# component_index

attributes.append('component_index')
attribute_synonyms['component_indices'] = 'component_index'

_required_attributes['component_index'] = ['component_index']
_required_indices['component_index'] = ['indices']
_reverse_search_in_molecular_system['component_index'] = False

# component_name

attributes.append('component_name')
attribute_synonyms['component_names'] = 'component_name'

_required_attributes['component_name'] = ['component_name']
_required_indices['component_name'] = ['indices']
_reverse_search_in_molecular_system['component_name'] = False

# component_id

attributes.append('component_id')
attribute_synonyms['component_ids'] = 'component_id'

_required_attributes['component_id'] = ['component_id']
_required_indices['component_id'] = ['indices']
_reverse_search_in_molecular_system['component_id'] = False

# component_type

attributes.append('component_type')
attribute_synonyms['component_types'] = 'component_type'

_required_attributes['component_type'] = ['component_type']
_required_indices['component_type'] = ['indices']
_reverse_search_in_molecular_system['component_type'] = False

# chain_index

attribute_synonyms['chain_indices'] = 'chain_index'
required_attributes['chain_index'] = ['chain_index']
required_indices['chain_index'] = ['indices']
reverse_search_in_molecular_system['chain_index'] = False

# chain_name

attribute_synonyms['chain_names'] = 'chain_name'
required_attributes['chain_name'] = ['chain_name']
required_indices['chain_name'] = ['indices']
reverse_search_in_molecular_system['chain_name'] = False

# chain_id

attribute_synonyms['chain_ids'] = 'chain_id'
required_attributes['chain_id'] = ['chain_id']
required_indices['chain_id'] = ['indices']
reverse_search_in_molecular_system['chain_id'] = False

# chain_type

attribute_synonyms['chain_types'] = 'chain_type'
required_attributes['chain_type'] = ['chain_type']
required_indices['chain_type'] = ['indices']
reverse_search_in_molecular_system['chain_type'] = False

# molecule_index

attribute_synonyms['molecule_indices'] = 'molecule_index'
required_attributes['molecule_index'] = ['molecule_index']
required_indices['molecule_index'] = ['indices']
reverse_search_in_molecular_system['molecule_index'] = False

# molecule_name

attribute_synonyms['molecule_names'] = 'molecule_name'
required_attributes['molecule_name'] = ['molecule_name']
required_indices['molecule_name'] = ['indices']
reverse_search_in_molecular_system['molecule_name'] = False

# molecule_id

attribute_synonyms['molecule_ids'] = 'molecule_id'
required_attributes['molecule_id'] = ['molecule_id']
required_indices['molecule_id'] = ['indices']
reverse_search_in_molecular_system['molecule_id'] = False

# molecule_type

attribute_synonyms['molecule_types'] = 'molecule_type'
required_attributes['molecule_type'] = ['molecule_type']
required_indices['molecule_type'] = ['indices']
reverse_search_in_molecular_system['molecule_type'] = False

# entity_index

attribute_synonyms['entity_indices'] = 'entity_index'
required_attributes['entity_index'] = ['entity_index']
required_indices['entity_index'] = ['indices']
reverse_search_in_molecular_system['entity_index'] = False

# entity_name

attribute_synonyms['entity_names'] = 'entity_name'
required_attributes['entity_name'] = ['entity_name']
required_indices['entity_name'] = ['indices']
reverse_search_in_molecular_system['entity_name'] = False

# entity_id

attribute_synonyms['entity_ids'] = 'entity_id'
required_attributes['entity_id'] = ['entity_id']
required_indices['entity_id'] = ['indices']
reverse_search_in_molecular_system['entity_id'] = False

# entity_type

attribute_synonyms['entity_types'] = 'entity_type'
required_attributes['entity_type'] = ['entity_type']
required_indices['entity_type'] = ['indices']
reverse_search_in_molecular_system['entity_type'] = False

# bond_index

attribute_synonyms['bond_indices'] = 'bond_index'
required_attributes['bond_index'] = ['bond_index']
required_indices['bond_index'] = ['indices']
reverse_search_in_molecular_system['bond_index'] = False

# bond_id

attribute_synonyms['bond_ids'] = 'bond_id'
required_attributes['bond_id'] = ['bond_id']
required_indices['bond_id'] = ['indices']
reverse_search_in_molecular_system['bond_id'] = False

# bond_type

attribute_synonyms['bond_types'] = 'bond_type'
required_attributes['bond_type'] = ['bond_type']
required_indices['bond_type'] = ['indices']
reverse_search_in_molecular_system['bond_type'] = False

# bonds_order

attribute_synonyms['bonds_order'] = 'bond_order'
required_attributes['bonds_order'] = ['bond_order']
required_indices['bond_order'] = ['indices']
reverse_search_in_molecular_system['bond_order'] = False

# bonded_atoms

attribute_synonyms['bonded_atom'] = 'bond_atoms'
required_attributes['bonded_atoms'] = ['bonded_atoms']
required_indices['bonded_atoms'] = ['indices']
reverse_search_in_molecular_system['bonded_atoms'] = False

# inner_bonded_atoms
attribute_synonyms['inner_bonded_atom'] = 'inner_bonded_atoms'
required_attributes['inner_bonded_atoms'] = ['bonded_atoms']
required_indices['inner_bonded_atoms'] = ['indices']
reverse_search_in_molecular_system['inner_bonded_atoms'] = False

# inner_bond_index

attribute_synonyms['inner_bond_indices'] = 'inner_bond_index'
required_attributes['inner_bond_index'] = ['bond_index']
required_indices['inner_bond_index'] = ['indices']
reverse_search_in_molecular_system['inner_bond_index'] = False

# n_atoms

attribute_synonyms['n_atom'] = 'n_atoms'
required_attributes['n_atoms'] = ['atom_index', 'coordinates']
required_indices['n_atoms'] = ['indices']
reverse_search_in_molecular_system['n_atoms'] = False

# n_groups

attribute_synonyms['n_group'] = 'n_groups'
attribute_synonyms['n_residues'] = 'n_groups'
attribute_synonyms['n_residue'] = 'n_groups'
required_attributes['n_groups'] = ['group_index']
required_indices['n_groups'] = ['indices']
reverse_search_in_molecular_system['n_groups'] = False

# n_components

attribute_synonyms['n_component'] = 'n_components'
required_attributes['n_components'] = ['component_index']
required_indices['n_components'] = ['indices']
reverse_search_in_molecular_system['n_components'] = False

# n_chains

attribute_synonyms['n_chain'] = 'n_chains'
required_attributes['n_chains'] = ['chain_index']
required_indices['n_chains'] = ['indices']
reverse_search_in_molecular_system['n_chains'] = False

# n_molecules

attribute_synonyms['n_molecule'] = 'n_molecules'
required_attributes['n_molecules'] = ['molecule_index']
required_indices['n_molecules'] = ['indices']
reverse_search_in_molecular_system['n_molecules'] = False

# n_entities

attribute_synonyms['n_entity'] = 'n_entities'
required_attributes['n_entities'] = ['entity_index']
required_indices['n_entities'] = ['indices']
reverse_search_in_molecular_system['n_entities'] = False

# n_bonds

attribute_synonyms['n_bond'] = 'n_bonds'
required_attributes['n_bonds'] = ['bond_index']
required_indices['n_bonds'] = ['indices']
reverse_search_in_molecular_system['n_bonds'] = False

# n_inner_bonds

attribute_synonyms['n_inner_bond'] = 'n_inner_bonds'
required_attributes['n_inner_bonds'] = ['bond_index']
required_indices['n_inner_bonds'] = ['indices']
reverse_search_in_molecular_system['n_inner_bonds'] = False

# n_aminoacids

attribute_synonyms['n_aminoacid'] = 'n_aminoacids'
required_attributes['n_aminoacids'] = ['group_type']
required_indices['n_aminoacids'] = ['indices']
reverse_search_in_molecular_system['n_aminoacids'] = False

# n_nucleotides

attribute_synonyms['n_nucleotide'] = 'n_nucleotides'
required_attributes['n_nucleotides'] = ['group_type']
required_indices['n_nucleotides'] = ['indices']
reverse_search_in_molecular_system['n_nucleotides'] = False

# n_ions

attribute_synonyms['n_ion'] = 'n_ions'
required_attributes['n_ions'] = ['group_type']
required_indices['n_ions'] = ['indices']
reverse_search_in_molecular_system['n_ions'] = False

# n_waters

attribute_synonyms['n_water'] = 'n_waters'
required_attributes['n_waters'] = ['group_type']
required_indices['n_waters'] = ['indices']
reverse_search_in_molecular_system['n_waters'] = False

# n_cosolutes

attribute_synonyms['n_cosolute'] = 'n_cosolute'
required_attributes['n_cosolutes'] = ['group_type']
required_indices['n_cosolutes'] = ['indices']
reverse_search_in_molecular_system['n_cosolutes'] = False

# n_small_molecules

attribute_synonyms['n_small_molecule'] = 'n_small_molecules'
required_attributes['n_small_molecules'] = ['group_type']
required_indices['n_small_molecules'] = ['indices']
reverse_search_in_molecular_system['n_small_molecules'] = False

# n_peptides

attribute_synonyms['n_peptide'] = 'n_peptides'
required_attributes['n_peptides'] = ['molecule_type']
required_indices['n_peptides'] = ['indices']
reverse_search_in_molecular_system['n_peptides'] = False

# n_proteins

attribute_synonyms['n_protein'] = 'n_proteins'
required_attributes['n_proteins'] = ['molecule_type']
required_indices['n_proteins'] = ['indices']
reverse_search_in_molecular_system['n_proteins'] = False

# n_dnas

attribute_synonyms['n_dna'] = 'n_dnas'
required_attributes['n_dnas'] = ['molecule_type']
required_indices['n_dnas'] = ['indices']
reverse_search_in_molecular_system['n_dnas'] = False

# n_rnas

attribute_synonyms['n_rna'] = 'n_rnas'
required_attributes['n_rnas'] = ['molecule_type']
required_indices['n_rnas'] = ['indices']
reverse_search_in_molecular_system['n_rnas'] = False

# n_lipids

attribute_synonyms['n_lipid'] = 'n_lipids'
required_attributes['n_lipids'] = ['group_type']
required_indices['n_lipids'] = ['indices']
reverse_search_in_molecular_system['n_lipids'] = False

# step

attribute_synonyms['steps'] = 'step'
required_attributes['step'] = ['step']
required_indices['step'] = ['structure_indices']
reverse_search_in_molecular_system['step'] = True

# time

attribute_synonyms['times'] = 'time'
required_attributes['time'] = ['time']
required_indices['time'] = ['structure_indices']
reverse_search_in_molecular_system['time'] = True

# box

attribute_synonyms['boxes'] = 'box'
required_attributes['box'] = ['box']
required_indices['box'] = ['structure_indices']
reverse_search_in_molecular_system['box'] = True

# box_shape

required_attributes['box_shape'] = ['box']
required_indices['box_shape'] = ['structure_indices']
reverse_search_in_molecular_system['box_shape'] = True

# box_angles

required_attributes['box_angles'] = ['box']
required_indices['box_angles'] = ['structure_indices']
reverse_search_in_molecular_system['box_angles'] = True

# box_lengths

required_attributes['box_lengths'] = ['box']
required_indices['box_lengths'] = ['structure_indices']
reverse_search_in_molecular_system['box_lengths'] = True

# box_volume

required_attributes['box_volume'] = ['box']
required_indices['box_volume'] = ['structure_indices']
reverse_search_in_molecular_system['box_volume'] = True

# coordinates
attribute_synonyms['coordinate'] = 'coordinates'
attribute_synonyms['positions'] = 'coordinates'
attribute_synonyms['position'] = 'coordinates'
required_attributes['coordinates'] = ['coordinates']
required_indices['coordinates'] = ['indices', 'structure_indices']
reverse_search_in_molecular_system['coordinates'] = True

# n_structures
attribute_synonyms['n_structure'] = 'n_structures'
required_attributes['n_structures'] = ['coordinates', 'box']
required_indices['n_structures'] = []
reverse_search_in_molecular_system['n_structures'] = True



