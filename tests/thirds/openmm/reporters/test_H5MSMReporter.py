"""
Unit and regression test for the copy module of the molsysmt package.
"""

import molsysmt as msm
from molsysmt import pyunitwizard as puw
import numpy as np
import openmm as mm
from openmm import app
from openmm import unit
import os

def test_H5MSMReporter_1():

    modeller = msm.convert(msm.systems['Trp-Cage']['1l2y.h5msm'], to_form='openmm.Modeller', structure_indices=0)
    forcefield = app.ForceField("amber14-all.xml", "amber14/tip3p.xml")
    system = forcefield.createSystem(modeller.topology, nonbondedMethod=app.NoCutoff, constraints=app.HBonds)
    integrator = mm.LangevinIntegrator(300*unit.kelvin, 1.0/unit.picosecond, 2.0*unit.femtoseconds)
    platform = mm.Platform.getPlatformByName('CPU')
    simulation = app.Simulation(modeller.topology, system, integrator, platform)
    simulation.context.setPositions(modeller.positions)
    simulation.minimizeEnergy()
    simulation.context.setVelocitiesToTemperature(300*unit.kelvin)
    tqdm_reporter = msm.thirds.openmm.reporters.H5MSMReporter('test.h5msm', 100, 1000)
    simulation.reporters.append(tqdm_reporter)
    simulation.step(1000)
    tqdm_reporter.close()
    molsys = msm.convert('test.h5msm')
    n_atoms, n_structures = msm.get(molsys, n_atoms=True, n_structures=True)
    assert n_atoms == 304
    assert n_structures == 11
    os.remove('test.h5msm')

