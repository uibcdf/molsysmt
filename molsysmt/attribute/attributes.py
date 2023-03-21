attributes = {}
attribute_synonyms = {}
independent_attributes = []

def add_attribute(name, synonyms=[], depends_on=[], dependants=[], runs_on_elements=False, runs_on_structures=False,
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

    if len(depends_on)==0:
        independent_attributes.append(name)

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
add_attribute('group_index', synonyms=['group_indices', 'residue_indices', 'residue_index'], dependants=['n_groups'], runs_on_elements=True, topological=True,
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
add_attribute('component_index', synonyms=['component_indices'], dependants=['n_components'], runs_on_elements=True, topological=True,
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
add_attribute('chain_index', synonyms=['chain_indices'], dependants=['n_chains'], runs_on_elements=True, topological=True,
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
add_attribute('molecule_index', synonyms=['molecule_indices'], dependants=['n_molecules'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'])

## molecule_name
add_attribute('molecule_name', synonyms=['molecule_names'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'], set_to='molecule')

## molecule_id
add_attribute('molecule_id', synonyms=['molecule_ids'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'], set_to='molecule')

## molecule_type
add_attribute('molecule_type', synonyms=['molecule_types'],
        dependants=['n_ions', 'n_waters', 'n_small_molecules', 'n_lipids', 'n_peptides',
            'n_proteins', 'n_dnas', 'n_rnas', 'n_oligosaccharides', 'n_saccharides'],
        runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'], set_to='molecule')

## entity_index
add_attribute('entity_index', synonyms=['entity_indices'], dependants=['n_entities'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'])

## entity_name
add_attribute('entity_name', synonyms=['entity_names'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'], set_to='entity')

## entity_id
add_attribute('entity_id', synonyms=['entity_ids'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'], set_to='entity')

## entity_type
add_attribute('entity_type', synonyms=['entity_types'], runs_on_elements=True, topological=True,
        get_from=['atom','group','component','molecule','chain','entity'], set_to='entity')

## bond_index
add_attribute('bond_index', synonyms=['bond_indices'], dependants=['n_bonds'], runs_on_elements=True, topological=True,
        get_from=['atom','bond'])

## bond_id
add_attribute('bond_id', synonyms=['bond_ids'], runs_on_elements=True, topological=True,
        get_from=['bond'], set_to='bond')

## bond_type
add_attribute('bond_type', synonyms=['bond_types'], runs_on_elements=True, topological=True,
        get_from=['bond'], set_to='bond')

## bond_order
add_attribute('bond_order', synonyms=['bonds_order'], runs_on_elements=True, topological=True,
        get_from=['bond'], set_to='bond')

## bonded_atoms
add_attribute('bonded_atoms', synonyms=['bonded_atom'], dependants=['inner_bonded_atoms'], runs_on_elements=True, topological=True,
        get_from=['atom','bond'], set_to='bond')

## inner_bonded_atoms
add_attribute('inner_bonded_atoms', synonyms=['inner_bonded_atom'], depends_on=['bonded_atoms'], runs_on_elements=True, topological=True,
        get_from=['atom'])

## inner_bond_index
add_attribute('inner_bond_index', synonyms=['inner_bond_indices'], depends_on=['bonded_atoms'], runs_on_elements=True, topological=True,
        get_from=['atom'])

## n_atoms
add_attribute('n_atoms', synonyms=['n_atom'], depends_on=['atom_index'], runs_on_elements=True, topological=True,
        get_from=['atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'])

## n_groups
add_attribute('n_groups', synonyms=['n_group'], depends_on=['group_index'], runs_on_elements=True, topological=True,
        get_from=['atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'])

## n_components
add_attribute('n_components', synonyms=['n_component'], depends_on=['component_index'], runs_on_elements=True, topological=True,
        get_from=['atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'])

## n_chains
add_attribute('n_chains', synonyms=['n_chain'], depends_on=['chain_index'], runs_on_elements=True, topological=True,
        get_from=['atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'])

## n_molecules
add_attribute('n_molecules', synonyms=['n_molecule'], depends_on=['molecule_index'], runs_on_elements=True, topological=True,
        get_from=['atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'])

## n_entities
add_attribute('n_entities', synonyms=['n_entity'], depends_on=['entity_index'], runs_on_elements=True, topological=True,
        get_from=['atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'])

## n_bonds
add_attribute('n_bonds', synonyms=['n_bond'], depends_on=['bond_index'], runs_on_elements=True, topological=True,
        get_from=['system'])

## n_inner_bonds
add_attribute('n_inner_bonds', synonyms=['n_inner_bond'], depends_on=['bonded_atoms'], runs_on_elements=True, topological=True,
        get_from=['atom'])

## n_aminoacids
add_attribute('n_aminoacids', synonyms=['n_aminoacid'], depends_on=['group_type'], runs_on_elements=True, topological=True,
        get_from=['system'])

## n_nucleotides
add_attribute('n_nucleotides', synonyms=['n_nucleotide'], depends_on=['group_type'], runs_on_elements=True, topological=True,
        get_from=['system'])

## n_ions
add_attribute('n_ions', synonyms=['n_ion'], depends_on=['molecule_type'], runs_on_elements=True, topological=True,
        get_from=['system'])

## n_waters
add_attribute('n_waters', synonyms=['n_water'], depends_on=['molecule_type'], runs_on_elements=True, topological=True,
        get_from=['system'])

## n_small_molecules
add_attribute('n_small_molecules', synonyms=['n_small_molecule'], depends_on=['molecule_type'], runs_on_elements=True, topological=True,
        get_from=['system'])

## n_peptides
add_attribute('n_peptides', synonyms=['n_peptide'], depends_on=['molecule_type'], runs_on_elements=True, topological=True,
        get_from=['system'])

## n_proteins
add_attribute('n_proteins', synonyms=['n_protein'], depends_on=['molecule_type'], runs_on_elements=True, topological=True,
        get_from=['system'])

## n_dnas
add_attribute('n_dnas', synonyms=['n_dna'], depends_on=['molecule_type'], runs_on_elements=True, topological=True,
        get_from=['system'])

## n_rnas
add_attribute('n_rnas', synonyms=['n_rna'], depends_on=['molecule_type'], runs_on_elements=True, topological=True,
        get_from=['system'])

## n_lipids
add_attribute('n_lipids', synonyms=['n_lipid'], depends_on=['molecule_type'], runs_on_elements=True, topological=True,
        get_from=['system'])

## n_oligosaccharides
add_attribute('n_oligosaccharides', synonyms=['n_oligosaccharide'], depends_on=['molecule_type'], runs_on_elements=True, topological=True,
        get_from=['system'])

## n_saccharides
add_attribute('n_saccharides', synonyms=['n_saccharide'], depends_on=['molecule_type'], runs_on_elements=True, topological=True,
        get_from=['system'])


###
### STRUCTURAL ATTRIBUTES
###

## structure_index
add_attribute('structure_index', synonyms=['runs_on_structures'], dependants='n_structures', runs_on_structures=True, structural=True)

## structure_id
add_attribute('structure_id', synonyms=['structure_ids', 'structures_id', 'structures_ids', 'md_step', 'md_steps', 'mdstep', 'mdsteps'], runs_on_structures=True, structural=True,
        get_from=['system'], set_to='system')

## time
add_attribute('time', synonyms=['times'], runs_on_structures=True, structural=True,
        get_from=['system'], set_to='system')

## box
add_attribute('box', synonyms=['boxes'],
        dependants=['box_shape', 'box_angles', 'box_lengths', 'box_volume'],
        runs_on_structures=True, structural=True,
        get_from=['system'], set_to='system')

## box_shape
add_attribute('box_shape', synonyms=['box_shapes'], depends_on=['box'], runs_on_structures=True, structural=True,
        get_from=['system'])

## box_angles
add_attribute('box_angles', synonyms=['box_angle'], depends_on=['box'], runs_on_structures=True, structural=True,
        get_from=['system'])

## box_lengths
add_attribute('box_lengths', synonyms=['box_length'], depends_on=['box'], runs_on_structures=True, structural=True,
        get_from=['system'])

## box_volume
add_attribute('box_volume', synonyms=['box_volumes'], depends_on=['box'], runs_on_structures=True, structural=True,
        get_from=['system'])

## coordinates
add_attribute('coordinates', synonyms=['coordinate', 'positions', 'position'], runs_on_elements=True, runs_on_structures=True, structural=True,
        get_from=['atom', 'system'], set_to='atom')

## velocities
add_attribute('velocities', synonyms=['velocity'], runs_on_elements=True, runs_on_structures=True, structural=True,
        get_from=['atom', 'system'], set_to='atom')

## n_structures
add_attribute('n_structures', synonyms=['n_structure'], depends_on=['structure_index'], runs_on_elements=True, runs_on_structures=True, structural=True,
        get_from=['system'])

## occupancy
add_attribute('occupancy', synonyms=['occupancies'], runs_on_elements=True, runs_on_structures=True, structural=True,
        get_from=['atom','system'], set_to='atom')

## alternate_location
add_attribute('alternate_location', synonyms=['alternate_locations'], runs_on_elements=True, runs_on_structures=True, structural=True,
        get_from=['atom','system'], set_to='atom')

## b_factor
add_attribute('b_factor', synonyms=['b_factors'], runs_on_elements=True, runs_on_structures=True, structural=True,
        get_from=['atom','system'], set_to='atom')

## temperature
add_attribute('temperature', synonyms=['temperatures'], runs_on_structures=True, structural=True,
        get_from=['system'], set_to='system')


###
### MECHANICAL ATTRIBUTES
###

## formal_charge
add_attribute('formal_charge', synonyms=['formal_charges'], runs_on_elements=True, mechanical=True,
        get_from=['atom','system'], set_to='atom')

## partial_charge
add_attribute('partial_charge', synonyms=['partial_charges'], runs_on_elements=True, mechanical=True,
        get_from=['atom','system'], set_to='atom')

## forcefield
add_attribute('forcefield', synonyms=['force field', 'forcefields', 'force_field', 'force_fields'], mechanical=True,
        get_from=['system'], set_to='system')

## non_bonded_method
add_attribute('non_bonded_method', synonyms=['non bonded method'], mechanical=True,
        get_from=['system'], set_to='system')

## cutoff_distance
add_attribute('cutoff_distance', synonyms=['cutoff distance'], mechanical=True,
        get_from=['system'], set_to='system')

## switch_distance
add_attribute('switch_distance', synonyms=['switch distance'], mechanical=True,
        get_from=['system'], set_to='system')

## dispersion_correction
add_attribute('dispersion_correction', synonyms=['dispersion correction', 'use_dispersion_correction'], mechanical=True,
        get_from=['system'], set_to='system')

## ewald_error_tolerance
add_attribute('ewald_error_tolerance', synonyms=['ewald error tolerance'], mechanical=True,
        get_from=['system'], set_to='system')

## hydrogen_mass
add_attribute('hydrogen_mass', synonyms=['hydrogen mass'], mechanical=True,
        get_from=['system'], set_to='system')

## constraints
add_attribute('constraints', synonyms=['constraints'], mechanical=True,
        get_from=['system'], set_to='system')

## flexible_constraints
add_attribute('flexible_constraints', synonyms=['flexible constraints', 'flexible constraint', 'flexible_constraint'], mechanical=True,
        get_from=['system'], set_to='system')

## water_model
add_attribute('water_model', synonyms=['water model'], mechanical=True,
        get_from=['system'], set_to='system')

## rigid_water
add_attribute('rigid_water', synonyms=['rigid water'], mechanical=True,
        get_from=['system'], set_to='system')

## implicit_solvent
add_attribute('implicit_solvent', synonyms=['implicit solvent'], mechanical=True,
        get_from=['system'], set_to='system')

## solute_dielectric
add_attribute('solute_dielectric', synonyms=['solute dielectric'], mechanical=True,
        get_from=['system'], set_to='system')

## solvent_dielectric
add_attribute('solvent_dielectric', synonyms=['solvent dielectric'], mechanical=True,
        get_from=['system'], set_to='system')

## salt_concentration
add_attribute('salt_concentration', synonyms=['salt concentration'], mechanical=True,
        get_from=['system'], set_to='system')

## kappa
add_attribute('kappa', synonyms=['debye_length', 'debye length'], mechanical=True,
        get_from=['system'], set_to='system')

