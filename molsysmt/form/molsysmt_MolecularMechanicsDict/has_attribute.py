from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolecularMechanicsDict')
def has_attribute(molecular_system, attribute, skip_digestion=False):

    from . import attributes

    output = attributes[attribute]

    ###
    ### MECHANICAL ATTRIBUTES
    ###

    if attribute=='n_atoms':
        output = False
        for attribute in ['formal_charge', 'partial_charge']:
            if attribute in molecular_system:
                if molecular_system[attribute] is not None:
                    output = True

    if attribute=='formal_charge':
        if 'formal_charge' not in molecular_system:
            output = False
        elif molecular_system['formal_charge'] is None:
            output = False

    elif attribute=='partial_charge':
        if 'partial_charge' not in molecular_system:
            output = False
        elif molecular_system['partial_charge'] is None:
            output = False

    elif attribute=='forcefield':
        if 'forcefield' not in molecular_system:
            output = False
        elif molecular_system['forcefield'] is None:
            output = False

    elif attribute=='non_bonded_method':
        if 'non_bonded_method' not in molecular_system:
            output = False
        elif molecular_system['non_bonded_method'] is None:
            output = False

    elif attribute=='cutoff_distance':
        if 'cutoff_distance' not in molecular_system:
            output = False
        elif molecular_system['cutoff_distance'] is None:
            output = False

    elif attribute=='switch_distance':
        if 'switch_distance' not in molecular_system:
            output = False
        elif molecular_system['switch_distance'] is None:
            output = False

    elif attribute=='dispersion_correction':
        if 'dispersion_correction' not in molecular_system:
            output = False
        elif molecular_system['dispersion_correction'] is None:
            output = False

    elif attribute=='ewald_error_tolerance':
        if 'ewald_error_tolerance' not in molecular_system:
            output = False
        elif molecular_system['ewald_error_tolerance'] is None:
            output = False

    elif attribute=='hydrogen_mass':
        if 'hydrogen_mass' not in molecular_system:
            output = False
        elif molecular_system['hydrogen_mass'] is None:
            output = False

    elif attribute=='constraints':
        if 'constraints' not in molecular_system:
            output = False
        elif molecular_system['constraints'] is None:
            output = False

    elif attribute=='flexible_constraints':
        if 'flexible_constraints' not in molecular_system:
            output = False
        elif molecular_system['flexible_constraints'] is None:
            output = False

    elif attribute=='water_model':
        if 'water_model' not in molecular_system:
            output = False
        elif molecular_system['water_model'] is None:
            output = False

    elif attribute=='rigid_water':
        if 'rigid_water' not in molecular_system:
            output = False
        elif molecular_system['rigid_water'] is None:
            output = False

    elif attribute=='implicit_solvent':
        if 'implicit_solvent' not in molecular_system:
            output = False
        elif molecular_system['implicit_solvent'] is None:
            output = False

    elif attribute=='solute_dielectric':
        if 'solute_dielectric' not in molecular_system:
            output = False
        elif molecular_system['solute_dielectric'] is None:
            output = False

    elif attribute=='solvent_dielectric':
        if 'solvent_dielectric' not in molecular_system:
            output = False
        elif molecular_system['solvent_dielectric'] is None:
            output = False

    elif attribute=='salt_concentration':
        if 'salt_concentration' not in molecular_system:
            output = False
        elif molecular_system['salt_concentration'] is None:
            output = False

    elif attribute=='kappa':
        if 'kappa' not in molecular_system:
            output = False
        elif molecular_system['kappa'] is None:
            output = False

    return output

