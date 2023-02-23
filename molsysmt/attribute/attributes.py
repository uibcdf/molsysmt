attributes = []
attribute_synonyms = {}
required_indices = {}
topological_attributes = []
structural_attributes = []
mechanical_attributes = []


def add_attribute(name, synonyms=[], element_indices=False, structural_indices=False,
        topological=False, structural=False, mechanical=False):

    attributes.append(name)
    for alternative_name in synonyms:
        attribute_synonyms[alternative_name]=name
    required_indices[name]=[]
    if element_indices:
        required_indices[name].append('element_indices')
    if structural_indices:
        required_indices[name].append('structural_indices')
    if topological:
        topological_attributes.append(name)
    if structural:
        structural_attributes.append(name)
    if mechanical:
        mechanical_attributes.append(name)

###
### TOPOLOGICAL ATTRIBUTES
###

add_attribute('atom_index', synonyms=['atom_indices'], element_indices=True, topological=True)
add_attribute('atom_name', synonyms=['atom_names'], element_indices=True, topological=True)
add_attribute('atom_id', synonyms=['atom_ids'], element_indices=True, topological=True)
add_attribute('atom_type', synonyms=['atom_types'], element_indices=True, topological=True)
add_attribute('group_index', synonyms=['group_indices', 'residue_indices', 'residue_index'], element_indices=True, topological=True)
add_attribute('group_name', synonyms=['group_names', 'residue_names', 'residue_name'], element_indices=True, topological=True)
add_attribute('group_id', synonyms=['group_ids', 'residue_ids', 'residue_id'], element_indices=True, topological=True)
add_attribute('group_type', synonyms=['group_types', 'residue_types', 'residue_type'], element_indices=True, topological=True)
add_attribute('component_index', synonyms=['component_indices'], element_indices=True, topological=True)
add_attribute('component_name', synonyms=['component_names'], element_indices=True, topological=True)
add_attribute('component_id', synonyms=['component_ids'], element_indices=True, topological=True)
add_attribute('component_type', synonyms=['component_types'], element_indices=True, topological=True)
add_attribute('chain_index', synonyms=['chain_indices'], element_indices=True, topological=True)
add_attribute('chain_name', synonyms=['chain_names'], element_indices=True, topological=True)
add_attribute('chain_id', synonyms=['chain_ids'], element_indices=True, topological=True)
add_attribute('chain_type', synonyms=['chain_types'], element_indices=True, topological=True)
add_attribute('molecule_index', synonyms=['molecule_indices'], element_indices=True, topological=True)
add_attribute('molecule_name', synonyms=['molecule_names'], element_indices=True, topological=True)
add_attribute('molecule_id', synonyms=['molecule_ids'], element_indices=True, topological=True)
add_attribute('molecule_type', synonyms=['molecule_types'], element_indices=True, topological=True)
add_attribute('entity_index', synonyms=['entity_indices'], element_indices=True, topological=True)
add_attribute('entity_name', synonyms=['entity_names'], element_indices=True, topological=True)
add_attribute('entity_id', synonyms=['entity_ids'], element_indices=True, topological=True)
add_attribute('entity_type', synonyms=['entity_types'], element_indices=True, topological=True)
add_attribute('bond_index', synonyms=['bond_indices'], element_indices=True, topological=True)
add_attribute('bond_id', synonyms=['bond_ids'], element_indices=True, topological=True)
add_attribute('bond_type', synonyms=['bond_types'], element_indices=True, topological=True)



# bond_order

attributes.append('bond_order')
attribute_synonyms['bonds_order'] = 'bond_order'

required_indices['bond_order'] = ['element_indices']

topological_attributes.append('bond_order')

# bonded_atoms

attributes.append('bonded_atoms')
attribute_synonyms['bonded_atom'] = 'bonded_atoms'

required_indices['bonded_atoms'] = ['element_indices']

topological_attributes.append('bonded_atoms')

# inner_bonded_atoms

attributes.append('inner_bonded_atoms')
attribute_synonyms['inner_bonded_atom'] = 'inner_bonded_atoms'

required_indices['inner_bonded_atoms'] = ['element_indices']

topological_attributes.append('inner_bonded_atoms')

# inner_bond_index

