# =======================
# Potential Energy
# =======================

"""
Potential Energy
================

Methods related with the potential energy of the system.
From energy minimization to potential energy contribution of specific set of atoms or interactions.
"""

from molsysmt._private_tools.exceptions import *
from molsysmt import puw

def potential_energy (molecular_system, forcefield=None, non_bonded_method='no_cutoff',
    non_bonded_cutoff='1.0 nm', constraints=None, rigid_water=True,
    switch_distance=None, flexible_constraints=False, use_dispersion_correction=False, ewald_error_tolerance=0.0001,
    water_model=None, implicit_solvent=None, implicit_solvent_salt_conc='0.0 mol/L',
    implicit_solvent_kappa='0.0 1/nm', solute_dielectric=1.0, solvent_dielectric=78.5,
    platform='CUDA', selection='all', frame_indices='all', syntaxis='MolSysMT', engine='OpenMM'):

    from molsysmt._private_tools._digestion import digest_engine
    from molsysmt.multitool import convert

    engine=digest_engine(engine)

    if engine=='OpenMM':

        tmp_molecular_system = convert(molecular_system,
            forcefield=forcefield, non_bonded_method=non_bonded_method,
            non_bonded_cutoff=non_bonded_cutoff, constraints=constraints,
            rigid_water=rigid_water, switch_distance=switch_distance,
            flexible_constraints=flexible_constraints, use_dispersion_correction=use_dispersion_correction,
            ewald_error_tolerance=ewald_error_tolerance, water_model=water_model, implicit_solvent=implicit_solvent,
            implicit_solvent_salt_conc=implicit_solvent_salt_conc, implicit_solvent_kappa=implicit_solvent_kappa,
            solute_dielectric=solute_dielectric, solvent_dielectric=solvent_dielectric,
            integrator='Langevin', temperature='0 K', collisions_rate='1.0 1/ps',
            integration_timestep='2.0 fs', platform=platform,
            selection=selection, frame_indices=frame_indices, syntaxis=syntaxis, to_form='openmm.Simulation')

        state = tmp_molecular_system.context.getState(getEnergy=True)
        output = state.getPotentialEnergy()

    else:

        raise NotImplementedError()

    output = puw.standardize(output)

    return output

def energy_minimization (molecular_system, method='L-BFGS', forcefield=None, non_bonded_method='no_cutoff',
        non_bonded_cutoff='1.0 nm', constraints=None, rigid_water=True, hydrogen_mass=None,
        switch_distance=None, flexible_constraints=False, use_dispersion_correction=False, ewald_error_tolerance=0.0001,
        water_model=None, implicit_solvent=None, implicit_solvent_salt_conc= '0.0 mol/L',
        implicit_solvent_kappa='0.0 1/nm', solute_dielectric=1.0, solvent_dielectric=78.5,
        platform='CUDA', to_form=None, selection='all', frame_indices='all', syntaxis='MolSysMT', engine='OpenMM', verbose=True):

    """remove(molecular_system, selection=None, syntaxis='mdtraj')

    A new structure is returned with the molecular model relaxed to the nearest potential energy local
    minimum.

    Parameters
    ----------
    molecular_system : molecular model
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
    molecular_system : molecular model
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
    from molsysmt._private_tools._digestion import digest_engine
    from molsysmt.multitool import convert, get_form

    engine=digest_engine(engine)

    if to_form is None:
        to_form = get_form(molecular_system)

    if engine=='OpenMM':

        simulation = convert(molecular_system,
            forcefield=forcefield, non_bonded_method=non_bonded_method,
            non_bonded_cutoff=non_bonded_cutoff, constraints=constraints,
            rigid_water=rigid_water, hydrogen_mass=hydrogen_mass, switch_distance=switch_distance,
            flexible_constraints=flexible_constraints,
            use_dispersion_correction=use_dispersion_correction, ewald_error_tolerance=ewald_error_tolerance,
            water_model=water_model, implicit_solvent=implicit_solvent, implicit_solvent_salt_conc=implicit_solvent_salt_conc,
            implicit_solvent_kappa=implicit_solvent_kappa, solute_dielectric=solute_dielectric, solvent_dielectric=solvent_dielectric,
            integrator='Langevin', temperature='0 K', collisions_rate='1.0 1/ps',
            integration_timestep='2.0 fs', platform=platform,
            selection=selection, frame_indices=frame_indices, syntaxis=syntaxis, to_form='openmm.Simulation')

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

        tmp_molecular_system = convert(simulation, to_form=to_form)

        return tmp_molecular_system

    else:

        raise NotImplementedError

