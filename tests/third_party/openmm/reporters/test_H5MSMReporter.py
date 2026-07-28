"""
Unit and regression test for the copy module of the molsysmt package.
"""

import molsysmt as msm
from molsysmt import pyunitwizard as puw
import numpy as np
import openmm as mm
from openmm import app
from openmm import unit
import pytest


@pytest.mark.parametrize(
    ('selection', 'expected_n_atoms'),
    [
        ('all', 304),
        ([0, 1, 2], 3),
    ],
)
def test_H5MSMReporter_1(tmp_path, selection, expected_n_atoms):

    modeller = msm.convert(msm.systems['Trp-Cage']['1l2y.h5msm'], to_form='openmm.Modeller', structure_indices=0)
    forcefield = app.ForceField("amber14-all.xml", "amber14/tip3p.xml")
    system = forcefield.createSystem(modeller.topology, nonbondedMethod=app.NoCutoff, constraints=app.HBonds)
    integrator = mm.LangevinIntegrator(300*unit.kelvin, 1.0/unit.picosecond, 2.0*unit.femtoseconds)
    platform = mm.Platform.getPlatformByName('CPU')
    simulation = app.Simulation(modeller.topology, system, integrator, platform)
    simulation.context.setPositions(modeller.positions)
    simulation.minimizeEnergy()
    simulation.context.setVelocitiesToTemperature(300*unit.kelvin)
    output_file = str(tmp_path / 'test.h5msm')
    tqdm_reporter = msm.thirds.openmm.reporters.H5MSMReporter(output_file, 100, 1000, selection=selection,
                    topology=True, time=True,
                    box=True, coordinates=True, velocities=True, potentialEnergy=True, kineticEnergy=True,
                    temperature=True)
    simulation.reporters.append(tqdm_reporter)
    simulation.step(1000)
    tqdm_reporter.close()
    molsys = msm.convert(output_file)
    n_atoms, n_structures = msm.get(molsys, n_atoms=True, n_structures=True)
    assert n_atoms == expected_n_atoms
    assert n_structures == 11
    assert np.array_equal(
        molsys.structures.structure_id,
        np.arange(0, 1001, 100),
    )
    assert molsys.structures.time.shape == (11,)
    assert molsys.structures.box.shape == (11, 3, 3)

    repeated = msm.convert(
        output_file,
        to_form='molsysmt.MolSys',
        structure_indices=[10, 0, 10],
    )
    assert np.array_equal(
        repeated.structures.structure_id,
        [1000, 0, 1000],
    )
    assert repeated.structures.time.shape == (3,)
    assert repeated.structures.box.shape == (3, 3, 3)
