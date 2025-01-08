"""
Unit and regression test for the add_point_harmonic_restraint function of the molsysmt module thirds.openmm.forces
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

def test_add_point_harmonic_restraint_1():

    system = mm.System()
    system.addParticle(atom.element.mass)
    fi = msm.thirds.openmm.forces.add_point_harmonic_restraint(system, selection=[0],
                                            force_constant = '5000 kilojoules/(mol*nanometers**2)',
                                            point='[0,0,0] nm', pbc=True)

    force = system.getForce(0)
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
    assert 0==per_particle[0]
    assert np.allclose(per_particle[0], [0,0,0])
    assert f_pbc==True
    assert f_expression=="0.5*k*periodicdistance(x, y, z, x0, y0, z0)^2"


def test_add_point_harmonic_restraint_2():

    system = mm.System()
    system.addParticle(atom.element.mass)
    fi = msm.thirds.openmm.forces.add_point_harmonic_restraint(system, selection=[0],
                                            force_constant = '5000 kilojoules/(mol*nanometers**2)',
                                            point='[0,0,0] nm', pbc=False)

    force = system.getForce(0)
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
    assert 0==per_particle[0]
    assert np.allclose(per_particle[0], [0,0,0])
    assert f_pbc==False
    assert f_expression=="0.5*k*((x-x0)^2 + (y-y0)^2 + (z-z0)^2)"

def test_add_point_harmonic_restraint_3():

    system = mm.System()
    system.addParticle(atom.element.mass)


    temperature = 300*unit.kelvin
    integration_timestep = 2.0*unit.femtoseconds
    friction   = 5.0/unit.picoseconds
    integrator = mm.LangevinIntegrator(temperature, friction, integration_timestep)
    platform = mm.Platform.getPlatformByName('CPU')
    context = mm.Context(system, integrator, platform)

    fi = msm.thirds.openmm.forces.add_point_harmonic_restraint(context, selection=[0],
                                            force_constant = '5000 kilojoules/(mol*nanometers**2)',
                                            point='[0,0,0] nm', pbc=False)

    force = system.getForce(0)
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
    assert 0==per_particle[0]
    assert np.allclose(per_particle[0], [0,0,0])
    assert f_pbc==False
    assert f_expression=="0.5*k*((x-x0)^2 + (y-y0)^2 + (z-z0)^2)"

def test_add_point_harmonic_restraint_4():

    system = mm.System()
    system.addParticle(atom.element.mass)

    temperature = 300*unit.kelvin
    integration_timestep = 2.0*unit.femtoseconds
    friction   = 5.0/unit.picoseconds
    integrator = mm.LangevinIntegrator(temperature, friction, integration_timestep)
    platform = mm.Platform.getPlatformByName('CPU')
    simulation = app.Simulation(topology, system, integrator, platform)
    initial_positions  = [[0.0, 0.0, 0.0]] * unit.nanometers
    simulation.context.setPositions(initial_positions)
    Lbox = 2.0
    v1 = [Lbox,0,0] * unit.nanometers
    v2 = [0,Lbox,0] * unit.nanometers
    v3 = [0,0,Lbox] * unit.nanometers
    simulation.context.setPeriodicBoxVectors(v1, v2, v3)

    fi = msm.thirds.openmm.forces.add_point_harmonic_restraint(simulation, selection=[0],
                                            force_constant = '5000 kilojoules/(mol*nanometers**2)',
                                            pbc=True)

    force = system.getForce(0)
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
    assert 0==per_particle[0]
    assert np.allclose(per_particle[0], [0,0,0])
    assert f_pbc==True
    assert f_expression=="0.5*k*periodicdistance(x, y, z, x0, y0, z0)^2"