attributes.append('inner_bond_index')
attribute_synonyms['inner_bond_indices'] = 'inner_bond_index'

required_indices['inner_bond_index'] = ['element_indices']

topological_attributes.append('inner_bond_index')

# n_atoms

attributes.append('n_atoms')
attribute_synonyms['n_atom'] = 'n_atoms'

required_indices['n_atoms'] = ['element_indices']

# n_groups

attributes.append('n_groups')
attribute_synonyms['n_group'] = 'n_groups'
attribute_synonyms['n_residues'] = 'n_groups'
attribute_synonyms['n_residue'] = 'n_groups'

required_indices['n_groups'] = ['element_indices']

topological_attributes.append('n_groups')

# n_components

attributes.append('n_components')
attribute_synonyms['n_component'] = 'n_components'

required_indices['n_components'] = ['element_indices']

topological_attributes.append('n_components')

# n_chains

attributes.append('n_chains')
attribute_synonyms['n_chain'] = 'n_chains'

required_indices['n_chains'] = ['element_indices']

topological_attributes.append('n_chains')

# n_molecules

attributes.append('n_molecules')
attribute_synonyms['n_molecule'] = 'n_molecules'

required_indices['n_molecules'] = ['element_indices']

topological_attributes.append('n_molecules')

# n_entities

attributes.append('n_entities')
attribute_synonyms['n_entity'] = 'n_entities'

required_indices['n_entities'] = ['element_indices']

topological_attributes.append('n_entities')

# n_bonds

attributes.append('n_bonds')
attribute_synonyms['n_bond'] = 'n_bonds'

required_indices['n_bonds'] = ['element_indices']

topological_attributes.append('n_bonds')

# n_inner_bonds

attributes.append('n_inner_bonds')
attribute_synonyms['n_inner_bond'] = 'n_inner_bonds'

required_indices['n_inner_bonds'] = ['element_indices']

topological_attributes.append('n_inner_bonds')

# n_aminoacids

attributes.append('n_aminoacids')
attribute_synonyms['n_aminoacid'] = 'n_aminoacids'

required_indices['n_aminoacids'] = ['element_indices']

topological_attributes.append('n_aminoacids')

# n_nucleotides

attributes.append('n_nucleotides')
attribute_synonyms['n_nucleotide'] = 'n_nucleotides'

required_indices['n_nucleotides'] = ['element_indices']

topological_attributes.append('n_nucleotides')

# n_ions

attributes.append('n_ions')
attribute_synonyms['n_ion'] = 'n_ions'

required_indices['n_ions'] = ['element_indices']

topological_attributes.append('n_ions')

# n_waters

attributes.append('n_waters')
attribute_synonyms['n_water'] = 'n_waters'

required_indices['n_waters'] = ['element_indices']

topological_attributes.append('n_waters')

# n_small_molecules

attributes.append('n_small_molecules')
attribute_synonyms['n_small_molecule'] = 'n_small_molecules'

required_indices['n_small_molecules'] = ['element_indices']

topological_attributes.append('n_small_molecules')

# n_peptides

attributes.append('n_peptides')
attribute_synonyms['n_peptide'] = 'n_peptides'

required_indices['n_peptides'] = ['element_indices']

topological_attributes.append('n_peptides')

# n_proteins

attributes.append('n_proteins')
attribute_synonyms['n_protein'] = 'n_proteins'

required_indices['n_proteins'] = ['element_indices']

topological_attributes.append('n_proteins')

# n_dnas

attributes.append('n_dnas')
attribute_synonyms['n_dna'] = 'n_dnas'

required_indices['n_dnas'] = ['element_indices']

topological_attributes.append('n_dnas')

# n_rnas

attributes.append('n_rnas')
attribute_synonyms['n_rna'] = 'n_rnas'

required_indices['n_rnas'] = ['element_indices']

topological_attributes.append('n_rnas')

# n_lipids

attributes.append('n_lipids')
attribute_synonyms['n_lipid'] = 'n_lipids'

required_indices['n_lipids'] = ['element_indices']

topological_attributes.append('n_lipids')

# n_oligosaccharides

attributes.append('n_oligosaccharides')
attribute_synonyms['n_oligosaccharides'] = 'n_oligosaccharides'

