from molsysmt import pyunitwizard as puw
from molsysmt._private.digestion import digest

@digest()
def potential_energy_minimization(molecular_system, molecular_mechanics={'forcefield':'AMBER99SB-ILDN'}, method='L-BFGS',
        engine='OpenMM', to_form=None, inplace=False, verbose=True):

    """potential_energy_minimization(molecular_system, ...)

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

    in_form = get_form(molecular_system)
    if to_form is vNone:
        to_form = in_form

    if engine=='OpenMM':

        if method!='L-BFGS':
            raise ValueError

        if in_form=='openmm.Context':

            if inplace:
                output = molecular_system
            else:
                output = copy(molecular_system)

            from openmm import LocalEnergyMinimizer
            state_pre_min = output.getState(getEnergy=True)
            LocalEnergyMinimizer.minimize(output)
            state_post_min = output.getState(getEnergy=True)

        elif in_form=='openmm.Simulation':

            if inplace:
                output = molecular_system
            else:
                output = copy(molecular_system)

            state_pre_min = output.context.getState(getEnergy=True)
            output.minimizeEnergy()
            state_post_min = output.context.getState(getEnergy=True)

        else:

            if has_attribute(molecular_system, 'mechanical'):
                output = convert(molecular_system, to_form='openmm.Simulation')
            else:
                output = convert([molecular_system, molecular_mechanics], to_form='openmm.Simulation')

            state_pre_min = output.context.getState(getEnergy=True)
            simulation.minimizeEnergy()
            state_post_min = output.context.getState(getEnergy=True)

            if inplace:
                from molsysmt.form.openmm_Simulation import get_coordinates_from_system
                coordinates = get_coordinates_from_system(output)
                set(molecular_system, coordinates=coordinates)

        if verbose:
            energy_pre_min = state_pre_min.getPotentialEnergy()
            energy_pre_min = puw.standardize(energy_pre_min)
            print("Potential Energy before minimization: {}".format(energy_pre_min))
            energy_post_min = state_post_min.getPotentialEnergy()
            energy_post_min = puw.standardize(energy_post_min)
            print("Potential Energy after minimization: {}".format(energy_post_min))

        if inplace:
            pass
        else:
            output = convert(output, to_form=to_form)
            return output

    else:

        raise NotImplementedError

