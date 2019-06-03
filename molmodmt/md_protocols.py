# =======================
# Potential Energy
# =======================

from .utils.engines import digest_engines as _digest_engines
from .utils.forcefields import switcher as _digest_forcefields


"""
Potential Energy
================

Methods related with the potential energy of the system.
From energy minimization to potential energy contribution of specific set of atoms or interactions.
"""

def equilibration_NVT (item, protocol=0, forcefield=['AMBER99SB-ILDN','TIP3P'],
                       contraint_HBonds=True, engine='OpenMM', verbose=True, *kwargs):
    raise NotImplementedError

def equilibration_NPT (item, temperature=300*unit.kelvin, pressure=1.0*unit.atmosphere,
                       protocol=0, forcefield=['AMBER99SB-ILDN','TIP3P'],
                       engine='OpenMM', verbose=True, *kwargs):
    """equilibration_NPT (item, protocol, forcefield, constraint_HBonds, engine, verbose)

    Description

    Parameters
    ----------
    item : molecular model
        Molecular model in any form to be operated by the method.
    protocol : int (default 0)
        description.
    forcefield : list or str (default ["AMBER99SB-ILDN", "TIP3P"])
        Forcefield to model the inter-atomic interactions.
    engine : str (default "OpenMM")

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
    >>> minimized_system = m3t.minimze(system)
    >>> minimized_equilibrated = m3t.equilibration_NPT(system)
    """

    from .multitool import get_form, get, convert, reformat

    engine = _digest_engines(engine)

    if engine=='OpenMM':

        import simtk.openmm.app as app
        import simtk.openmm as mm
        import simtk.unit as unit

        forcefield_omm_parameters= _digest_forcefields(forcefield, engine)

        in_form = _get_form(item)

        topology = _convert(item, 'openmm.Topology')
        positions = get(item, coordinates=True)
        positions = reformat(attribute='coordinates', value=positions,
                             is_format=in_form, to_format='openmm')

        forcefield_generator = _app.ForceField(*forcefield_omm_parameters)

        ## System
        system = forcefield_generator.createSystem(topology,
                                                   constraints=app.HBonds,
                                                   nonbondedMethod=app.PME,
                                                   nonbondedCutoff=1.0*unit.nanometers,
                                                   rigidWater=True,
                                                   ewaldErrorTolerance=0.0005
                                                   )
        ## Thermodynamic State
        kB = unit.BOLTZMANN_CONSTANT_kB * unit.AVOGADRO_CONSTANT_NA
        temperature = temperature
        pressure = pressure

        ## Heavy atoms constrained equilibration
        friction   = 1.0/unit.picosecond
        step_size  = 2.0*unit.femtoseconds
        integrator = mm.LangevinIntegrator(temperature, friction, step_size)
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

    else:

        raise NotImplementedError

