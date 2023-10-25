from openmm import unit
import numpy as np

class MolSysMTTrajectoryDictReporter(object):

    def __init__(self, reportInterval, time=True, coordinates=True, velocities=False,
             potentialEnergy=False, kineticEnergy=False, totalEnergy=False, temperature=False,
             box=False, includeInitialContext=True):

        self._needsPositions = coordinates
        self._needsVelocities = velocities
        self._needsForces = False
        self._needsEnergy = (potentialEnergy or kineticEnergy or totalEnergy or temperature)

        self._time = time
        self._box = box
        self._coordinates = coordinates
        self._velocities = velocities
        self._potentialEnergy = potentialEnergy
        self._kineticEnergy = kineticEnergy
        self._totalEnergy = totalEnergy
        self._temperature = temperature


        self._initialized = False
        self._reportInterval = reportInterval
        self._includeInitialContext = includeInitialContext
        self._dict = {}

        if self._time:
            self._dict['time']=[]*unit.picoseconds

        if self._coordinates:
            self._dict['coordinates']=[]*unit.nanometer

        if self._velocities:
            self._dict['velocities']=[]*unit.nanometer/unit.picoseconds

        if self._potentialEnergy:
            self._dict['potential_energy']=[]*unit.kilojoule/unit.mole

        if self._kineticEnergy:
            self._dict['kinetic_energy']=[]*unit.kilojoule/unit.mole

        if self._totalEnergy:
            self._dict['total_energy']=[]*unit.kilojoule/unit.mole

        if self._temperature:
            self._dict['temperature']=[]*unit.kelvin

        if self._box:
            self._dict['box']=[]*unit.nanometer

    def _initialize(self, simulation):

        import openmm as mm
        system = simulation.system
        frclist = system.getForces()
        if self._temperature:
            dof = 0
            for i in range(system.getNumParticles()):
                if system.getParticleMass(i) > 0*unit.dalton:
                    dof += 3
            dof -= system.getNumConstraints()
            if any(isinstance(frc, mm.CMMotionRemover) for frc in frclist):
                dof -= 3
            self._dof = dof

        self._initialized = True

    def describeNextReport(self, simulation):

        if simulation.currentStep==0 and self._includeInitialContext:
            initial_state = simulation.context.getState(getPositions=self._needsPositions,
                                                       getVelocities=self._needsVelocities,
                                                       getForces=self._needsForces,
                                                       getEnergy=self._needsEnergy)
            self.report(simulation, initial_state)
            del(initial_state)

        steps_left = simulation.currentStep % self._reportInterval
        steps = self._reportInterval - steps_left
        return (steps, self._needsPositions, self._needsVelocities, self._needsForces, self._needsEnergy)

    def report(self, simulation, state):

        if not self._initialized:
            self._initialize(simulation)

        if self._time:
            time = state.getTime()
            self._dict['time'].append(time)

        if self._coordinates:
            coordinates = state.getPositions(asNumpy=True)
            self._dict['coordinates'].append(coordinates)

        if self._velocities:
            velocities = state.getVelocities(asNumpy=True)
            self._dict['velocities'].append(velocities)

        if self._potentialEnergy:
            potential_energy = state.getPotentialEnergy()
            self._dict['potential_energy'].append(potential_energy)

        if self._kineticEnergy:
            kinetic_energy = state.getKineticEnergy()
            self._dict['kinetic_energy'].append(kinetic_energy)

        if self._totalEnergy:
            if not self._kineticEnergy:
                kinetic_energy = state.getKineticEnergy()
            if not self._potentialEnergy:
                potential_energy = state.getPotentialEnergy()
            self._dict['total_energy'].append(kinetic_energy+potential_energy)

        if self._temperature:
            if not self._kineticEnergy:
                kinetic_energy = state.getKineticEnergy()
            temperature = 2 * kinetic_energy / (self._dof * unit.MOLAR_GAS_CONSTANT_R)
            self._dict['temperature'].append(temperature)

        if self._box:
            box = state.getPeriodicBoxVectors(asNumpy=True)
            self._dict['box'].append(box)

    def finalize(self):

        for key in self._dict.keys():
            self._dict[key]._value = np.stack(self._dict[key]._value)

        return self._dict

