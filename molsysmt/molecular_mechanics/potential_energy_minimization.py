from molsysmt import pyunitwizard as puw
from molsysmt._private.digestion import digest

@digest()
def potential_energy_minimization(molecular_system, method='L-BFGS',
        platform='CUDA', engine='OpenMM', to_form=None, in_place=True, verbose=False):

    """
    To be written soon...

    potential_energy_minimization(molecular_system, ...)

    A new structure is returned with the molecular model relaxed to the nearest potential energy local
    minimum.

    Parameters
    ----------
    item : molecular model
        Molecular model in any form to be operated by the method.
    method : str (default "L-BFGS")
        Energy minimization method.
    method : str (default "AMBER99SB-ILDN")
        Forcefield to model the inter-atomic interactions.
    selection : str, int, list, tuple or numpy array (default None)
        Region to be minimized defined as a selection sentence or atoms indices list. By default
        None means all atoms and there by the whole molecular model is minized.
    syntax : str (default "mdtraj")
        Name of the selection syntax used: "mdtraj" or "amber".
    engine : str (default "openmm")

    Returns
    -------
    item : molecular model
        The result is a new molecular model with coordinates or positions relaxed to the nearest local minimum of
        the potential energy.

    Examples
    --------
    Remove chains 0 and 1 from the pdb: 1B3T.
    >>> import molsysmt as msm
    >>> system = msm.load('pdb:1B3T')
    Check the number of chains
    >>> minimized_system = m3t.molecular_mechanics.potential_energy_minimization(system)

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

