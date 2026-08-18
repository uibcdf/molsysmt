from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest()
def get_forces(molecular_system, selection='all', engine='OpenMM', syntax='MolSysMT', skip_digestion=False):
    """
    Calculating the atomic forces acting on the molecular system.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection of atoms for which forces are extracted.
    engine : str, default='OpenMM'
        Simulation engine backend used for force calculation.
    syntax : str, default='MolSysMT'
        Selection syntax used.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    quantity
        NumPy array of force vectors with shape `(n_atoms, 3)` in canonical units (`kJ/(mol*nm)`).

    .. versionadded:: 1.0.0
    """

    from molsysmt import convert, get_form, has_attribute
    from molsysmt.configure import default_attribute

    if engine == 'OpenMM':

        form_in = get_form(molecular_system)

        if form_in == 'openmm.Context':
            context = molecular_system
        elif form_in == 'openmm.Simulation':
            context = molecular_system.context
        else:
            extra_conversion_arguments = {}
            possible_missing_attributes = ['forcefield', 'water_model', 'implicit_solvent', 'constraints',
                                          'non_bonded_method', 'switch_distance', 'dispersion_correction', 'ewald_error_tolerance',
                                          'integrator', 'temperature', 'friction', 'time_step']

            for att in possible_missing_attributes:
                if not has_attribute(molecular_system, att):
                    extra_conversion_arguments[att] = default_attribute[att]

            context = convert(molecular_system, to_form='openmm.Context', **extra_conversion_arguments)

        state = context.getState(getForces=True)
        forces = state.getForces(asNumpy=True)
        forces = puw.standardize(forces)

        if not is_all(selection):
            from molsysmt.basic import select
            atom_indices = select(molecular_system, selection=selection, syntax=syntax)
            forces = forces[atom_indices]

        return forces

    else:
        raise NotImplementedError
