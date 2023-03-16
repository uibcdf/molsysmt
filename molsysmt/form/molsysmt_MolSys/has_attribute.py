from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def has_attribute(molecular_system, attribute):

    from . import attributes

    output = attributes[attribute]

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

    elif attribute in ['bond_index', 'bond_id', 'bond_name', 'bond_type',
            'bond_order', 'bond_atoms']:
        if molecular_system.topology.bonds_dataframe.shape[0]:
            output = True 

    ###
    ### STRUCTURAL ATTRIBUTES
    ###

    elif attribute=='structure_index':
        if molecular_system.structures.structure_id is None:
            output = False

    elif attribute=='structure_id':
        if molecular_system.structures.structure_id is None:
            output = False

    elif attribute=='coordinates':
        if molecular_system.structures.coordinates is None:
            output = False

    elif attribute=='velocities':
        if molecular_system.structures.velocities is None:
            output = False

    elif attribute=='time':
        if molecular_system.structures.time is None:
            output = False

    elif attribute in ['box', 'box_shape', 'box_angles', 'box_lengths', 'box_volume']:
        if molecular_system.structures.box is None:
            output = False

    elif attribute=='occupancy':
        if molecular_system.structures.occupancy is None:
            output = False

    elif attribute=='alternate_location':
        if molecular_system.structures.alternate_location is None:
            output = False

    elif attribute=='b_factor':
        if molecular_system.structures.b_factor is None:
            output = False


    ###
    ### MECHANICAL ATTRIBUTES
    ###

    elif attribute=='formal_charge':
        if molecular_system.molecular_mechanics.formal_charge is None:
            output = False

    elif attribute=='partial_charge':
        if molecular_system.molecular_mechanics.partial_charge is None:
            output = False

    elif attribute=='forcefield':
        if molecular_system.molecular_mechanics.forcefield is None:
            output = False

    elif attribute=='non_bonded_method':
        if molecular_system.molecular_mechanics.non_bonded_method is None:
            output = False

    elif attribute=='cutoff_distance':
        if molecular_system.molecular_mechanics.cutoff_distance is None:
            output = False

    elif attribute=='switch_distance':
        if molecular_system.molecular_mechanics.switch_distance is None:
            output = False

    elif attribute=='dispersion_correction':
        if molecular_system.molecular_mechanics.dispersion_correction is None:
            output = False

    elif attribute=='ewald_error_tolerance':
        if molecular_system.molecular_mechanics.ewald_error_tolerance is None:
            output = False

    elif attribute=='hydrogen_mass':
        if molecular_system.molecular_mechanics.hydrogen_mass is None:
            output = False

    elif attribute=='constraints':
        if molecular_system.molecular_mechanics.constraints is None:
            output = False

    elif attribute=='flexible_constraints':
        if molecular_system.molecular_mechanics.flexible_constraints is None:
            output = False

    elif attribute=='water_model':
        if molecular_system.molecular_mechanics.water_model is None:
            output = False

    elif attribute=='rigid_water':
        if molecular_system.molecular_mechanics.rigid_water is None:
            output = False

    elif attribute=='implicit_solvent':
        if molecular_system.molecular_mechanics.implicit_solvent is None:
            output = False

    elif attribute=='solute_dielectric':
        if molecular_system.molecular_mechanics.solute_dielectric is None:
            output = False

    elif attribute=='solvent_dielectric':
        if molecular_system.molecular_mechanics.solvent_dielectric is None:
            output = False

    elif attribute=='salt_concentration':
        if molecular_system.molecular_mechanics.salt_concentration is None:
            output = False

    elif attribute=='kappa':
        if molecular_system.molecular_mechanics.kappa is None:
            output = False

    return output

