# =======================
# Potential Energy
# =======================

from .utils.engines import digest_engines as _digest_engines
from .utils.forcefields import switcher as _digest_forcefields
import simtk._unit as _unit

"""
Potential Energy
================

Methods related with the potential energy of the system.
From energy minimization to potential energy contribution of specific set of atoms or interactions.
"""

def equilibration_NVT (item, protocol=0, forcefield=['AMBER99SB-ILDN','TIP3P'],
                       contraint_HBonds=True, engine='OpenMM', verbose=True, *kwargs):
    raise NotImplementedError

def equilibration_NPT (item, temperature=300*_unit.kelvin, pressure=1.0*_unit.atmosphere,
                       time=1.0*_unit.nanosecond, protocol=0, forcefield=['AMBER99SB-ILDN','TIP3P'],
                       engine='OpenMM', verbose=True, form_out=None, *kwargs):
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

        in_form = _get_form(item)

        forcefield = _digest_forcefields(forcefield, engine)

        in_form = _get_form(item)

        topology = _convert(item, 'openmm.Topology')
        positions = get(item, coordinates=True)
        positions = reformat(attribute='coordinates', value=positions,
                             is_format=in_form, to_format='openmm')

        if protocol==0:

            new_positions, new_velocities, equil_data = _equil_NPT_OpenMM_protocol_0(topology,
                                                                                     positions,
                                                                                     temperature=temperature,
                                                                                     pressure=pressure,
                                                                                     time=time,
                                                                                     forcefield=forcefield,
                                                                                     verbose=verbose,
                                                                                     progress_bar=progress_bar)
    else:

        raise NotImplementedError

def _equil_NPT_OpenMM_protocol_0(topology, positions,
                                 temperature=300.0*_unit.kelvin, pressure=1.0*_unit.atmosphere,
                                 time= 1.0*_unit.nanosecond, forcefield=None, verbose=True,
                                 progress_bar=True):

    import numpy as np
    import simtk.openmm.app as app
    import simtk.openmm as mm
    from openmmtools.integrators import LangevinIntegrator, GeodesicBAOABIntegrator

    if progress_bar:
        from tqdm import tqdm
    else:
        def tqdm(arg):
            return arg

    #item needs to be openmm.modeller

    forcefield = app.ForceField("amber99sbildn.xml","tip3p.xml")
    topology = item.topology
    positions = item.positions

    system = forcefield_generator.createSystem(topology,
                                               contraints=app.HBonds,
                                               nonbondedMethod=app.PME,
                                               nonbondedCutoff=1.0*_unit.nanometers,
                                               rigidWater=True,
                                               ewaldErrorTolerance=0.0005
                                              )

    ## Thermodynamic State
    kB = _unit.BOLTZMANN_CONSTANT_kB * _unit.AVOGADRO_CONSTANT_NA
    temperature = temperature
    pressure = pressure

    ## Barostat
    barostat_frequency = 25 # steps
    barostat = mm.MonteCarloBarostat(pressure, temperature, barostat_frequency)
    system.addForce(barostat)

    ## Integrator
    friction   = 1.0/_unit.picosecond
    step_size  = 2.0*_unit.femtoseconds
    integrator = LangevinIntegrator(temperature, friction, step_size)
    integrator.setConstraintTolerance(0.00001)

    ## Platform
    platform = mm.Platform.getPlatformByName('CUDA')
    properties = {'CudaPrecision': 'mixed'}

    ## Simulation
    simulation = app.Simulation(topology, system, integrator, platform, properties)
    simulation.context.setPositions(positions)
    simulation.context.setVelocitiesToTemperature(temperature)

    time_equilibration = time
    time_iteration = 0.2 * _unit.picoseconds
    number_iterations = int(time_equilibration/time_iteration)
    steps_iteration = int(time_iteration/step_size)
    steps_equilibration = number_iterations*steps_iteration

    ## Reporters

    net_mass, n_degrees_of_freedom = m3t.get(system, net_mass=True, n_degrees_of_freedom=True)
    niters = number_iterations
    data = dict()
    data['time'] = _unit.Quantity(np.zeros([niters], np.float64), _unit.picoseconds)
    data['potential'] = _unit.Quantity(np.zeros([niters], np.float64), _unit.kilocalories_per_mole)
    data['kinetic'] = _unit.Quantity(np.zeros([niters], np.float64), _unit.kilocalories_per_mole)
    data['volume'] = _unit.Quantity(np.zeros([niters], np.float64), _unit.angstroms**3)
    data['density'] = _unit.Quantity(np.zeros([niters], np.float64), _unit.gram / _unit.centimeters**3)
    data['kinetic_temperature'] = unit.Quantity(np.zeros([niters], np.float64), _unit.kelvin)

    for iteration in tqdm(range(number_iterations)):
        integrator.step(steps_iteration)
        state = simulation.context.getState(getEnergy=True)
        time = state.getTime()
        potential_energy = state.getPotentialEnergy()
        kinetic_energy = state.getKineticEnergy()
        volume = state.getPeriodicBoxVolume()
        density = (net_mass / volume).in_units_of(unit.gram / unit.centimeter**3)
        kinetic_temperature = (2.0 * kinetic_energy / kB / n_degrees_of_freedom).in_units_of(unit.kelvin) # (1/2) ndof * kB * T = KE
        data['time'][iteration]=time
        data['potential'] = potential_energy
        data['kinetic'] = kinetic_energy
        data['volume'] = volume
        data['density'] = density
        data['kinetic_temperature'] = kinetic_temperature

    final_state = simulation.context.getState(getPositions=True, getVelocities=True)
    final_positions = final_state.getPositions()
    final_velocities = final_state.getVelocities()

    return final_positions, final_velocities, data

