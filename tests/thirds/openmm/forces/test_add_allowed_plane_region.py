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

def test_add_allowed_plane_region_1():

    system = mm.System()
    system.addParticle(atom.element.mass)
    fi = msm.thirds.openmm.forces.add_allowed_plane_region(system, point='[1,2,3] nm', normal_vector=[1,0,0],
                                                           width='0.5 nm',
                                                           force_constant = '5000 kilojoules/(mol*nm**2)',
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
    assert glob2_name=='px'
    assert np.isclose(glob0_value,5000)
    assert np.isclose(glob1_value,0.25)
    assert np.isclose(glob2_value,1.0)
    assert f_pbc==True
    assert f_expression== '0.5*Ka*q^2; q = max(0, d-wa); d = periodicdistance(x, 0, 0, px, 0, 0)'

def test_add_allowed_plane_region_2():

    system = mm.System()
    system.addParticle(atom.element.mass)
    fi = msm.thirds.openmm.forces.add_allowed_plane_region(system, point='[1,2,3] nm', normal_vector=[0,1,0],
                                                           width='0.5 nm',
                                                           force_constant = '5000 kilojoules/(mol*nm**2)',
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
    assert glob2_name=='py'
    assert np.isclose(glob0_value,5000)
    assert np.isclose(glob1_value,0.25)
    assert np.isclose(glob2_value,2.0)
    assert f_pbc==False
    assert f_expression== '0.5*Ka*q^2; q = max(0, d-wa); d = abs(y-py)'

def test_add_allowed_plane_region_3():

    system = mm.System()
    system.addParticle(atom.element.mass)

    temperature = 300*unit.kelvin
    integration_timestep = 2.0*unit.femtoseconds
    friction   = 5.0/unit.picoseconds
    integrator = mm.LangevinIntegrator(temperature, friction, integration_timestep)
    platform = mm.Platform.getPlatformByName('CPU')
    context = mm.Context(system, integrator, platform)

    fi = msm.thirds.openmm.forces.add_allowed_plane_region(context, point='[1,2,3] nm', normal_vector=[1,1,1],
                                                           width='0.5 nm',
                                                           force_constant = '5000 kilojoules/(mol*nm**2)',
                                                           pbc=True)

    force = context.getSystem().getForce(0)
    f_name = force.getName()
    f_expression = force.getEnergyFunction()
    f_pbc = force.usesPeriodicBoundaryConditions()
    n_particles = force.getNumParticles()
    glob0_name = force.getGlobalParameterName(0)
    glob1_name = force.getGlobalParameterName(1)
    glob2_name = force.getGlobalParameterName(2)
    glob3_name = force.getGlobalParameterName(3)
    glob4_name = force.getGlobalParameterName(4)
    glob5_name = force.getGlobalParameterName(5)
    glob6_name = force.getGlobalParameterName(6)
    glob7_name = force.getGlobalParameterName(7)
    glob0_value = force.getGlobalParameterDefaultValue(0)
    glob1_value = force.getGlobalParameterDefaultValue(1)
    glob2_value = force.getGlobalParameterDefaultValue(2)
    glob3_value = force.getGlobalParameterDefaultValue(3)
    glob4_value = force.getGlobalParameterDefaultValue(4)
    glob5_value = force.getGlobalParameterDefaultValue(5)
    glob6_value = force.getGlobalParameterDefaultValue(6)
    glob7_value = force.getGlobalParameterDefaultValue(7)


    aux = 1.0/np.sqrt(3.0)

    assert fi==0
    assert f_name=='CustomExternalForce'
    assert n_particles==1
    assert glob0_name=='Ka'
    assert glob1_name=='wa'
    assert glob2_name=='px'
    assert glob3_name=='py'
    assert glob4_name=='pz'
    assert glob5_name=='vx'
    assert glob6_name=='vy'
    assert glob7_name=='vz'
    assert np.isclose(glob0_value,5000)
    assert np.isclose(glob1_value,0.25)
    assert np.isclose(glob2_value,1)
    assert np.isclose(glob3_value,2)
    assert np.isclose(glob4_value,3)
    assert np.isclose(glob5_value,aux)
    assert np.isclose(glob6_value,aux)
    assert np.isclose(glob7_value,aux)
    assert f_pbc==True
    assert f_expression== (
                '0.5*Ka*q^2; '
                'q = max(0, d-wa); '
                'd = abs(periodicdistance(a, b, c, 0, 0, 0)); '
                'a = u*vx; '
                'b = u*vy; '
                'c = u*vz; '
                'u = (x-px)*vx+(y-py)*vy+(z-pz)*vz;'
            )

def test_add_allowed_plane_region_4():

    system = mm.System()
    system.addParticle(atom.element.mass)

    temperature = 300*unit.kelvin
    integration_timestep = 2.0*unit.femtoseconds
    friction   = 5.0/unit.picoseconds
    integrator = mm.LangevinIntegrator(temperature, friction, integration_timestep)
    platform = mm.Platform.getPlatformByName('CPU')

    simulation = app.Simulation(topology, system, integrator, platform)


    fi = msm.thirds.openmm.forces.add_allowed_plane_region(simulation, point='[1,2,3] nm', normal_vector=[1,1,1],
                                                           width='0.5 nm',
                                                           force_constant = '5000 kilojoules/(mol*nm**2)',
                                                           pbc=False)

    force = simulation.context.getSystem().getForce(0)
    f_name = force.getName()
    f_expression = force.getEnergyFunction()
    f_pbc = force.usesPeriodicBoundaryConditions()
    n_particles = force.getNumParticles()
    glob0_name = force.getGlobalParameterName(0)
    glob1_name = force.getGlobalParameterName(1)
    glob2_name = force.getGlobalParameterName(2)
    glob3_name = force.getGlobalParameterName(3)
    glob4_name = force.getGlobalParameterName(4)
    glob5_name = force.getGlobalParameterName(5)
    glob6_name = force.getGlobalParameterName(6)
    glob7_name = force.getGlobalParameterName(7)
    glob0_value = force.getGlobalParameterDefaultValue(0)
    glob1_value = force.getGlobalParameterDefaultValue(1)
    glob2_value = force.getGlobalParameterDefaultValue(2)
    glob3_value = force.getGlobalParameterDefaultValue(3)
    glob4_value = force.getGlobalParameterDefaultValue(4)
    glob5_value = force.getGlobalParameterDefaultValue(5)
    glob6_value = force.getGlobalParameterDefaultValue(6)
    glob7_value = force.getGlobalParameterDefaultValue(7)


    aux = 1.0/np.sqrt(3.0)

    assert fi==0
    assert f_name=='CustomExternalForce'
    assert n_particles==1
    assert glob0_name=='Ka'
    assert glob1_name=='wa'
    assert glob2_name=='px'
    assert glob3_name=='py'
    assert glob4_name=='pz'
    assert glob5_name=='vx'
    assert glob6_name=='vy'
    assert glob7_name=='vz'
    assert np.isclose(glob0_value,5000)
    assert np.isclose(glob1_value,0.25)
    assert np.isclose(glob2_value,1)
    assert np.isclose(glob3_value,2)
    assert np.isclose(glob4_value,3)
    assert np.isclose(glob5_value,aux)
    assert np.isclose(glob6_value,aux)
    assert np.isclose(glob7_value,aux)
    assert f_pbc==False
    assert f_expression== (
                '0.5*Ka*q^2; '
                'q = max(0, d-wa); '
                'd = abs((x-px)*vx+(y-py)*vy+(z-pz)*vz);'
            )

