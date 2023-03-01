from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def has_attribute(molecular_system, **kwargs):

    arguments = []
    for key in kwargs.keys():
        if kwargs[key]:
            arguments.append(key)

    outputs = []

    for argument in arguments:

        output = False

        ###
        ### TOPOLOGICAL
        ###

        if argument in ['atom_index', 'atom_id', 'atom_name', 'atom_type',
                'group_index', 'group_id', 'group_name', 'group_type',
                'component_index', 'component_id', 'component_name', 'component_type',
                'molecule_index', 'molecule_id', 'molecule_name', 'molecule_type',
                'chain_index', 'chain_id', 'chain_name', 'chain_type',
                'entity_index', 'entity_id', 'entity_name', 'entity_type',
                'n_atoms', 'n_groups', 'n_components', 'n_chains', 'n_molecules',
                'n_entities', 'n_aminoacids', 'n_nucleotides', 'n_ions', 'n_waters',
                'n_waters', 'n_small_molecules', 'n_peptides', 'n_proteins', 'n_dnas', 'n_rnas',
                'n_lipids', 'n_oligosaccharides', 'n_saccharides']:
            if molecular_system.topology.atoms_data_frame.shape[0]:
                output = True 

        if argument in ['bond_index', 'bond_id', 'bond_name', 'bond_type',
                'bond_order', 'bond_atoms']:
            if molecular_system.topology.atoms_data_frame.shape[0]:
                output = True 




from molsysmt.attribute.attributes import attributes as _all_attributes

attributes = {ii:False for ii in _all_attributes}

attributes['bond_index'] = True
attributes['bond_id'] = True
attributes['bond_name'] = True
attributes['bond_type'] = True
attributes['bond_order'] = True
attributes['bonded_atoms'] = True

###
### STRUCTURAL ATTRIBUTES
###

attributes['structure_index'] = True
attributes['structure_id'] = True
attributes['time'] = True
attributes['box'] = True
attributes['coordinates'] = True
attributes['occupancy'] = True
attributes['alternate_location'] = True
attributes['b_factor'] = True

###
### MECHANICAL ATTRIBUTES
###


attributes['formal_charge'] = True
attributes['partial_charge'] = True
attributes['forcefield'] = True
attributes['non_bonded_method'] = True
attributes['cutoff_distance'] = True
attributes['switch_distance'] = True
attributes['dispersion_correction'] = True
attributes['ewald_error_tolerance'] = True
attributes['hydrogen_mass'] = True
attributes['constraints'] = True
attributes['flexible_constraints'] = True
attributes['water_model'] = True
attributes['rigid_water'] = True
attributes['implicit_solvent'] = True
attributes['solute_dielectric'] = True
attributes['solvent_dielectric'] = True
attributes['salt_concentration'] = True
attributes['kappa'] = True

del(_all_attributes)
