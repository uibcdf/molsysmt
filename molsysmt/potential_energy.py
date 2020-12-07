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

def potential_energy (item, forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff=1.0*nanometer,
                      constraints=None, rigid_water=True, switch_distance=None,
        flexible_constraints=False, selection='all', syntaxis='MolSysMT',
        engine='OpenMM', **kwargs):

    from .multitool import convert

    engine=_digest_engines(engine)

    if engine=='openmm':

        forcefield_omm_parameters=digest_forcefields(forcefield, engine)

        system = convert(item, to_form='openmm.System', forcefield=forcefield)

        kB = _unit.BOLTZMANN_CONSTANT_kB * _unit.AVOGADRO_CONSTANT_NA
        temperature = 0*_unit.kelvin
        pressure    = None

    else:

        raise NotImplementedError

    return get(item, target='system', has_parameters=True)

def energy_minimization (item, method='L-BFGS', forcefield=['AMBER99SB-ILDN','TIP3P'], constraint_HBonds=True,
                         to_form=None, selection=None, syntaxis='MolSysMT', engine='OpenMM', verbose=True, *kwargs):
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

    engine=_digest_engines(engine)
    in_form = get_form(item)
    if to_form is None:
        to_form = in_form

    if engine=='OpenMM':

        from simtk.openmm import app, LangevinIntegrator
        from simtk.openmm import Platform
        from simtk import unit as unit

        forcefield_omm_parameters=digest_forcefields(forcefield, engine)

        system = convert(item, to_form='openmm.System')

        kB = _unit.BOLTZMANN_CONSTANT_kB * _unit.AVOGADRO_CONSTANT_NA
        temperature = 0*_unit.kelvin
        pressure    = None

        friction   = 1.0/_unit.picosecond
        step_size  = 2.0*_unit.femtoseconds
        integrator = _LangevinIntegrator(temperature, friction, step_size)
        integrator.setConstraintTolerance(0.00001)

        platform = _Platform.getPlatformByName('CUDA')
        properties = {'CudaPrecision': 'mixed'}

        simulation = _app.Simulation(topology, system, integrator, platform, properties)
        simulation.context.setPositions(positions)
        simulation.context.setVelocitiesToTemperature(0*_unit.kelvin)

        if verbose:
            state_pre_min = simulation.context.getState(getEnergy=True)
            energy_pre_min = state_pre_min.getPotentialEnergy()
            print("Potential Energy before minimization: {}".format(energy_pre_min))

        if method=='L-BFGS':
            simulation.minimizeEnergy()

        if verbose:
            state_post_min = simulation.context.getState(getEnergy=True)
            energy_post_min = state_post_min.getPotentialEnergy()
            print("Potential Energy after minimization: {}".format(energy_post_min))

        tmp_item = _convert(simulation, to_form=out_form)

        return tmp_item

    else:

        raise NotImplementedError

