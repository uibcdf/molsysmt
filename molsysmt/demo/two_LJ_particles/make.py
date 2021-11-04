import molsysmt as msm
import os
import openmm as mm
from openmm import app
from openmm import unit
import numpy as np
from tqdm import tqdm

# purge
print('Removing old files...')
files_to_be_purged = ['traj.trjpk']
for filename in files_to_be_purged:
    if os.path.isfile(filename):
        os.remove(filename)

# simulation

mass_1 = 39.948 * unit.amu
sigma_1 = 3.404 * unit.angstroms
epsilon_1 = 0.238 * unit.kilocalories_per_mole
charge_1 = 0.0 * unit.elementary_charge

mass_2 = 131.293 * unit.amu
sigma_2 = 3.961 * unit.angstroms
epsilon_2 = 0.459 * unit.kilocalories_per_mole
charge_2 = 0.0 * unit.elementary_charge

system = mm.System()

non_bonded_force = mm.NonbondedForce()

reduced_sigma = 0.5*(sigma_1+sigma_2)
cutoff_distance = 4.0*reduced_sigma
switching_distance = 3.0*reduced_sigma
non_bonded_force.setNonbondedMethod(mm.NonbondedForce.CutoffPeriodic)
non_bonded_force.setUseSwitchingFunction(True)
non_bonded_force.setCutoffDistance(cutoff_distance)
non_bonded_force.setSwitchingDistance(switching_distance)

system.addParticle(mass_1)
non_bonded_force.addParticle(charge_1, sigma_1, epsilon_1)

system.addParticle(mass_2)
non_bonded_force.addParticle(charge_2, sigma_2, epsilon_2)

system.setDefaultPeriodicBoxVectors([3.0, 0.0, 0.0]*unit.nanometers, [0.0, 3.0, 0.0]*unit.nanometers, [0.0, 0.0, 3.0]*unit.nanometers)

_ = system.addForce(non_bonded_force)

step_size = 2*unit.femtoseconds
temperature = 300*unit.kelvin
friction = 1.0/unit.picosecond

integrator = mm.LangevinIntegrator(temperature, friction, step_size)

platform_name = 'CUDA'
platform = mm.Platform.getPlatformByName(platform_name)

context = mm.Context(system, integrator, platform)

initial_positions  = np.zeros([2, 3], np.float32) * unit.angstroms
initial_velocities = np.zeros([2, 3], np.float32) * unit.angstroms/unit.picoseconds

initial_positions[1, 0] = 1.0 * unit.nanometers

context.setPositions(initial_positions)
context.setVelocities(initial_velocities)

simulation_time = 20.0*unit.nanosecond
saving_time = 1.0*unit.picoseconds

n_steps_per_saving_period = int(saving_time/step_size)
n_saving_periods = int(simulation_time/saving_time)

time = np.zeros([n_saving_periods], np.float32) * unit.picoseconds
position = np.zeros([n_saving_periods, 2, 3], np.float32) * unit.nanometers
velocity = np.zeros([n_saving_periods, 2, 3], np.float32) * unit.nanometers/unit.picosecond
potential_energy   = np.zeros([n_saving_periods], np.float32) * unit.kilocalories_per_mole
kinetic_energy     = np.zeros([n_saving_periods], np.float32) * unit.kilocalories_per_mole
box = np.zeros([n_saving_periods, 3, 3], np.float32) * unit.nanometers

state = context.getState(getPositions=True, getVelocities=True, getEnergy=True)
time[0] = state.getTime()
position[0] = state.getPositions()
velocity[0] = state.getVelocities()
kinetic_energy[0]=state.getKineticEnergy()
potential_energy[0]=state.getPotentialEnergy()
box[0] = state.getPeriodicBoxVectors()

for ii in tqdm(range(n_saving_periods)):
    context.getIntegrator().step(n_steps_per_saving_period)
    state = context.getState(getPositions=True, getVelocities=True, getEnergy=True)
    time[ii] = state.getTime()
    position[ii] = state.getPositions()
    velocity[ii] = state.getVelocities()
    kinetic_energy[ii]=state.getKineticEnergy()
    potential_energy[ii]=state.getPotentialEnergy()
    box[ii] = state.getPeriodicBoxVectors()

trajdict={
    'time' : time,
    'coordinates' : position,
    'box' : box
          }

msm.convert(trajdict, to_form='traj.trjpk')

