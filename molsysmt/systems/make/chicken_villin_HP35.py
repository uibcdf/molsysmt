import molsysmt as msm
import os
import openmm as mm
from openmm import app
from openmm import unit
from sys import stdout
from mdtraj.reporters import HDF5Reporter
from pathlib import Path
import shutil

data_dir = Path('../../../data/.')

# Purge

files_to_be_purged = [
        'pdb/1vii.pdb',
        'mmtf/1vii.mmtf',
        'msmpk/chicken_villin_HP35.msmpk',
        'msmpk/chicken_villin_HP35_solvated.msmpk',
        'dcd/traj_chicken_villin_HP35_solvated.dcd',
        'h5/traj_chicken_villin_HP35_solvated.h5',
        ]

for filename in files_to_be_purged:
    filepath = Path(data_dir, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)

# Make

# 1vii pdb and mmtf files
print('Protein Data Bank files...')
msm.convert('pdb_id:1vii', to_form='1vii.pdb')
msm.convert('pdb_id:1vii', to_form='1vii.mmtf')
shutil.move('1vii.pdb', Path(data_dir, 'pdb/1vii.pdb'))
shutil.move('1vii.mmtf', Path(data_dir, 'mmtf/1vii.mmtf'))


# vacuum
print('Vacuum system in msmpk file...')
molsys = msm.convert('pdb_id:1vii', to_form='molsysmt.MolSys')
molsys = msm.basic.remove(molsys, selection='group_type==["water", "ion"]')
molsys = msm.basic.remove(molsys, selection='atom_type=="H"')
molsys = msm.build.add_missing_terminal_cappings(molsys, N_terminal='ACE', C_terminal='NME')
molsys = msm.build.add_missing_hydrogens(molsys, pH=7.4)
_ = msm.convert(molsys, to_form='chicken_villin_HP35.msmpk')
shutil.move('chicken_villin_HP35.msmpk', Path(data_dir, 'msmpk/chicken_villin_HP35.msmpk'))


# solvated
print('Solvated system in msmpk file...')
molsys = msm.build.solvate([molsys, {'forcefield':'AMBER14', 'water_model':'TIP3P'}],
                   box_shape='truncated octahedral', clearance='14.0 angstroms',
                   to_form='molsysmt.MolSys')
_ = msm.convert(molsys, to_form='chicken_villin_HP35_solvated.msmpk')
shutil.move('chicken_villin_HP35_solvated.msmpk', Path(data_dir, 'msmpk/chicken_villin_HP35_solvated.msmpk'))



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
simulation.step(1000000)
simulation.reporters[2].close()
final_positions = simulation.context.getState(getPositions=True).getPositions()

shutil.move('traj_chicken_villin_HP35_solvated.dcd', Path(data_dir, 'dcd/traj_chicken_villin_HP35_solvated.dcd'))
shutil.move('traj_chicken_villin_HP35_solvated.h5', Path(data_dir, 'h5/traj_chicken_villin_HP35_solvated.h5'))