required_indices['n_oligosaccharides'] = ['element_indices']

topological_attributes.append('n_oligosaccharides')

# n_saccharides

attributes.append('n_saccharides')
attribute_synonyms['n_saccharides'] = 'n_saccharides'

required_indices['n_saccharides'] = ['element_indices']

topological_attributes.append('n_saccharides')

# formal_charge

attributes.append('formal_charge')
attribute_synonyms['formal_charges'] = 'formal_charge'

required_indices['formal_charge'] = ['element_indices']

topological_attributes.append('formal_charge')

# partial_charge

attributes.append('partial_charge')
attribute_synonyms['partial_charges'] = 'partial_charge'

required_indices['partial_charge'] = ['element_indices']

topological_attributes.append('partial_charge')


###
### STRUCTURAL ATTRIBUTES
###

# structure_id

attributes.append('structure_id')
attribute_synonyms['structure_ids'] = 'structure_id'
attribute_synonyms['structures_ids'] = 'structure_id'
attribute_synonyms['structures_id'] = 'structure_id'
attribute_synonyms['md_step'] = 'structure_id'
attribute_synonyms['md_steps'] = 'structure_id'
attribute_synonyms['mdstep'] = 'structure_id'
attribute_synonyms['mdsteps'] = 'structure_id'

required_indices['structure_id'] = ['structure_indices']

structural_attributes.append('structure_id')

# time

attributes.append('time')
attribute_synonyms['times'] = 'time'

required_indices['time'] = ['structure_indices']

structural_attributes.append('time')

# box

attributes.append('box')
attribute_synonyms['boxes'] = 'box'

required_indices['box'] = ['structure_indices']

structural_attributes.append('box')

# box_shape

attributes.append('box_shape')
attribute_synonyms['box_shapes'] = 'box_shape'

required_indices['box_shape'] = ['structure_indices']

structural_attributes.append('box_shape')

# box_angles

attributes.append('box_angles')
attribute_synonyms['box_angle'] = 'box_angles'

required_indices['box_angles'] = ['structure_indices']

structural_attributes.append('box_angles')

# box_lengths

attributes.append('box_lengths')
attribute_synonyms['box_length'] = 'box_length'

required_indices['box_lengths'] = ['structure_indices']

structural_attributes.append('box_lengths')

# box_volume

attributes.append('box_volume')
attribute_synonyms['box_volumes'] = 'box_volume'

required_indices['box_volume'] = ['structure_indices']

structural_attributes.append('box_volume')

# coordinates

attributes.append('coordinates')
attribute_synonyms['coordinate'] = 'coordinates'
attribute_synonyms['positions'] = 'coordinates'
attribute_synonyms['position'] = 'coordinates'

required_indices['coordinates'] = ['element_indices', 'structure_indices']

structural_attributes.append('coordinates')

# n_structures

attributes.append('n_structures')
attribute_synonyms['n_structure'] = 'n_structures'

required_indices['n_structures'] = []

structural_attributes.append('box_volume')

# bioassemblies
# This is not an attribute. It has to be removed in the future.

attributes.append('bioassemblies')
attribute_synonyms['biological_assembly'] = 'bioassemblies'
attribute_synonyms['biological_assemblies'] = 'bioassemblies'
attribute_synonyms['bioassembly'] = 'bioassemblies'

required_indices['bioassemblies'] = []

# n_bioassemblies
# This is not an attribute. It has to be removed in the future.

attributes.append('n_bioassemblies')
attribute_synonyms['n_bioassembly'] = 'n_bioassemblies'
attribute_synonyms['n_biological_assemblies'] = 'n_bioassemblies'
attribute_synonyms['n_biological_assembly'] = 'n_bioassemblies'

required_indices['n_bioassemblies'] = []

# occupancy

attributes.append('occupancy')
attribute_synonyms['occupancies'] = 'occupancy'

required_indices['occupancy'] = ['element_indices']

# alternate_location

attributes.append('alternate_location')
attribute_synonyms['alternate_locations'] = 'alternate_location'

required_indices['alternate_location'] = ['element_indices']


# b_factor

attributes.append('b_factor')
attribute_synonyms['b_factors'] = 'b_factor'

