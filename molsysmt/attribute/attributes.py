attributes = []
attribute_synonyms = {}
required_indices = {}
topological_attributes = []
structural_attributes = []
mechanical_attributes = []


def add_attribute(name, synonyms=[], element_indices=False, structure_indices=False,
        topological=False, structural=False, mechanical=False):

    attributes.append(name)
    for alternative_name in synonyms:
        attribute_synonyms[alternative_name]=name
    required_indices[name]=[]
    if element_indices:
        required_indices[name].append('element_indices')
    if structure_indices:
        required_indices[name].append('structure_indices')
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
add_attribute('bond_order', synonyms=['bonds_order'], element_indices=True, topological=True)
add_attribute('bonded_atoms', synonyms=['bonded_atom'], element_indices=True, topological=True)
add_attribute('inner_bonded_atoms', synonyms=['inner_bonded_atom'], element_indices=True, topological=True)
add_attribute('inner_bond_index', synonyms=['inner_bond_indices'], element_indices=True, topological=True)
add_attribute('n_atoms', synonyms=['n_atom'], element_indices=True, topological=True)
add_attribute('n_groups', synonyms=['n_group'], element_indices=True, topological=True)
add_attribute('n_components', synonyms=['n_component'], element_indices=True, topological=True)
add_attribute('n_chains', synonyms=['n_chain'], element_indices=True, topological=True)
add_attribute('n_molecules', synonyms=['n_molecule'], element_indices=True, topological=True)
add_attribute('n_entities', synonyms=['n_entity'], element_indices=True, topological=True)
add_attribute('n_bonds', synonyms=['n_bond'], element_indices=True, topological=True)
add_attribute('n_inner_bonds', synonyms=['n_inner_bond'], element_indices=True, topological=True)
add_attribute('n_aminoacids', synonyms=['n_aminoacid'], element_indices=True, topological=True)
add_attribute('n_nucleotides', synonyms=['n_nucleotide'], element_indices=True, topological=True)
add_attribute('n_ions', synonyms=['n_ion'], element_indices=True, topological=True)
add_attribute('n_waters', synonyms=['n_water'], element_indices=True, topological=True)
add_attribute('n_small_molecules', synonyms=['n_small_molecule'], element_indices=True, topological=True)
add_attribute('n_peptides', synonyms=['n_peptide'], element_indices=True, topological=True)
add_attribute('n_proteins', synonyms=['n_protein'], element_indices=True, topological=True)
add_attribute('n_dnas', synonyms=['n_dna'], element_indices=True, topological=True)
add_attribute('n_rnas', synonyms=['n_rna'], element_indices=True, topological=True)
add_attribute('n_lipids', synonyms=['n_lipid'], element_indices=True, topological=True)
add_attribute('n_oligosaccharides', synonyms=['n_oligosaccharide'], element_indices=True, topological=True)
add_attribute('n_saccharides', synonyms=['n_saccharide'], element_indices=True, topological=True)


###
### STRUCTURAL ATTRIBUTES
###

add_attribute('structure_index', synonyms=['structure_indices'], structure_indices=True, structural=True)
add_attribute('structure_id', synonyms=['structure_ids', 'structures_id', 'structures_ids', 'md_step', 'md_steps', 'mdstep', 'mdsteps'], structure_indices=True, structural=True)
add_attribute('time', synonyms=['times'], structure_indices=True, structural=True)
add_attribute('box', synonyms=['boxes'], structure_indices=True, structural=True)
add_attribute('box_shape', synonyms=['box_shapes'], structure_indices=True, structural=True)
add_attribute('box_angles', synonyms=['box_angle'], structure_indices=True, structural=True)
add_attribute('box_lengths', synonyms=['box_length'], structure_indices=True, structural=True)
add_attribute('box_volume', synonyms=['box_volumes'], structure_indices=True, structural=True)
add_attribute('coordinates', synonyms=['coordinate', 'positions', 'position'], element_indices=True, structure_indices=True, structural=True)
add_attribute('n_structures', synonyms=['n_structure'], element_indices=True, structure_indices=True, structural=True)
add_attribute('occupancy', synonyms=['occupancies'], element_indices=True, structure_indices=True, structural=True)
add_attribute('alternate_location', synonyms=['alternate_locations'], element_indices=True, structure_indices=True, structural=True)
add_attribute('b_factor', synonyms=['b_factors'], element_indices=True, structure_indices=True, structural=True)
add_attribute('temperature', synonyms=['temperatures'], structure_indices=True, structural=True)


###
### MECHANICAL ATTRIBUTES
###

add_attribute('formal_charge', synonyms=['formal_charges'], element_indices=True, mechanical=True)
add_attribute('partial_charge', synonyms=['partial_charges'], element_indices=True, mechanical=True)
add_attribute('forcefield', synonyms=['force field', 'forcefields', 'force_field', 'force_fields'], mechanical=True)
add_attribute('non_bonded_method', synonyms=['non bonded method'], mechanical=True)
add_attribute('cutoff_distance', synonyms=['cutoff distance'], mechanical=True)
add_attribute('switch_distance', synonyms=['switch distance'], mechanical=True)
add_attribute('dispersion_correction', synonyms=['dispersion correction', 'use_dispersion_correction'], mechanical=True)
add_attribute('ewald_error_tolerance', synonyms=['ewald error tolerance'], mechanical=True)
add_attribute('hydrogen_mass', synonyms=['hydrogen mass'], mechanical=True)
add_attribute('constraints', synonyms=['constraints'], mechanical=True)
add_attribute('flexible_constraints', synonyms=['flexible constraints', 'flexible constraint', 'flexible_constraint'], mechanical=True)
add_attribute('water_model', synonyms=['water model'], mechanical=True)
add_attribute('rigid_water', synonyms=['rigid water'], mechanical=True)
add_attribute('implicit_solvent', synonyms=['implicit solvent'], mechanical=True)
add_attribute('solute_dielectric', synonyms=['solute dielectric'], mechanical=True)
add_attribute('solvent_dielectric', synonyms=['solvent dielectric'], mechanical=True)
add_attribute('salt_concentration', synonyms=['salt concentration'], mechanical=True)
add_attribute('kappa', synonyms=['debye_length', 'debye length'], mechanical=True)

