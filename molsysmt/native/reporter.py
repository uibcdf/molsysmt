import openmm.unit as unit
from molsysmt.native.molsys import MolSys
from molsysmt.native.trajectory import Trajectory
import molsysmt as msm
from molsysmt._private.variables import is_all as _is_all
import time

class MolSysMTReporter():

    def __init__(self, reportInterval, topology, selection='all', syntax='MolSysMT',
                 step=True, time=True, coordinates=True, boxVectors=True,
                 potentialEnergy=False, kineticEnergy=False, temperature=False,
                 runningTime=False):

        if not is_all(selection):
            self._atom_indices = msm.selection(topology, selection=selection, syntax=syntax)
            self.topology = msm.convert(topology, to_form='molsysmt.Topology', selection=self._atom_indices)
        else:
            self._atom_indices = 'all'
            self.topology = msm.convert(topology, to_form='molsysmt.Topology')

        self._reportInterval = reportInterval
        self._step = step
        self._time = time
        self._coordinates = coordinates
        self._boxVectors = boxVectors
        self._potentialEnergy = potentialEnergy
        self._kineticEnergy = kineticEnergy
        self._temperature = temperature
        self._runningTime = runningTime

        self.step = []
        self.time = []
        self.coordinates = []
        self.box = []
        self.potential_energy = []
        self.kinetic_energy = []
        self.temperature = []
        self.starting_time = None
        self.running_time = None

        self._initialized=False
        self._dof = None

    def _initialize(self, simulation, state):

        if self._temperature:
            dof = 0
            for i in range(system.getNumParticles()):
                if system.getParticleMass(i) > 0*unit.dalton:
                    dof += 3
            for i in range(system.getNumConstraints()):
                p1, p2, distance = system.getConstraintParameters(i)
                if system.getParticleMass(p1) > 0*unit.dalton or system.getParticleMass(p2) > 0*unit.dalton:
                    dof -= 1
            if any(type(system.getForce(i)) == mm.CMMotionRemover for i in range(system.getNumForces())):
                dof -= 3
            self._dof = dof

        if self._runningTime:

            self.starting_time = time.time()

    def end(self):

        if self._runningTime:

            self.running_time = self.starting_time - time.time()

    def report(self, simulation, state):

        if self._step:
            value = simulation.currentStep
            self.step.append(value)

        if self._time:
            value = state.getTime().value_in_unit(unit.picosecond)
            self.time.append(value)

        if self._coordinates:
            value=state.getPositions(asNumpy=True)
            self.coordinates.append(value)

        if self._boxVectors:
            value=state.getPeriodicBoxVectors(asNumpy=True)
            self.box.append(value)

        if self._potentialEnergy:
            value=state.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)
            self.potential_energy.append(value)

        if self._kineticEnergy:
            value=state.getKineticEnergy().value_in_unit(unit.kilojoules_per_mole)
            self.kinetic_energy.append(value)

        if self._temperature:
            value=(2*state.getKineticEnergy()/(self._dof*unit.MOLAR_GAS_CONSTANT_R)).value_in_unit(unit.kelvin)

