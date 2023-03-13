from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def has_attribute(molecular_system, attribute):

    output = False

    # Check attributes list first

    from . import attributes

    if not attributes[attribute]:
        return output

    ###
    ### TOPOLOGICAL
    ###

    if attribute in ['atom_index', 'atom_id', 'atom_name', 'atom_type',
            'group_index', 'group_id', 'group_name', 'group_type',
            'component_index', 'component_id', 'component_name', 'component_type',
            'molecule_index', 'molecule_id', 'molecule_name', 'molecule_type',
            'chain_index', 'chain_id', 'chain_name', 'chain_type',
            'entity_index', 'entity_id', 'entity_name', 'entity_type']:
        if molecular_system.topology.atoms_dataframe.shape[0]:
            output = True 

    elif attribute in ['n_atoms', 'n_groups', 'n_components', 'n_molecules', 'n_chains', 'n_entities',
            'n_ions', 'n_waters', 'n_small_molecules', 'n_peptides', 'n_proteins', 'n_dnas',
            'n_rnas', 'n_lipids', 'n_oligosaccharides']:
        output = True

    elif attribute in ['bond_index', 'bond_id', 'bond_name', 'bond_type',
            'bond_order', 'bond_atoms']:
        if molecular_system.topology.bonds_dataframe.shape[0]:
            output = True 
    elif attribute=='n_bonds':
        output = True 

    ###
    ### STRUCTURAL ATTRIBUTES
    ###

    elif attribute=='n_structures':
        output = True

    elif attribute in ['structure_index', 'structure_id', 'coordinates']:
        if molecular_system.structures.n_structures :
            output = True

    elif attribute=='time':
        if molecular_system.structures.time is not None:
            output = True

    elif attribute in ['box', 'box_shape', 'box_angles', 'box_lengths', 'box_volume']:
        if molecular_system.structures.box is not None:
            output = True

    elif attribute=='occupancy':
        if molecular_system.structures.occupancy is not None:
            output = True

    elif attribute=='alternate_location':
        if molecular_system.structures.alternate_location is not None:
            output = True

    elif attribute=='b_factor':
        if molecular_system.structures.b_factor is not None:
            output = True


    ###
    ### MECHANICAL ATTRIBUTES
    ###

    elif attribute=='formal_charge':
        if molecular_system.molecular_mechanics.formal_charge is not None:
            output = True

    elif attribute=='partial_charge':
        if molecular_system.molecular_mechanics.partial_charge is not None:
            output = True

    elif attribute=='forcefield':
        if molecular_system.molecular_mechanics.forcefield is not None:
            output = True

    elif attribute=='non_bonded_method':
        if molecular_system.molecular_mechanics.non_bonded_method is not None:
            output = True

    elif attribute=='cutoff_distance':
        if molecular_system.molecular_mechanics.cutoff_distance is not None:
            output = True

    elif attribute=='switch_distance':
        if molecular_system.molecular_mechanics.switch_distance is not None:
            output = True

    elif attribute=='dispersion_correction':
        if molecular_system.molecular_mechanics.dispersion_correction is not None:
            output = True

    elif attribute=='ewald_error_tolerance':
        if molecular_system.molecular_mechanics.ewald_error_tolerance is not None:
            output = True

    elif attribute=='hydrogen_mass':
        if molecular_system.molecular_mechanics.hydrogen_mass is not None:
            output = True

    elif attribute=='constraints':
        if molecular_system.molecular_mechanics.constraints is not None:
            output = True

    elif attribute=='flexible_constraints':
        if molecular_system.molecular_mechanics.flexible_constraints is not None:
            output = True

    elif attribute=='water_model':
        if molecular_system.molecular_mechanics.water_model is not None:
            output = True

    elif attribute=='rigid_water':
        if molecular_system.molecular_mechanics.rigid_water is not None:
            output = True

    elif attribute=='implicit_solvent':
        if molecular_system.molecular_mechanics.implicit_solvent is not None:
            output = True

    elif attribute=='solute_dielectric':
        if molecular_system.molecular_mechanics.solute_dielectric is not None:
            output = True

    elif attribute=='solvent_dielectric':
        if molecular_system.molecular_mechanics.solvent_dielectric is not None:
            output = True

    elif attribute=='salt_concentration':
        if molecular_system.molecular_mechanics.salt_concentration is not None:
            output = True

    elif attribute=='kappa':
        if molecular_system.molecular_mechanics.kappa is not None:
            output = True

    return output
