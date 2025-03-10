"""
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np
from openmm import app
import openmm as mm
from openmm import unit

def test_get_forces_1():


    molsys = msm.convert(msm.systems['Trp-Cage']['1l2y.h5msm'], structure_indices=0)
    openmm_topology = msm.convert(molsys, to_form='openmm.Topology')
    positions = msm.get(molsys, element='atom', coordinates=True)
    positions = msm.pyunitwizard.convert(positions[0], to_form='openmm.unit')
    
    forcefield = app.ForceField("amber14-all.xml", "amber14/tip3p.xml")
    system = forcefield.createSystem(openmm_topology, nonbondedMethod=app.NoCutoff,
                                     constraints=app.HBonds)
    
    integrator = mm.LangevinIntegrator(300*unit.kelvin, 1/unit.picosecond, 1*unit.femtosecond)
    platform = mm.Platform.getPlatform('CPU')
    
    context = mm.Context(system, integrator, platform)
    context.setPositions(positions)

    forces = msm.molecular_mechanics.get_forces(context)
    forces_norm = msm.molecular_mechanics.get_forces(context, magnitude=True)

    assert forces.shape==(304,3)
    assert puw.get_unit(forces) == puw.unit('kilojoule/mole/nanometer')
    assert forces_norm.shape==(304,)
    assert puw.get_unit(forces_norm) == puw.unit('kilojoule/mole/nanometer')