required_indices['b_factor'] = ['element_indices']

# temperature

attributes.append('temperature')
attribute_synonyms['temperatures'] = 'temperature'

required_indices['temperature'] = []

structural_attributes.append('temperature')

###
### MECHANICAL ATTRIBUTES
###

#  forcefield

attributes.append('forcefield')
attribute_synonyms['force field'] = 'forcefield'
attribute_synonyms['force_field'] = 'forcefield'
attribute_synonyms['forcefields'] = 'forcefield'
attribute_synonyms['force fields'] = 'forcefield'
attribute_synonyms['force_fields'] = 'forcefield'

required_indices['forcefield'] = []

mechanical_attributes.append('forcefield')

# non_bonded_method

attributes.append('non_bonded_method')
attribute_synonyms['non bonded method'] = 'non_bonded_method'

required_indices['non_bonded_method'] = []

mechanical_attributes.append('non_bonded_method')

# non_bonded_method

attributes.append('non_bonded_method')
attribute_synonyms['non bonded method'] = 'non_bonded_method'

required_indices['non_bonded_method'] = []

mechanical_attributes.append('non_bonded_method')

# cutoff_distance

attributes.append('cutoff_distance')
attribute_synonyms['cutoff distance'] = 'cutoff_distance'

required_indices['cutoff_distance'] = []

mechanical_attributes.append('cutoff_distance')

# switch_distance

attributes.append('switch_distance')
attribute_synonyms['switch distance'] = 'switch_distance'

required_indices['switch_distance'] = []

mechanical_attributes.append('switch_distance')

# dispersion_correction

attributes.append('dispersion_correction')
attribute_synonyms['dispersion correction'] = 'dispersion_correction'
attribute_synonyms['use_dispersion_correction'] = 'dispersion_correction'

required_indices['dispersion_correction'] = []

mechanical_attributes.append('dispersion_correction')

# ewald_error_tolerance

attributes.append('ewald_error_tolerance')
attribute_synonyms['ewald error tolerance'] = 'ewald_error_tolerance'

required_indices['ewald_error_tolerance'] = []

mechanical_attributes.append('ewald_error_tolerance')

# hydrogen_mass

attributes.append('hydrogen_mass')
attribute_synonyms['hydrogen mass'] = 'hydrogen_mass'

required_indices['hydrogen_mass'] = []

mechanical_attributes.append('hydrogen_mass')

# constraints

attributes.append('constraints')
attribute_synonyms['constraint'] = 'constraints'

required_indices['constraints'] = []

mechanical_attributes.append('constraints')

# flexible_constraints

attributes.append('flexible_constraints')
attribute_synonyms['flexible constraint'] = 'flexible_constraints'

required_indices['flexible_constraints'] = []

mechanical_attributes.append('flexible_constraints')

# water_model

attributes.append('water_model')
attribute_synonyms['water model'] = 'water_model'

required_indices['water_model'] = []

mechanical_attributes.append('water_model')

# rigid_water

attributes.append('rigid_water')
attribute_synonyms['rigid water'] = 'rigid_water'

required_indices['rigid_water'] = []

mechanical_attributes.append('rigid_water')

# implicit_solvent

attributes.append('implicit_solvent')
attribute_synonyms['implicit solvent'] = 'implicit_solvent'

required_indices['implicit_solvent'] = []

mechanical_attributes.append('implicit_solvent')

# solute_dielectric

attributes.append('solute_dielectric')
attribute_synonyms['solute dielectric'] = 'solute_dielectric'

required_indices['solute_dielectric'] = []

mechanical_attributes.append('solute_dielectric')

# solvent_dielectric

attributes.append('solvent_dielectric')
attribute_synonyms['solvent dielectric'] = 'solvent_dielectric'

required_indices['solvent_dielectric'] = []

mechanical_attributes.append('solvent_dielectric')

# salt_concentration

attributes.append('salt_concentration')
attribute_synonyms['salt concentration'] = 'salt_concentration'

required_indices['salt_concentration'] = []

mechanical_attributes.append('salt_concentration')

# kappa

attributes.append('kappa')
attribute_synonyms['debye_length'] = 'kappa'

required_indices['kappa'] = []

mechanical_attributes.append('kappa')





















