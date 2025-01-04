"""
Unit and regression test for the copy module of the molsysmt package.
"""

import molsysmt as msm
from molsysmt import pyunitwizard as puw
import numpy as np
import openmm as mm
from openmm import app
from openmm import unit

def test_TrajectoryDictReporter_1():

    reporter = msm.thirds.openmm.reporters.TrajectoryDictReporter(10)

    assert reporter._reportInterval == 10
    assert reporter._needsPositions is True
    assert reporter._needsVelocities is False
    assert reporter._needsEnergy is False
    assert 'time' in reporter._dict
    assert 'coordinates' in reporter._dict
    assert 'temperature' not in reporter._dict

def test_TrajectoryDictReporter_2():

    modeller = msm.convert(msm.systems['Trp-Cage']['1l2y.h5msm'], to_form='openmm.Modeller', structure_indices=0)
    forcefield = app.ForceField("amber14-all.xml", "amber14/tip3p.xml")
    system = forcefield.createSystem(modeller.topology, nonbondedMethod=app.NoCutoff, constraints=app.HBonds)
    integrator = mm.LangevinIntegrator(300*unit.kelvin, 1.0/unit.picosecond, 2.0*unit.femtoseconds)
    platform = mm.Platform.getPlatformByName('CPU')
    simulation = app.Simulation(modeller.topology, system, integrator, platform)
    simulation.context.setPositions(modeller.positions)
    simulation.minimizeEnergy()
    simulation.context.setVelocitiesToTemperature(300*unit.kelvin)
    tqdm_reporter = msm.thirds.openmm.reporters.TrajectoryDictReporter(100, time=True, coordinates=True,
                    velocities=True, potentialEnergy=True, kineticEnergy=True, totalEnergy=True, temperature=True,
                    box=True)
    simulation.reporters.append(tqdm_reporter)
    simulation.step(1000)
    traj_dict = tqdm_reporter.finalize()
    assert len(traj_dict['time'])==11
    assert 'coordinates' in traj_dict
    assert 'velocities' in traj_dict
    assert 'potential_energy' in traj_dict
    assert 'kinetic_energy' in traj_dict
    assert 'total_energy' in traj_dict
    assert 'temperature' in traj_dict
    assert 'box' in traj_dict

