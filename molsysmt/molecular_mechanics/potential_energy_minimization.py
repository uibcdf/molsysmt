from molsysmt import pyunitwizard as puw
from molsysmt._private.arg_digestion import arg_digest

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
        Molecular system in any of :ref:`the supported forms <Introduction_Forms>`.
        When ``engine='OpenMM'``, the system may also be provided directly as an
        ``openmm.Context`` or ``openmm.Simulation`` object, in which case the
        context is used and reused without conversion.

    method : str, default 'L-BFGS'
        Energy minimization algorithm. Currently only the L-BFGS method provided
        by OpenMM's ``LocalEnergyMinimizer`` is supported.

    platform : str, default 'CPU'
        OpenMM platform used when creating a new context from the molecular system.
        Common values: ``'CPU'``, ``'CUDA'``, ``'OpenCL'``, ``'Reference'``.

    engine : {'OpenMM'}, default 'OpenMM'
        Backend used to perform the minimization. Only ``'OpenMM'`` is currently
        supported.

    to_form : str or None, default None
        Target form for the output molecular system when ``in_place=False``. If
        None, a copy of the input is returned in its original form.

    in_place : bool, default False
        If True, the minimized coordinates are written back into ``molecular_system``
        directly and the function returns None. If False, a new molecular system is
        returned with the relaxed coordinates.

    verbose : bool, default False
        If True, print the potential energy before and after minimization.

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
    from molsysmt.config import default_attribute

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

