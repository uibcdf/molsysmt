import molsysmt as msm
import os
import openmm as mm
from openmm import app
from openmm import unit
from sys import stdout
from mdtraj.reporters import HDF5Reporter


# purge
print('Removing old files...')
files_to_be_purged = ['1vii.pdb', '1vii.mmtf', 'villin_hp35_vacuum.msmpk',
        'villin_hp35_solvated.msmpk', 'villin_hp35_solvated.dcd', 'villin_hp35_solvated.h5',
        'villin_hp35_solvated_last.pdb']
for filename in files_to_be_purged:
    if os.path.isfile(filename):
        os.remove(filename)

# 1vii pdb and mmtf files
print('Protein Data Bank files...')
msm.convert('pdbid:1vii', to_form='1vii.pdb')
msm.convert('pdbid:1vii', to_form='1vii.mmtf')

# vacuum
print('Vacuum system in msmpk file...')
molsys = msm.convert('pdbid:1vii', to_form='molsysmt.MolSys')
molsys = msm.build.remove_hydrogens(molsys)
molsys = msm.build.add_terminal_cappings(molsys, N_terminal='ACE', C_terminal='NME')
molsys = msm.build.add_hydrogens(molsys, pH=7.4)
_ = msm.convert(molsys, to_form='villin_hp35_vacuum.msmpk')

# solvated
print('Solvated system in msmpk file...')
molsys = msm.build.solvate([molsys, {'forcefield':'AMBER14', 'water_model':'TIP3P'}],
                   box_geometry='truncated octahedral', clearance='14.0 angstroms',
                   to_form='molsysmt.MolSys', engine="OpenMM", verbose=False)
_ = msm.convert(molsys, to_form='villin_hp35_solvated.msmpk')

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
simulation.reporters.append(app.DCDReporter('villin_hp35_solvated.dcd', 50000, enforcePeriodicBox=True))
simulation.reporters.append(HDF5Reporter('villin_hp35_solvated.h5', 50000))
simulation.step(1000000)
simulation.reporters[2].close()
final_positions = simulation.context.getState(getPositions=True).getPositions()
app.PDBFile.writeFile(modeller.topology, final_positions, open('villin_hp35_solvated_last.pdb', 'w'))

