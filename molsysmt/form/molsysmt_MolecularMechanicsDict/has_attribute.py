from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolecularMechanicsDict')
def has_attribute(molecular_system, attribute):

    from . import attributes

    output = attributes[attribute]

    ###
    ### MECHANICAL ATTRIBUTES
    ###

    if argument=='formal_charge':
        if 'formal_charge' in molecular_system:
            output = True

    elif argument=='partial_charge':
        if 'partial_charge' in molecular_system:
            output = True

    elif argument=='forcefield':
        if 'forcefield' in molecular_system:
            output = True

    elif argument=='non_bonded_method':
        if 'non_bonded_method' in molecular_system:
            output = True

    elif argument=='cutoff_distance':
        if 'cutoff_distance' in molecular_system:
            output = True

    elif argument=='switch_distance':
        if 'switch_distance' in molecular_system:
            output = True

    elif argument=='dispersion_correction':
        if 'dispersion_correction' in molecular_system:
            output = True

    elif argument=='ewald_error_tolerance':
        if 'ewald_error_tolerance' in molecular_system:
            output = True

    elif argument=='hydrogen_mass':
        if 'hydrogen_mass' in molecular_system:
            output = True

    elif argument=='constraints':
        if 'constraints' in molecular_system:
            output = True

    elif argument=='flexible_constraints':
        if 'flexible_constraints' in molecular_system:
            output = True

    elif argument=='water_model':
        if 'water_model' in molecular_system:
            output = True

    elif argument=='rigid_water':
        if 'rigid_water' in molecular_system:
            output = True

    elif argument=='implicit_solvent':
        if 'implicit_solvent' in molecular_system:
            output = True

    elif argument=='solute_dielectric':
        if 'solute_dielectric' in molecular_system:
            output = True

    elif argument=='solvent_dielectric':
        if 'solvent_dielectric' in molecular_system:
            output = True

    elif argument=='salt_concentration':
        if 'salt_concentration' in molecular_system:
            output = True

    elif argument=='kappa':
        if 'kappa' in molecular_system:
            output = True

    return output

