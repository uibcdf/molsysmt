"""
Unit and regression test for the copy module of the molsysmt package.
"""

import molsysmt as msm
import openmm as mm
from openmm import unit
from openmm import app
import numpy as np

topology = app.Topology()
chain = topology.addChain('A')
residue = topology.addResidue('Ar', chain)
atom = topology.addAtom(name='Ar', element= app.element.argon, residue=residue)
chain = topology.addChain('B')
residue = topology.addResidue('Ar', chain)
atom = topology.addAtom(name='Ar', element= app.element.argon, residue=residue)

def test_pin_atoms_1():

    system = mm.System()
    system.addParticle(atom.element.mass) # masa del átomo de argón
    system.addParticle(atom.element.mass) # masa del átomo de argón

    temperature = 300*unit.kelvin
    integration_timestep = 2.0*unit.femtoseconds
    saving_interval = 1.00*unit.picoseconds
    logging_interval = 100.00*unit.picoseconds
    simulation_time = 1000.*unit.picoseconds

    saving_steps = int(saving_interval/integration_timestep)
    logging_steps = int(logging_interval/integration_timestep)
    md_steps = int(simulation_time/integration_timestep)
    friction   = 5.0/unit.picoseconds
    integrator = mm.LangevinIntegrator(temperature, friction, integration_timestep)
    platform = mm.Platform.getPlatformByName('CPU')
    context = mm.Context(system, integrator, platform)
    initial_positions  = [[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]] * unit.nanometers
    context.setPositions(initial_positions)
    Lbox = 2.0
    v1 = [Lbox,0,0] * unit.nanometers
    v2 = [0,Lbox,0] * unit.nanometers
    v3 = [0,0,Lbox] * unit.nanometers
    context.setPeriodicBoxVectors(v1, v2, v3)

    fi = msm.thirds.openmm.forces.pin_atoms(context, selection=[1],
                                            force_constant = '5000 kilojoules/(mol*nanometers**2)',
                                            pbc=True)

    force = context.getSystem().getForce(0)
    f_name = force.getName()
    f_expression = force.getEnergyFunction()
    f_pbc = force.usesPeriodicBoundaryConditions()
    n_particles = force.getNumParticles()
    glob0_name = force.getGlobalParameterName(0)
    glob0_value = force.getGlobalParameterDefaultValue(0)
    per_particle = force.getParticleParameters(0)

    assert fi==0
    assert f_name=='CustomExternalForce'
    assert n_particles==1
    assert glob0_name=='k'
    assert np.isclose(glob0_value,5000)
    assert 1==per_particle[0]
    assert np.allclose(per_particle[1], [1,1,1])
    assert f_pbc==True
    assert f_expression=="0.5*k*periodicdistance(x, y, z, x0, y0, z0)^2"

def test_pin_atoms_2():

    system = mm.System()
    system.addParticle(atom.element.mass) # masa del átomo de argón
    system.addParticle(atom.element.mass) # masa del átomo de argón

    temperature = 300*unit.kelvin
    integration_timestep = 2.0*unit.femtoseconds
    saving_interval = 1.00*unit.picoseconds
    logging_interval = 100.00*unit.picoseconds
    simulation_time = 1000.*unit.picoseconds

    saving_steps = int(saving_interval/integration_timestep)
    logging_steps = int(logging_interval/integration_timestep)
    md_steps = int(simulation_time/integration_timestep)
    friction   = 5.0/unit.picoseconds
    integrator = mm.LangevinIntegrator(temperature, friction, integration_timestep)
    platform = mm.Platform.getPlatformByName('CPU')
    context = mm.Context(system, integrator, platform)
    initial_positions  = [[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]] * unit.nanometers
    context.setPositions(initial_positions)

    fi = msm.thirds.openmm.forces.pin_atoms(context, selection=[1],
                                            force_constant = '5000 kilojoules/(mol*nanometers**2)',
                                            pbc=False)

    force = context.getSystem().getForce(0)
    f_name = force.getName()
    f_expression = force.getEnergyFunction()
    f_pbc = force.usesPeriodicBoundaryConditions()
    n_particles = force.getNumParticles()
    glob0_name = force.getGlobalParameterName(0)
    glob0_value = force.getGlobalParameterDefaultValue(0)
    per_particle = force.getParticleParameters(0)

    assert fi==0
    assert f_name=='CustomExternalForce'
    assert n_particles==1
    assert glob0_name=='k'
    assert np.isclose(glob0_value,5000)
    assert 1==per_particle[0]
    assert np.allclose(per_particle[1], [1,1,1])
    assert f_pbc==False
    assert f_expression=="0.5*k*((x-x0)^2 + (y-y0)^2 + (z-z0)^2)"

def test_pin_atoms_3():

    system = mm.System()
    system.addParticle(atom.element.mass) # masa del átomo de argón
    system.addParticle(atom.element.mass) # masa del átomo de argón

    temperature = 300*unit.kelvin
    integration_timestep = 2.0*unit.femtoseconds
    saving_interval = 1.00*unit.picoseconds
    logging_interval = 100.00*unit.picoseconds
    simulation_time = 1000.*unit.picoseconds

    saving_steps = int(saving_interval/integration_timestep)
    logging_steps = int(logging_interval/integration_timestep)
    md_steps = int(simulation_time/integration_timestep)
    friction   = 5.0/unit.picoseconds
    integrator = mm.LangevinIntegrator(temperature, friction, integration_timestep)
    platform = mm.Platform.getPlatformByName('CPU')
    simulation = app.Simulation(topology, system, integrator, platform)
    initial_positions  = [[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]] * unit.nanometers
    simulation.context.setPositions(initial_positions)
    Lbox = 2.0
    v1 = [Lbox,0,0] * unit.nanometers
    v2 = [0,Lbox,0] * unit.nanometers
    v3 = [0,0,Lbox] * unit.nanometers
    simulation.context.setPeriodicBoxVectors(v1, v2, v3)

    fi = msm.thirds.openmm.forces.pin_atoms(simulation, selection='chain_name=="B"',
                                            force_constant = '5000 kilojoules/(mol*nanometers**2)',
                                            pbc=True)

    force = simulation.system.getForce(0)
    f_name = force.getName()
    f_expression = force.getEnergyFunction()
    f_pbc = force.usesPeriodicBoundaryConditions()
    n_particles = force.getNumParticles()
    glob0_name = force.getGlobalParameterName(0)
    glob0_value = force.getGlobalParameterDefaultValue(0)
    per_particle = force.getParticleParameters(0)

    assert fi==0
    assert f_name=='CustomExternalForce'
    assert n_particles==1
    assert glob0_name=='k'
    assert np.isclose(glob0_value,5000)
    assert 1==per_particle[0]
    assert np.allclose(per_particle[1], [1,1,1])
    assert f_pbc==True
    assert f_expression=="0.5*k*periodicdistance(x, y, z, x0, y0, z0)^2"

