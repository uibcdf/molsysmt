from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolecularMechanics')
def has_attribute(molecular_system, **kwargs):

    arguments = []
    for key in kwargs.keys():
        if kwargs[key]:
            arguments.append(key)

    outputs = []

    for argument in arguments:

        output = False

        ###
        ### MECHANICAL ATTRIBUTES
        ###

        if argument=='formal_charge':
            if molecular_system.molecular_mechanics.formal_charge is not None:
                output = True

        elif argument=='partial_charge':
            if molecular_system.molecular_mechanics.partial_charge is not None:
                output = True

        elif argument=='forcefield':
            if molecular_system.molecular_mechanics.forcefield is not None:
                output = True

        elif argument=='non_bonded_method':
            if molecular_system.molecular_mechanics.non_bonded_method is not None:
                output = True

        elif argument=='cutoff_distance':
            if molecular_system.molecular_mechanics.cutoff_distance is not None:
                output = True

        elif argument=='switch_distance':
            if molecular_system.molecular_mechanics.switch_distance is not None:
                output = True

        elif argument=='dispersion_correction':
            if molecular_system.molecular_mechanics.dispersion_correction is not None:
                output = True

        elif argument=='ewald_error_tolerance':
            if molecular_system.molecular_mechanics.ewald_error_tolerance is not None:
                output = True

        elif argument=='hydrogen_mass':
            if molecular_system.molecular_mechanics.hydrogen_mass is not None:
                output = True

        elif argument=='constraints':
            if molecular_system.molecular_mechanics.constraints is not None:
                output = True

        elif argument=='flexible_constraints':
            if molecular_system.molecular_mechanics.flexible_constraints is not None:
                output = True

        elif argument=='water_model':
            if molecular_system.molecular_mechanics.water_model is not None:
                output = True

        elif argument=='rigid_water':
            if molecular_system.molecular_mechanics.rigid_water is not None:
                output = True

        elif argument=='implicit_solvent':
            if molecular_system.molecular_mechanics.implicit_solvent is not None:
                output = True

        elif argument=='solute_dielectric':
            if molecular_system.molecular_mechanics.solute_dielectric is not None:
                output = True

        elif argument=='solvent_dielectric':
            if molecular_system.molecular_mechanics.solvent_dielectric is not None:
                output = True

        elif argument=='salt_concentration':
            if molecular_system.molecular_mechanics.salt_concentration is not None:
                output = True

        elif argument=='kappa':
            if molecular_system.molecular_mechanics.kappa is not None:
                output = True

        outputs.append(output)

    if len(outputs)==1:
        return outputs[0]
    else:
        return outputs

