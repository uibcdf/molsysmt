from molsysmt._private.variables import is_all
from molsysmt.basic import select
import numpy as np

class MSMH5Reporter(object):

    def __init__(self, file, reportInterval, stepSize, steps=None,
            context=None, topology=None, selection='all',
            time=True, box=True, coordinates=True, velocities=False,
            potentialEnergy=False, kineticEnergy=False, temperature=False,
            includeInitialContext=True, constantReportInterval=True,
            constantStepSize=True, constantBox=True,
            compression='gzip', compression_opts=4,
            int_precision='single', float_precision='single',
            syntax='MolSysMT'):

        self._initialized = False

        self._needsPositions = coordinates
        self._needsVelocities = velocities
        self._needsForces = False
        self._needEnergy = (potentialEnergy or kineticEnergy or totalEnergy or temperature)

        self._time = time
        self._box = box
        self._coordinates = coordinates
        self._velocities = velocities
        self._potentialEnergy = potentialEnergy
        self._kineticEnergy = kineticEnergy
        self._temperature = temperature

        self._reportInterval = reportInterval
        self._stepSize = stepSize
        self._steps = steps

        self._atom_indices = selection

        if not is_all(self._atom_indices):
            if topology is None:
                raise ValueError('A topology object is needed.')
            self._atom_indices = select(topology, selection=selection, syntax=syntax)

        self._file_handler = MSMH5FileHandler(file, io_mode='w', creator='OpenMM',
                compression=compression, compression_opts=compression_opts,
                int_precision=int_precision, float_precision=float_precision,
                length_unit='nm', time_unit='ps', energy_unit='kJ/mol',
                temperature_unit='kelvin', charge_unit='e', mass_unit='dalton')

        if topology is not None:
            self._file_handler.write_topology(topology, selection=self._atom_indices)


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

        # Tengo que detectar si hay barostato

        self._initialized = True

    def describeNextReport(self, simulation):

        steps_left = simulation.currentStep % self._reportInterval
        steps = self._reportInterval - steps_left
        return (steps, self._needsPositions, self._needsVelocities, self._needsForces, self._needEnergy)

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

