# =======================
# Potential Energy
# =======================


"""
Potential Energy
================

Methods related with the potential energy of the system.
From energy minimization to potential energy contribution of specific set of atoms or interactions.
"""


def energy_minimization (item, method='L-BFGS', forcefield='AMBER99SB-ILDN', constraint_HBonds=True,
                         selection=None, syntaxis='mdtraj', engine='openmm', verbose=True, *kwargs):
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
    >>> import molmodmt as m3t
    >>> system = m3t.load('pdb:1B3T')
    Check the number of chains
    >>> minimized_system = m3t.minimze(system)

    """

    from .multitool import get_form as _get_form, get as _get
    from .multitool import convert as _convert, reformat as _reformat
    from .utils.forcefields import switcher as _ff_switcher

    if engine=='openmm':

        from simtk.openmm import app as _app, LangevinIntegrator as _LangevinIntegrator
        from simtk.openmm import Platform as _Platform
        from simtk import unit as _unit

        forcefield_omm_parameters=_ff_switcher(forcefield)

        in_form = _get_form(item)

        topology = _convert(item, 'openmm.Topology')
        positions = _get(item, coordinates=True)
        positions = _reformat(attribute='coordinates', value=positions, is_format=in_form,
                              to_format='openmm')

        forcefield_generator = _app.ForceField(forcefield_omm_parameters)

        constraints=None
        if constraint_HBonds:
            constraints = _app.HBonds

        system = forcefield_generator.createSystem(topology, constraints=constraints)

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

        tmp_item = _convert(simulation, in_form)

        return tmp_item

