
molecular_mechanics_parameters = {
    'forcefield', 'non_bonded_method', 'non_bonded_cutoff', 'switch_distance',
    'use_dispersion_correction', 'ewald_error_tolerance', 'hydrogen_mass',
    'constraints', 'flexible_constraints', 'constraint_tolerance',
    'water_model', 'rigid_water', 'residue_templates', 'ignore_external_bonds',
    'implicit_solvent', 'solute_dielectric', 'solvent_dielectric', 'implicit_solvent_salt_conc',
    'implicit_solvent_kappa',
}

def is_molecular_mechanics_dict(dictionary):

    keys=set(dictionary.keys())
    output = (keys <= molecular_mechanics_parameters)

    return output


