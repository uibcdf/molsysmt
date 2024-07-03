import molsysmt as msm
import os
import openmm as mm
from openmm import app
from openmm import unit
from sys import stdout
from mdtraj.reporters import HDF5Reporter
from pathlib import Path
import shutil

data_dir = Path('../.')

# Purge

files_to_be_purged = [
        'pdb/1vii.pdb',
        'h5msm/chicken_villin_HP35.h5msm',
        'h5msm/chicken_villin_HP35_solvated.h5msm',
        'dcd/traj_chicken_villin_HP35.dcd',
        'h5/traj_chicken_villin_HP35.h5',
        'h5msm/traj_chicken_villin_HP35.h5msm',
        ]

for filename in files_to_be_purged:
    filepath = Path(data_dir, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)


# Make

# 1vii pdb and mmtf files
print('Protein Data Bank files...')
msm.convert('pdb_id:1vii', to_form='1vii.pdb')
msm.convert('pdb_id:1vii', to_form='1vii.bcif')
msm.convert('pdb_id:1vii', to_form='1vii.bcif.gz')
shutil.move('1vii.pdb', Path(data_dir, 'pdb/1vii.pdb'))
shutil.move('1vii.bcif', Path(data_dir, 'bcif/1vii.bcif'))
shutil.move('1vii.bcif.gz', Path(data_dir, 'bcif_gz/1vii.bcif.gz'))


# vacuum
print('Vacuum system in h5msm file...')
molsys = msm.convert('1VII', to_form='molsysmt.MolSys')
molsys = msm.basic.remove(molsys, selection='group_type==["water", "ion"]')
molsys = msm.basic.remove(molsys, selection='atom_type=="H"')
molsys = msm.build.add_missing_terminal_cappings(molsys, N_terminal='ACE', C_terminal='NME')
molsys = msm.build.add_missing_hydrogens(molsys, pH=7.4)
molsys = msm.molecular_mechanics.potential_energy_minimization(molsys)
_ = msm.convert(molsys, to_form='chicken_villin_HP35.h5msm')
shutil.move('chicken_villin_HP35.h5msm', Path(data_dir, 'h5msm/chicken_villin_HP35.h5msm'))


# solvated
print('Solvated system in h5msm file...')
molsys = msm.build.solvate(molsys, 
                   box_shape='truncated octahedral', clearance='14.0 angstroms',
                   to_form='molsysmt.MolSys')
_ = msm.convert(molsys, to_form='chicken_villin_HP35_solvated.h5msm')
shutil.move('chicken_villin_HP35_solvated.h5msm', Path(data_dir, 'h5msm/chicken_villin_HP35_solvated.h5msm'))


# simulation
print('Trajectory files...')
modeller = msm.convert(molsys, to_form='openmm.Modeller')
forcefield = app.ForceField("amber14-all.xml", "amber14/tip3p.xml")
system = forcefield.createSystem(modeller.topology, nonbondedMethod=app.PME, nonbondedCutoff=1.2*unit.nanometer, constraints=app.HBonds)
integrator = mm.LangevinIntegrator(300*unit.kelvin, 1.0/unit.picosecond, 2.0*unit.femtoseconds)
platform = mm.Platform.getPlatformByName('CUDA')
simulation = app.Simulation(modeller.topology, system, integrator, platform)
simulation.context.setPositions(modeller.positions)
simulation.minimizeEnergy()
simulation.context.setVelocitiesToTemperature(300*unit.kelvin)
simulation.reporters.append(app.StateDataReporter(stdout, 50000, progress=True,
    potentialEnergy=True, temperature=True, remainingTime=True, totalSteps=1000000))
simulation.reporters.append(app.DCDReporter('traj_chicken_villin_HP35_solvated.dcd', 50000, enforcePeriodicBox=True))
simulation.reporters.append(HDF5Reporter('traj_chicken_villin_HP35_solvated.h5', 50000))
simulation.reporters.append(msm.thirds.openmm.reporters.H5MSMReporter('traj_chicken_villin_HP35_solvated.h5msm', 
                                                                      10000000, 50000))
simulation.step(1000000)
simulation.reporters[2].close()
final_positions = simulation.context.getState(getPositions=True).getPositions()

shutil.move('traj_chicken_villin_HP35_solvated.dcd', Path(data_dir, 'dcd/traj_chicken_villin_HP35_solvated.dcd'))
shutil.move('traj_chicken_villin_HP35_solvated.h5', Path(data_dir, 'h5/traj_chicken_villin_HP35_solvated.h5'))
shutil.move('traj_chicken_villin_HP35_solvated.h5msm', Path(data_dir, 'h5msm/traj_chicken_villin_HP35_solvated.h5msm'))

