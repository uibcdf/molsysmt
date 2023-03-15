attributes = {}
attribute_synonyms = {}

def add_attribute(name, synonyms=[], depends_of=None, dependants=[], runs_on_elements=False, runs_on_structures=False,
        topological=False, structural=False, mechanical=False, get_from=[], set_to=None):

    attributes[name] = {
            'synonyms' : synonyms,
            'runs_on_elements' :  runs_on_elements,
            'runs_on_structures' :  runs_on_structures,
            'topological' :  topological,
            'structural' :  structural,
            'mechanical' :  mechanical,
            'get_from' : get_from,
            'set_to' : set_to
            }

    for alternative_name in synonyms:
        attribute_synonyms[alternative_name]=name

###
### TOPOLOGICAL ATTRIBUTES
###

### atom_index
add_attribute('atom_index', synonyms=['atom_indices'], dependants=['n_atoms'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'])

### atom_name
add_attribute('atom_name', synonyms=['atom_names'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'], set_to='atom')

## atom_id
add_attribute('atom_id', synonyms=['atom_ids'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'], set_to='atom')

## atom_type
add_attribute('atom_type', synonyms=['atom_types'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'], set_to='atom')

## group_index
add_attribute('group_index', synonyms=['group_indices', 'residue_indices', 'residue_index'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'])

## group_name
add_attribute('group_name', synonyms=['group_names', 'residue_names', 'residue_name'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'], set_to='group')

## group_id
add_attribute('group_id', synonyms=['group_ids', 'residue_ids', 'residue_id'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'], set_to='group')

## group_type
add_attribute('group_type', synonyms=['group_types', 'residue_types', 'residue_type'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'], set_to='group')

## component_index
add_attribute('component_index', synonyms=['component_indices'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'])

## component_name
add_attribute('component_name', synonyms=['component_names'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'], set_to='component')

## component_id
add_attribute('component_id', synonyms=['component_ids'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'], set_to='component')

## component_type
add_attribute('component_type', synonyms=['component_types'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'], set_to='component')

## chain_index
add_attribute('chain_index', synonyms=['chain_indices'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'])

## chain_name
add_attribute('chain_name', synonyms=['chain_names'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'], set_to='chain')

## chain_id
add_attribute('chain_id', synonyms=['chain_ids'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'], set_to='chain')

## chain_type
add_attribute('chain_type', synonyms=['chain_types'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'], set_to='chain')

## molecule_index
add_attribute('molecule_index', synonyms=['molecule_indices'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'])

## molecule_name
add_attribute('molecule_name', synonyms=['molecule_names'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'], set_to='molecule')

## molecule_id
add_attribute('molecule_id', synonyms=['molecule_ids'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'], set_to='molecule')

## molecule_type
add_attribute('molecule_type', synonyms=['molecule_types'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'], set_to='molecule')

## entity_index
add_attribute('entity_index', synonyms=['entity_indices'], runs_on_elements=True, topological=True)
add_attribute('entity_name', synonyms=['entity_names'], runs_on_elements=True, topological=True)
add_attribute('entity_id', synonyms=['entity_ids'], runs_on_elements=True, topological=True)
add_attribute('entity_type', synonyms=['entity_types'], runs_on_elements=True, topological=True)
add_attribute('bond_index', synonyms=['bond_indices'], runs_on_elements=True, topological=True)
add_attribute('bond_id', synonyms=['bond_ids'], runs_on_elements=True, topological=True)
add_attribute('bond_type', synonyms=['bond_types'], runs_on_elements=True, topological=True)
add_attribute('bond_order', synonyms=['bonds_order'], runs_on_elements=True, topological=True)
add_attribute('bonded_atoms', synonyms=['bonded_atom'], runs_on_elements=True, topological=True)
add_attribute('inner_bonded_atoms', synonyms=['inner_bonded_atom'], runs_on_elements=True, topological=True)
add_attribute('inner_bond_index', synonyms=['inner_bond_indices'], runs_on_elements=True, topological=True)
add_attribute('n_atoms', synonyms=['n_atom'], runs_on_elements=True, topological=True)
add_attribute('n_groups', synonyms=['n_group'], runs_on_elements=True, topological=True)
add_attribute('n_components', synonyms=['n_component'], runs_on_elements=True, topological=True)
add_attribute('n_chains', synonyms=['n_chain'], runs_on_elements=True, topological=True)
add_attribute('n_molecules', synonyms=['n_molecule'], runs_on_elements=True, topological=True)
add_attribute('n_entities', synonyms=['n_entity'], runs_on_elements=True, topological=True)
add_attribute('n_bonds', synonyms=['n_bond'], runs_on_elements=True, topological=True)
add_attribute('n_inner_bonds', synonyms=['n_inner_bond'], runs_on_elements=True, topological=True)
add_attribute('n_aminoacids', synonyms=['n_aminoacid'], runs_on_elements=True, topological=True)
add_attribute('n_nucleotides', synonyms=['n_nucleotide'], runs_on_elements=True, topological=True)
add_attribute('n_ions', synonyms=['n_ion'], runs_on_elements=True, topological=True)
add_attribute('n_waters', synonyms=['n_water'], runs_on_elements=True, topological=True)
add_attribute('n_small_molecules', synonyms=['n_small_molecule'], runs_on_elements=True, topological=True)
add_attribute('n_peptides', synonyms=['n_peptide'], runs_on_elements=True, topological=True)
add_attribute('n_proteins', synonyms=['n_protein'], runs_on_elements=True, topological=True)
add_attribute('n_dnas', synonyms=['n_dna'], runs_on_elements=True, topological=True)
add_attribute('n_rnas', synonyms=['n_rna'], runs_on_elements=True, topological=True)
add_attribute('n_lipids', synonyms=['n_lipid'], runs_on_elements=True, topological=True)
add_attribute('n_oligosaccharides', synonyms=['n_oligosaccharide'], runs_on_elements=True, topological=True)
add_attribute('n_saccharides', synonyms=['n_saccharide'], runs_on_elements=True, topological=True)


###
### STRUCTURAL ATTRIBUTES
###

add_attribute('structure_index', synonyms=['runs_on_structures'], runs_on_structures=True, structural=True)
add_attribute('structure_id', synonyms=['structure_ids', 'structures_id', 'structures_ids', 'md_step', 'md_steps', 'mdstep', 'mdsteps'], runs_on_structures=True, structural=True)
add_attribute('time', synonyms=['times'], runs_on_structures=True, structural=True)
add_attribute('box', synonyms=['boxes'], runs_on_structures=True, structural=True)
add_attribute('box_shape', synonyms=['box_shapes'], runs_on_structures=True, structural=True)
add_attribute('box_angles', synonyms=['box_angle'], runs_on_structures=True, structural=True)
add_attribute('box_lengths', synonyms=['box_length'], runs_on_structures=True, structural=True)
add_attribute('box_volume', synonyms=['box_volumes'], runs_on_structures=True, structural=True)
add_attribute('coordinates', synonyms=['coordinate', 'positions', 'position'], runs_on_elements=True, runs_on_structures=True, structural=True)
add_attribute('velocities', synonyms=['velocity'], runs_on_elements=True, runs_on_structures=True, structural=True)
add_attribute('n_structures', synonyms=['n_structure'], runs_on_elements=True, runs_on_structures=True, structural=True)
add_attribute('occupancy', synonyms=['occupancies'], runs_on_elements=True, runs_on_structures=True, structural=True)
add_attribute('alternate_location', synonyms=['alternate_locations'], runs_on_elements=True, runs_on_structures=True, structural=True)
add_attribute('b_factor', synonyms=['b_factors'], runs_on_elements=True, runs_on_structures=True, structural=True)
add_attribute('temperature', synonyms=['temperatures'], runs_on_structures=True, structural=True)


###
### MECHANICAL ATTRIBUTES
###

add_attribute('formal_charge', synonyms=['formal_charges'], runs_on_elements=True, mechanical=True)
add_attribute('partial_charge', synonyms=['partial_charges'], runs_on_elements=True, mechanical=True)
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

