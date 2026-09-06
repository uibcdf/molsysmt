from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest

@arg_digest()
def potential_energy_minimization(molecular_system, method='L-BFGS',
        platform='CPU', engine='OpenMM', to_form=None, in_place=False, verbose=False):

    """
    Relax a molecular system to a local minimum of the potential energy.

    Performs energy minimization using the chosen backend optimizer. The minimized
    coordinates are applied either in-place to the original molecular system or to
    a new copy depending on the ``in_place`` flag.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    method : str, default='L-BFGS'
        Local minimization algorithm. OpenMM's ``LocalEnergyMinimizer`` implements
        L-BFGS, so 'L-BFGS' is the only accepted value; any other name is refused.
    platform : str, default='CPU'
        OpenMM platform name. Accepted values are 'CPU' and 'CUDA'.
    engine : str, default='OpenMM'
        Engine performing the minimization. Only 'OpenMM' is implemented.
    to_form : str, default=None
        Form of the returned molecular system when ``in_place=False``. With None the
        input form is preserved.
    in_place : bool, default=False
        Whether the minimized coordinates are written into ``molecular_system``
        instead of being returned in a new molecular system.
    verbose : bool, default=False
        Whether the potential energy before and after the minimization is printed.

    Returns
    -------
    molecular system or None
        When ``in_place=False``, returns a molecular system with the minimized
        coordinates in the form specified by ``to_form`` (or the original form).
        When ``in_place=True``, returns None and updates ``molecular_system`` in
        place (only applicable for non-Context/Simulation forms).


    Raises
    ------
    NotImplementedError
        Raised if the requested ``engine`` is not supported.


    Notes
    -----
    If the input is not already an ``openmm.Context`` or ``openmm.Simulation``,
    the molecular system is converted to an ``openmm.Context`` using the MolSysMT
    default attributes for any missing molecular-mechanics parameters (forcefield,
    integrator, temperature, etc.).

    The minimization is performed by OpenMM's ``LocalEnergyMinimizer.minimize``,
    which converges to the nearest local minimum of the force-field potential
    energy surface.


    .. versionadded:: 1.0.0
    """

    from molsysmt import convert, get_form, has_attribute, set, copy
    from molsysmt.configure import default_attribute

    if engine=='OpenMM':

        from openmm import LocalEnergyMinimizer

        form_in = get_form(molecular_system)

        if form_in == 'openmm.Context':

            context=molecular_system

        elif form_in == 'openmm.Simulation':

            context = molecular_system.context

        else:

            extra_conversion_arguments={}

            possible_missing_attributes=['forcefield', 'water_model', 'implicit_solvent', 'constraints',
                    'non_bonded_method', 'switch_distance', 'dispersion_correction', 'ewald_error_tolerance',
                    'integrator', 'temperature', 'friction', 'time_step']

            for att in possible_missing_attributes:
                if not has_attribute(molecular_system, att):
                    extra_conversion_arguments[att]=default_attribute[att]

            context = convert(molecular_system, to_form='openmm.Context',
                    **extra_conversion_arguments, platform=platform)

        state_pre_min = context.getState(getEnergy=True)
        LocalEnergyMinimizer.minimize(context)
        state_post_min = context.getState(getEnergy=True, getPositions=True)

        if verbose:
            energy_pre_min = state_pre_min.getPotentialEnergy()
            energy_pre_min = puw.standardize(energy_pre_min)
            print("Potential Energy before minimization: {}".format(energy_pre_min))
            energy_post_min = state_post_min.getPotentialEnergy()
            energy_post_min = puw.standardize(energy_post_min)
            print("Potential Energy after minimization: {}".format(energy_post_min))

        if in_place:
            if form_in not in ['openmm.Context','openmm.Simulation']:
                coordinates = state_post_min.getPositions(asNumpy=True)
                set(molecular_system, coordinates=coordinates)
            pass
        else:
            if to_form is None:
                output=copy(molecular_system)
            else:
                output = convert(molecular_system, to_form=to_form)
            coordinates = state_post_min.getPositions(asNumpy=True)
            set(output, coordinates=coordinates)
            return output

    else:

        raise NotImplementedError

