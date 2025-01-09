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

def test_add_plane_harmonic_restraint_1():

    system = mm.System()
    system.addParticle(atom.element.mass)
    fi = msm.thirds.openmm.forces.add_plane_harmonic_restraint(system, selection=[0],
                                            force_constant = '5000 kilojoules/(mol*nanometers**2)',
                                            point='[0,0,0] nm', vector=[0,0,1], pbc=True)

    force = system.getForce(0)
    f_name = force.getName()
    f_expression = force.getEnergyFunction()
    f_pbc = force.usesPeriodicBoundaryConditions()
    n_particles = force.getNumParticles()
    glob0_name = force.getGlobalParameterName(0)
    glob0_value = force.getGlobalParameterDefaultValue(0)
    glob1_name = force.getGlobalParameterName(1)
    glob1_value = force.getGlobalParameterDefaultValue(1)
    glob2_name = force.getGlobalParameterName(2)
    glob2_value = force.getGlobalParameterDefaultValue(2)
    glob3_name = force.getGlobalParameterName(3)
    glob3_value = force.getGlobalParameterDefaultValue(3)
    glob4_name = force.getGlobalParameterName(4)
    glob4_value = force.getGlobalParameterDefaultValue(4)
    glob5_name = force.getGlobalParameterName(5)
    glob5_value = force.getGlobalParameterDefaultValue(5)
    glob6_name = force.getGlobalParameterName(6)
    glob6_value = force.getGlobalParameterDefaultValue(6)


    assert fi==0
    assert f_name=='CustomExternalForce'
    assert n_particles==1
    assert glob0_name=='k'
    assert np.isclose(glob0_value,5000)
    assert glob1_name=='vx'
    assert np.isclose(glob1_value,0)
    assert glob2_name=='vy'
    assert np.isclose(glob2_value,0)
    assert glob3_name=='vz'
    assert np.isclose(glob3_value,1)
    assert glob4_name=='px'
    assert np.isclose(glob4_value,0)
    assert glob5_name=='py'
    assert np.isclose(glob5_value,0)
    assert glob6_name=='pz'
    assert np.isclose(glob6_value,0)
    assert f_pbc==True
    assert f_expression== (
            "0.5 * k * (r^2); "
            "r = abs(periodicdistance(a, b, c, 0, 0, 0)); "
            "a = u * vx; "
            "b = u * vy; "
            "c = u * vz; "
            "u = (x - px) * vx + (y - py) * vy + (z - pz) * vz;"
        )

def test_add_plane_harmonic_restraint_2():

    system = mm.System()
    system.addParticle(atom.element.mass)

    temperature = 300*unit.kelvin
    integration_timestep = 2.0*unit.femtoseconds
    friction   = 5.0/unit.picoseconds
    integrator = mm.LangevinIntegrator(temperature, friction, integration_timestep)
    platform = mm.Platform.getPlatformByName('CPU')
    context = mm.Context(system, integrator, platform)

    fi = msm.thirds.openmm.forces.add_plane_harmonic_restraint(context, selection=[0],
                                            force_constant = '5000 kilojoules/(mol*nanometers**2)',
                                            point='[0,0,0] nm', vector=[0,0,1], pbc=False)

    force = context.getSystem().getForce(0)
    f_name = force.getName()
    f_expression = force.getEnergyFunction()
    f_pbc = force.usesPeriodicBoundaryConditions()
    n_particles = force.getNumParticles()
    glob0_name = force.getGlobalParameterName(0)
    glob0_value = force.getGlobalParameterDefaultValue(0)
    glob1_name = force.getGlobalParameterName(1)
    glob1_value = force.getGlobalParameterDefaultValue(1)
    glob2_name = force.getGlobalParameterName(2)
    glob2_value = force.getGlobalParameterDefaultValue(2)
    glob3_name = force.getGlobalParameterName(3)
    glob3_value = force.getGlobalParameterDefaultValue(3)
    glob4_name = force.getGlobalParameterName(4)
    glob4_value = force.getGlobalParameterDefaultValue(4)
    glob5_name = force.getGlobalParameterName(5)
    glob5_value = force.getGlobalParameterDefaultValue(5)
    glob6_name = force.getGlobalParameterName(6)
    glob6_value = force.getGlobalParameterDefaultValue(6)

    assert fi==0
    assert f_name=='CustomExternalForce'
    assert n_particles==1
    assert glob0_name=='k'
    assert np.isclose(glob0_value,5000)
    assert glob1_name=='vx'
    assert np.isclose(glob1_value,0)
    assert glob2_name=='vy'
    assert np.isclose(glob2_value,0)
    assert glob3_name=='vz'
    assert np.isclose(glob3_value,1)
    assert glob4_name=='px'
    assert np.isclose(glob4_value,0)
    assert glob5_name=='py'
    assert np.isclose(glob5_value,0)
    assert glob6_name=='pz'
    assert np.isclose(glob6_value,0)
    assert f_pbc==False
    assert f_expression== (
            "0.5 * k * (a^2+b^2+c^2); "
            "a = u * vx; "
            "b = u * vy; "
            "c = u * vz; "
            "u = (x - px) * vx + (y - py) * vy + (z - pz) * vz;"
        )

