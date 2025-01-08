"""
Unit and regression test for the add_allowed_z_region function of the molsysmt module thirds.openmm.forces
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

def test_add_allowed_z_region_1():

    system = mm.System()
    system.addParticle(atom.element.mass)
    fi = msm.thirds.openmm.forces.add_allowed_z_region(system, z0='1.0 nm', width='0.5 nm',
                                                       force_constant = '5000 kilojoules/(mol*angstroms**2)',
                                                       pbc=True)
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
    assert glob0_name=='Ka'
    assert glob1_name=='wa'
    assert glob2_name=='za'
    assert np.isclose(glob0_value,500000)
    assert np.isclose(glob1_value,0.25)
    assert np.isclose(glob2_value,1.0)
    assert f_pbc==True
    assert f_expression== '0.5*Ka*q^2; q = max(0, d-wa); d = periodicdistance(0, 0, z, 0, 0, za)'

def test_add_allowed_z_region_2():

    system = mm.System()
    system.addParticle(atom.element.mass)
    fi = msm.thirds.openmm.forces.add_allowed_z_region(system, z0='1.0 nm', width='0.5 nm',
                                                       force_constant = '5000 kilojoules/(mol*angstroms**2)',
                                                       pbc=False)
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
    assert glob0_name=='Ka'
    assert glob1_name=='wa'
    assert glob2_name=='za'
    assert np.isclose(glob0_value,500000)
    assert np.isclose(glob1_value,0.25)
    assert np.isclose(glob2_value,1.0)
    assert f_pbc==False
    assert f_expression== '0.5*Ka*q^2; q = max(0, d-wa); d = abs(z-za)'

def test_add_allowed_z_region_3():

    system = mm.System()
    system.addParticle(atom.element.mass)

    temperature = 300*unit.kelvin
    integration_timestep = 2.0*unit.femtoseconds
    friction   = 5.0/unit.picoseconds
    integrator = mm.LangevinIntegrator(temperature, friction, integration_timestep)
    platform = mm.Platform.getPlatformByName('CPU')
    context = mm.Context(system, integrator, platform)

    fi = msm.thirds.openmm.forces.add_allowed_z_region(context, z0='1.0 nm', width='0.5 nm',
                                                       force_constant = '5000 kilojoules/(mol*angstroms**2)',
                                                       pbc=True)
    force = context.getSystem().getForce(0)
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
    assert glob0_name=='Ka'
    assert glob1_name=='wa'
    assert glob2_name=='za'
    assert np.isclose(glob0_value,500000)
    assert np.isclose(glob1_value,0.25)
    assert np.isclose(glob2_value,1.0)
    assert f_pbc==True
    assert f_expression== '0.5*Ka*q^2; q = max(0, d-wa); d = periodicdistance(0, 0, z, 0, 0, za)'

def test_add_allowed_z_region_4():

    system = mm.System()
    system.addParticle(atom.element.mass)

    temperature = 300*unit.kelvin
    integration_timestep = 2.0*unit.femtoseconds
    friction   = 5.0/unit.picoseconds
    integrator = mm.LangevinIntegrator(temperature, friction, integration_timestep)
    platform = mm.Platform.getPlatformByName('CPU')


    simulation = app.Simulation(topology, system, integrator, platform)

    fi = msm.thirds.openmm.forces.add_allowed_z_region(simulation, z0='1.0 nm', width='0.5 nm',
                                                       force_constant = '5000 kilojoules/(mol*angstroms**2)',
                                                       pbc=True)
    force = simulation.context.getSystem().getForce(0)
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
    assert glob0_name=='Ka'
    assert glob1_name=='wa'
    assert glob2_name=='za'
    assert np.isclose(glob0_value,500000)
    assert np.isclose(glob1_value,0.25)
    assert np.isclose(glob2_value,1.0)
    assert f_pbc==True
    assert f_expression== '0.5*Ka*q^2; q = max(0, d-wa); d = periodicdistance(0, 0, z, 0, 0, za)'

