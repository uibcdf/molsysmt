"""
Unit and regression test for the copy module of the molsysmt package.
"""

import molsysmt as msm
from molsysmt import pyunitwizard as puw
import numpy as np
import openmm as mm
from openmm import app
from openmm import unit

def test_TQDMReporter_1():

    reporter = msm.thirds.openmm.reporters.TQDMReporter(10, 100, potential_energy=True, temperature=False, volume=True)

    assert reporter._report_interval == 10
    assert reporter._total_n_steps == 100
    assert reporter._with_potential_energy is True
    assert reporter._with_temperature is False
    assert reporter._with_volume is True

def test_TQDMReporter_2():

    modeller = msm.convert(msm.systems['Trp-Cage']['1l2y.h5msm'], to_form='openmm.Modeller', structure_indices=0)
    forcefield = app.ForceField("amber14-all.xml", "amber14/tip3p.xml")
    system = forcefield.createSystem(modeller.topology, nonbondedMethod=app.NoCutoff, constraints=app.HBonds)
    integrator = mm.LangevinIntegrator(300*unit.kelvin, 1.0/unit.picosecond, 2.0*unit.femtoseconds)
    platform = mm.Platform.getPlatformByName('CPU')
    simulation = app.Simulation(modeller.topology, system, integrator, platform)
    simulation.context.setPositions(modeller.positions)
    simulation.minimizeEnergy()
    simulation.context.setVelocitiesToTemperature(300*unit.kelvin)
    tqdm_reporter = msm.thirds.openmm.reporters.TQDMReporter(100,1000)
    simulation.reporters.append(tqdm_reporter)
    simulation.step(1000)
    assert np.isclose(puw.get_value(tqdm_reporter._end_md_time, to_unit='ps'), 2.0)