def test_add_plane_harmonic_restraint_3():

    system = mm.System()
    system.addParticle(atom.element.mass)

    temperature = 300*unit.kelvin
    integration_timestep = 2.0*unit.femtoseconds
    friction   = 5.0/unit.picoseconds
    integrator = mm.LangevinIntegrator(temperature, friction, integration_timestep)
    platform = mm.Platform.getPlatformByName('CPU')
    simulation = app.Simulation(topology, system, integrator, platform)
    initial_positions  = [[1.0, 2.0, 3.0]] * unit.nanometers
    simulation.context.setPositions(initial_positions)
    Lbox = 2.0
    v1 = [Lbox,0,0] * unit.nanometers
    v2 = [0,Lbox,0] * unit.nanometers
    v3 = [0,0,Lbox] * unit.nanometers
    simulation.context.setPeriodicBoxVectors(v1, v2, v3)

    fi = msm.thirds.openmm.forces.add_plane_harmonic_restraint(simulation, selection=[0],
                                            force_constant = '5000 kilojoules/(mol*nanometers**2)',
                                            vector=[0,0,1], pbc=True)

    force = system.getForce(0)
    f_name = force.getName()
    f_expression = force.getEnergyFunction()
    f_pbc = force.usesPeriodicBoundaryConditions()
    n_particles = force.getNumParticles()
    glob0_name = force.getGlobalParameterName(0)
    glob0_value = force.getGlobalParameterDefaultValue(0)
    glob1_name = force.getGlobalParameterName(1)
    glob1_value = force.getGlobalParameterDefaultValue(1)
    glob2_name = force.getGlobalParameterName(2)
    glob2_value = force.getGlobalParameterDefaultValue(2)
    glob3_name = force.getGlobalParameterName(3)
    glob3_value = force.getGlobalParameterDefaultValue(3)
    per_particle = force.getParticleParameters(0)

    assert fi==0
    assert f_name=='CustomExternalForce'
    assert n_particles==1
    assert glob0_name=='k'
    assert np.isclose(glob0_value,5000)
    assert glob1_name=='vx'
    assert np.isclose(glob1_value,0)
    assert glob2_name=='vy'
    assert np.isclose(glob2_value,0)
    assert glob3_name=='vz'
    assert np.isclose(glob3_value,1)
    assert 0==per_particle[0]
    assert np.allclose(per_particle[1], [1,2,3])
    assert f_pbc==True
    assert f_expression== (
            "0.5 * k * (r^2); "
            "r = abs(periodicdistance(a, b, c, 0, 0, 0)); "
            "a = u * vx; "
            "b = u * vy; "
            "c = u * vz; "
            "u = (x - px) * vx + (y - py) * vy + (z - pz) * vz;"
        )

