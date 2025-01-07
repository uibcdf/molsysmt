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

def test_add_constant_force_1():

    system = mm.System()
    system.addParticle(atom.element.mass) # masa del átomo de argón
    fi = msm.thirds.openmm.forces.add_constant_force(system, selection=0, force='[5000,0,0] kilojoules/(mol*nm)')
    force = system.getForce(0)
    f_name = force.getName()
    f_expression = force.getEnergyFunction()
    f_pbc = force.usesPeriodicBoundaryConditions()
    n_particles = force.getNumParticles()
    glob0_name = force.getGlobalParameterName(0)
    glob1_name = force.getGlobalParameterName(1)
    glob2_name = force.getGlobalParameterName(2)
    glob0_value = force.getGlobalParameterDefaultValue(0)
    glob1_value = force.getGlobalParameterDefaultValue(1)
    glob2_value = force.getGlobalParameterDefaultValue(2)


    assert fi==0
    assert f_name=='CustomExternalForce'
    assert n_particles==1
    assert glob0_name=='px'
    assert glob1_name=='py'
    assert glob2_name=='pz'
    assert np.isclose(glob0_value,5000)
    assert np.isclose(glob1_value,0)
    assert np.isclose(glob2_value,0)
    assert f_pbc==False
    assert f_expression=="-(px*x+py*y+pz*z)"

def test_add_constant_force_2():

    system = mm.System()
    system.addParticle(atom.element.mass) # masa del átomo de argón

    temperature = 300*unit.kelvin
    integration_timestep = 2.0*unit.femtoseconds
    friction   = 5.0/unit.picoseconds
    integrator = mm.LangevinIntegrator(temperature, friction, integration_timestep)
    platform = mm.Platform.getPlatformByName('CPU')
    context = mm.Context(system, integrator, platform)

    fi = msm.thirds.openmm.forces.add_constant_force(context, selection=0, force='[5000,0,0] kilojoules/(mol*nm)')
    force = system.getForce(0)
    f_name = force.getName()
    f_expression = force.getEnergyFunction()
    f_pbc = force.usesPeriodicBoundaryConditions()
    n_particles = force.getNumParticles()
    glob0_name = force.getGlobalParameterName(0)
    glob1_name = force.getGlobalParameterName(1)
    glob2_name = force.getGlobalParameterName(2)
    glob0_value = force.getGlobalParameterDefaultValue(0)
    glob1_value = force.getGlobalParameterDefaultValue(1)
    glob2_value = force.getGlobalParameterDefaultValue(2)


    assert fi==0
    assert f_name=='CustomExternalForce'
    assert n_particles==1
    assert glob0_name=='px'
    assert glob1_name=='py'
    assert glob2_name=='pz'
    assert np.isclose(glob0_value,5000)
    assert np.isclose(glob1_value,0)
    assert np.isclose(glob2_value,0)
    assert f_pbc==False
    assert f_expression=="-(px*x+py*y+pz*z)"

def test_add_constant_force_3():

    system = mm.System()
    system.addParticle(atom.element.mass) # masa del átomo de argón

    temperature = 300*unit.kelvin
    integration_timestep = 2.0*unit.femtoseconds
    friction   = 5.0/unit.picoseconds
    integrator = mm.LangevinIntegrator(temperature, friction, integration_timestep)
    platform = mm.Platform.getPlatformByName('CPU')


    simulation = app.Simulation(topology, system, integrator, platform)

    fi = msm.thirds.openmm.forces.add_constant_force(simulation, selection=0, force='[5000,0,0] kilojoules/(mol*nm)')
    force = system.getForce(0)
    f_name = force.getName()
    f_expression = force.getEnergyFunction()
    f_pbc = force.usesPeriodicBoundaryConditions()
    n_particles = force.getNumParticles()
    glob0_name = force.getGlobalParameterName(0)
    glob1_name = force.getGlobalParameterName(1)
    glob2_name = force.getGlobalParameterName(2)
    glob0_value = force.getGlobalParameterDefaultValue(0)
    glob1_value = force.getGlobalParameterDefaultValue(1)
    glob2_value = force.getGlobalParameterDefaultValue(2)

    assert fi==0
    assert f_name=='CustomExternalForce'
    assert n_particles==1
    assert glob0_name=='px'
    assert glob1_name=='py'
    assert glob2_name=='pz'
    assert np.isclose(glob0_value,5000)
    assert np.isclose(glob1_value,0)
    assert np.isclose(glob2_value,0)
    assert f_pbc==False
    assert f_expression=="-(px*x+py*y+pz*z)"

