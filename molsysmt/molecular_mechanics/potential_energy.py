# =======================
# Potential Energy
# =======================

"""
Potential Energy
================

Methods related with the potential energy of the system.
From energy minimization to potential energy contribution of specific set of atoms or interactions.
"""

from molsysmt import puw

def potential_energy (molecular_system, selection='all', syntaxis='MolSysMT', engine='OpenMM'):

    from molsysmt._private.engines import digest_engine
    from molsysmt._private._digestion import digest_molecular_system
    from molsysmt.basic import convert

    engine=digest_engine(engine)

    if engine=='OpenMM':

        molecular_system = digest_molecular_system(molecular_system)
        if molecular_system.simulation_item is None:
            from molsysmt.native.simulation import simulation_to_potential_energy_minimization
            molecular_system = molecular_system.combine_with_items(simulation_to_potential_energy_minimization)
        context = convert(molecular_system, to_form='openmm.Context', selection=selection, syntaxis=syntaxis)
        state = context.getState(getEnergy=True)
        output = state.getPotentialEnergy()

    else:

        raise NotImplementedError()

    output = puw.standardize(output)

    return output


def energy_minimization (molecular_system, method='L-BFGS', selection='all', syntaxis='MolSysMT', engine='OpenMM', to_form=None, verbose=True):

    """remove(item, selection=None, syntaxis='mdtraj')

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
    syntaxis : str (default "mdtraj")
        Name of the selection syntaxis used: "mdtraj" or "amber".
    engine : str (default "openmm")

    Returns
    -------
    item : molecular model
        The result is a new molecular model with coordinates or positions relaxed to the nearest local minimum of
        the potential energy.

    Examples
    --------
    Remove chains 0 and 1 from the pdb: 1B3T.
    >>> import molsysmt as m3t
    >>> system = m3t.load('pdb:1B3T')
    Check the number of chains
    >>> minimized_system = m3t.minimze(system)

    """

    from molsysmt._private.engines import digest_engine
    from molsysmt._private._digestion import digest_molecular_system
    from molsysmt.basic import convert, get_form

    engine=digest_engine(engine)
    in_form = get_form(molecular_system)
    if to_form is None:
        to_form = in_form

    if engine=='OpenMM':

        molecular_system = digest_molecular_system(molecular_system)
        if molecular_system.simulation_item is None:
            from molsysmt.native.simulation import simulation_to_potential_energy_minimization
            molecular_system = molecular_system.combine_with_items(simulation_to_potential_energy_minimization)

        simulation = convert(molecular_system, to_form='openmm.Simulation', selection=selection, syntaxis=syntaxis)

        if verbose:
            state_pre_min = simulation.context.getState(getEnergy=True)
            energy_pre_min = state_pre_min.getPotentialEnergy()
            energy_pre_min = puw.standardize(energy_pre_min)
            print("Potential Energy before minimization: {}".format(energy_pre_min))

        if method=='L-BFGS':
            simulation.minimizeEnergy()

        if verbose:
            state_post_min = simulation.context.getState(getEnergy=True)
            energy_post_min = state_post_min.getPotentialEnergy()
            energy_post_min = puw.standardize(energy_post_min)
            print("Potential Energy after minimization: {}".format(energy_post_min))

        tmp_item = convert(simulation, to_form=to_form)

        return tmp_item

    else:

        raise NotImplementedError

