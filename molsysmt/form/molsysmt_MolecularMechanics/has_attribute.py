from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolecularMechanics')
def has_attribute(molecular_system, attribute):

    from . import attributes

    output = attributes[attribute]

    ###
    ### MECHANICAL ATTRIBUTES
    ###

    if attribute=='formal_charge':
        if molecular_system.formal_charge is None:
            output = False

    elif attribute=='partial_charge':
        if molecular_system.partial_charge is None:
            output = False

    elif attribute=='forcefield':
        if molecular_system.forcefield is None:
            output = False

    elif attribute=='non_bonded_method':
        if molecular_system.non_bonded_method is None:
            output = False

    elif attribute=='cutoff_distance':
        if molecular_system.cutoff_distance is None:
            output = False

    elif attribute=='switch_distance':
        if molecular_system.switch_distance is None:
            output = False

    elif attribute=='dispersion_correction':
        if molecular_system.dispersion_correction is None:
            output = False

    elif attribute=='ewald_error_tolerance':
        if molecular_system.ewald_error_tolerance is None:
            output = False

    elif attribute=='hydrogen_mass':
        if molecular_system.hydrogen_mass is None:
            output = False

    elif attribute=='constraints':
        if molecular_system.constraints is None:
            output = False

    elif attribute=='flexible_constraints':
        if molecular_system.flexible_constraints is None:
            output = False

    elif attribute=='water_model':
        if molecular_system.water_model is None:
            output = False

    elif attribute=='rigid_water':
        if molecular_system.rigid_water is None:
            output = False

    elif attribute=='implicit_solvent':
        if molecular_system.implicit_solvent is None:
            output = False

    elif attribute=='solute_dielectric':
        if molecular_system.solute_dielectric is None:
            output = False

    elif attribute=='solvent_dielectric':
        if molecular_system.solvent_dielectric is None:
            output = False

    elif attribute=='salt_concentration':
        if molecular_system.salt_concentration is None:
            output = False

    elif attribute=='kappa':
        if molecular_system.kappa is None:
            output = False

    return output

