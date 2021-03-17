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

def potential_energy (molecular_system, molecular_mechanics_parameters=None, selection='all', syntaxis='MolSysMT', engine='OpenMM'):

    from molsysmt._private_tools.engines import digest_engine
    from molsysmt._private_tools._digestion import digest_molecular_system
    engine=digest_engines(engine)

    if engine=='OpenMM':

        molecular_system = digest_molecular_system(molecular_system)
        molecular_system = molecular_system.combine_with_items(molecular_mechanics_parameters)
        if molecular_system.simulation_item is None:
            from molsysmt.native.simulation import simulation_to_potential_energy_minimization
            molecular_system.combine_with_items(simulation_to_potential_energy_minimization)
        context = convert(molecular_system, selection=selection, syntaxis=syntaxis, to_form='openmm.Context')
        state = context.getState(getEnergy=True)
        output = state.getPotentialEnergy()

    else:

        raise NotImplementedError()

    output = puw.standardize(output)

    return output


def energy_minimization (molecular_system, molecular_mechanics_parameters=None, selection='all', syntaxis='MolSysMT', engine='OpenMM', to_form=None, verbose=True):

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
            rigid_water=rigid_water, hydrogen_mass=hydrogen_mass, switch_distance=switch_distance,
            flexible_constraints=flexible_constraints,
            use_dispersion_correction=use_dispersion_correction, ewald_error_tolerance=ewald_error_tolerance,
            water_model=water_model, implicit_solvent=implicit_solvent, implicit_solvent_salt_conc=implicit_solvent_salt_conc,
            implicit_solvent_kappa=implicit_solvent_kappa, solute_dielectric=solute_dielectric, solvent_dielectric=solvent_dielectric,
            integrator='Langevin', temperature='0 K', collisions_rate='1.0 1/ps',
            integration_timestep='2.0 fs', platform=platform,
            selection=selection, syntaxis=syntaxis, to_form='openmm.Simulation')

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

