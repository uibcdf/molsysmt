# =======================
# Potential Energy
# =======================

"""
Potential Energy
================

Methods related with the potential energy of the system.
From energy minimization to potential energy contribution of specific set of atoms or interactions.
"""

from .utils.engines import digest as digest_engines
from .utils.forcefields import digest as digest_forcefields
import simtk.unit as unit

def potential_energy (item, forcefield=None, non_bonded_method='no_cutoff',
        non_bonded_cutoff=1.0*unit.nanometers, constraints=None, rigid_water=True,
        switch_distance=None, flexible_constraints=False, platform='CUDA',
        selection='all', syntaxis='MolSysMT', engine='OpenMM'):

    from .multitool import get_form, convert

    engine=digest_engines(engine)
    in_form = get_form(item)

    if engine=='OpenMM':

        tmp_item = convert(item,
            forcefield=forcefield, non_bonded_method=non_bonded_method,
            non_bonded_cutoff=non_bonded_cutoff, constraints=constraints,
            rigid_water=rigid_water, switch_distance=switch_distance,
            flexible_constraints=flexible_constraints,
            integrator='Langevin', temperature=0*unit.kelvin, collisions_rate=1.0/unit.picoseconds,
            integration_timestep=2.0*unit.femtoseconds, platform=platform,
            selection=selection, syntaxis=syntaxis, to_form='openmm.Simulation')

        state = tmp_item.context.getState(getEnergy=True)
        output = state.getPotentialEnergy()

    else:

        raise NotImplementedError()

    return output.in_units_of(unit.kilocalories_per_mole)


def energy_minimization (item, method='L-BFGS', forcefield=None, non_bonded_method='no_cutoff',
        non_bonded_cutoff=1.0*unit.nanometers, constraints=None, rigid_water=True,
        switch_distance=None, flexible_constraints=False, platform='CUDA',
        to_form=None, selection='all', syntaxis='MolSysMT', engine='OpenMM', verbose=True, *kwargs):

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

    from .multitool import get_form, get, convert

    engine=digest_engines(engine)
    in_form = get_form(item)
    if to_form is None:
        to_form = in_form

    if engine=='OpenMM':

        simulation = convert(item,
            forcefield=forcefield, non_bonded_method=non_bonded_method,
            non_bonded_cutoff=non_bonded_cutoff, constraints=constraints,
            rigid_water=rigid_water, switch_distance=switch_distance,
            flexible_constraints=flexible_constraints,
            integrator='Langevin', temperature=0*unit.kelvin, collisions_rate=1.0/unit.picoseconds,
            integration_timestep=2.0*unit.femtoseconds, platform=platform,
            selection=selection, syntaxis=syntaxis, to_form='openmm.Simulation')

        if verbose:
            state_pre_min = simulation.context.getState(getEnergy=True)
            energy_pre_min = state_pre_min.getPotentialEnergy().in_units_of(unit.kilocalories_per_mole)
            print("Potential Energy before minimization: {}".format(energy_pre_min))

        if method=='L-BFGS':
            simulation.minimizeEnergy()

        if verbose:
            state_post_min = simulation.context.getState(getEnergy=True)
            energy_post_min = state_post_min.getPotentialEnergy().in_units_of(unit.kilocalories_per_mole)
            print("Potential Energy after minimization: {}".format(energy_post_min))

        tmp_item = convert(simulation, to_form=to_form)

        return tmp_item

    else:

        raise NotImplementedError

