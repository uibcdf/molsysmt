from molsysmt._private.variables import is_all
from molsysmt.basic import select, get
import numpy as np
import openmm as mm
from openmm import unit

class MSMH5Reporter(object):

    def __init__(self, file, reportInterval, steps, selection='all',
            topology=True, time=True, box=True, coordinates=True, velocities=False,
            potentialEnergy=False, kineticEnergy=False, temperature=False,
            includeInitialContext=True, constantReportInterval=True,
            constantStepSize=True, constantBox=True,
            compression='lzf', compression_opts=None,
            int_precision='single', float_precision='single',
            auto_close=False, syntax='MolSysMT'):

        from molsysmt.native import MSMH5FileHandler

        self._initialized = False

        self._needs_positions = coordinates
        self._needs_velocities = velocities
        self._needs_forces = False
        self._needs_energy = (potentialEnergy or kineticEnergy or totalEnergy or temperature)

        self._id = True
        self._topology = topology
        self._time = time
        self._box = box
        self._coordinates = coordinates
        self._velocities = velocities
        self._potential_energy = potentialEnergy
        self._kinetic_energy = kineticEnergy
        self._temperature = temperature

        self._include_initial_context = includeInitialContext
        self._constant_report_interval = constantReportInterval
        self._constant_step_size = constantStepSize
        self._constant_box = constantBox

        self._report_interval = reportInterval
        self._step_size = None
        self._steps = steps

        self._n_atoms = None
        self._selection = selection
        self._selection_is_all = False
        self._syntax = syntax

        self._n_structures = 0
        self._n_structures_reported = 0

        self._file_handler = MSMH5FileHandler(file, io_mode='w', creator='OpenMM',
                compression=compression, compression_opts=compression_opts,
                int_precision=int_precision, float_precision=float_precision,
                length_unit='nm', time_unit='ps', energy_unit='kJ/mol',
                temperature_unit='kelvin', charge_unit='e', mass_unit='dalton')

        if isinstance(topology, mm.app.Topology):

            if not is_all(self._selection):
                self._selection = select(topology, selection=self._selection, syntax=self._syntax)
                self._selection_is_all = False
                self._n_atoms = len(self._selection)
            else:
                self._selection_is_all = True
                self._n_atoms = get(topology, element='system', n_atoms=True)

            self._file_handler.write_topology(topology, selection=self._selection)

            self._topology = False

        self._structures_sd = self._file_handler.file['structures']

        self._auto_close = auto_close

    def _initialize(self, simulation):

        system = simulation.system
        context = simulation.context
        topology = simulation.topology
        integrator = simulation.integrator

        if self._topology:

            if not is_all(self._selection):
                self._selection = select(topology, selection=self._selection, syntax=self._syntax)
                self._selection_is_all = False
                self._n_atoms = len(self._selection)
            else:
                self._selection_is_all = True
                self._n_atoms = get(topology, element='system', n_atoms=True)

            self._file_handler.write_topology(topology, selection=self._selection)

        elif self._n_atoms == 0:

            if not is_all(self._selection):
                self._selection = select(topology, selection=self._selection, syntax=self._syntax)
                self._selection_is_all = False
                self._n_atoms = len(self._selection)
            else:
                self._selection_is_all = True
                self._n_atoms = get(topology, element='system', n_atoms=True)

        frclist = system.getForces()

        if self._temperature:
            dof = 0
            for i in range(system.getNumParticles()):
                if system.getParticleMass(i) > 0.0*unit.dalton:
                    dof += 3
            dof -= system.getNumConstraints()
            if any(isinstance(frc, mm.CMMotionRemover) for frc in frclist):
                dof -= 3
            self._dof = dof

        if self._box:
            if system.usesPeriodicBoundaryConditions():
                if  self._constant_box:
                    self._constant_box = True # Barostat needs to be checked
                    self._structures_sd.attrs['constant_box']=True
                    self._structures_sd.attrs['pbc']='continuous'

        if self._constant_report_interval:
            self._structures_sd.attrs['constant_id_step']=True
            self._structures_sd.attrs['id_step']=self._report_interval
            if self._constant_step_size:
                self._step_size = integrator.getStepSize()
                self._structures_sd.attrs['constant_time_step']=True
                self._structures_sd.attrs['time_step']=(self._step_size.in_units_of(unit.picoseconds)._value)*self._report_interval

        if self._steps is not None:

            self._n_structures = int(self._steps/self._report_interval)

            if self._include_initial_context:
                self._n_structures +=1

            if self._constant_report_interval:
                self._structures_sd['id'].resize((1,))
            else:
                self._structures_sd['id'].resize((self._n_structures))

            if self._time:
                if self._constant_report_interval and self._constant_step_size:
                    self._structures_sd['time'].resize((1,))
                else:
                    self._structures_sd['time'].resize((self._n_structures))

            if self._box:
                if self._constant_box:
                    self._structures_sd['box'].resize((1, 3, 3))
                else:
                    self._structures_sd['box'].resize((self._n_structures, 3, 3))

            if self._coordinates:
                self._structures_sd['coordinates'].resize((self._n_structures, self._n_atoms, 3))

            if self._velocities:
                self._structures_sd['velocities'].resize((self._n_structures, self._n_atoms, 3))

            if self._kinetic_energy:
                self._structures_sd['kinetic_energy'].resize((self._n_structures,))

            if self._potential_energy:
                self._structures_sd['potential_energy'].resize((self._n_structures,))

            if self._temperature:
                self._structures_sd['temperature'].resize((self._n_structures,))

            self._structures_sd.attrs['n_structures']=self._n_structures

        if self._include_initial_context:
            initial_state = simulation.context.getState(getPositions=self._needs_positions,
                                                       getVelocities=self._needs_velocities,
                                                       getForces=self._needs_forces,
                                                       getEnergy=self._needs_energy)
            self.report(simulation, initial_state)
            del(initial_state)

        self._initialized = True

    def describeNextReport(self, simulation):

        if not self._initialized:
            self._initialize(simulation)

        steps_left = simulation.currentStep % self._report_interval
        steps = self._report_interval - steps_left
        return (steps, self._needs_positions, self._needs_velocities, self._needs_forces,
                self._needs_energy)

    def report(self, simulation, state):

        index = self._n_structures_reported

        if self._id:
            self._structures_sd['id'][index] = simulation.currentStep
            if self._constant_report_interval:
                self._id = False

        if self._time:
            self._structures_sd['time'][index] = state.getTime()._value
            if self._constant_report_interval and self._constant_step_size:
                self._time = False

        if self._box:
            self._structures_sd['box'][index,:,:] = state.getPeriodicBoxVectors(asNumpy=True)._value
            if self._constant_box:
                self._box = False

        if self._coordinates:
            if self._selection_is_all:
                self._structures_sd['coordinates'][index,:,:] = state.getPositions(asNumpy=True)._value
            else:
                self._structures_sd['coordinates'][index,:,:] = state.getPositions(asNumpy=True)[selection,:]._value

        if self._velocities:
            if self._selection_is_all:
                self._structures_sd['velocities'][index,:,:] = state.getVelocities(asNumpy=True)._value
            else:
                self._structures_sd['velocities'][index,:,:] = state.getVelocities(asNumpy=True)[selection,:]._value

        if self._potential_energy:
            self._structures_sd['potential_energy'][index] = state.getPotentialEnergy()._value

        if self._kinetic_energy:
            self._structures_sd['kinetic_energy'][index] = state.getKineticEnergy()._value

        if self._temperature:
            kinetic_energy = state.getKineticEnergy()
            temperature = 2 * kinetic_energy / (self._dof * unit.MOLAR_GAS_CONSTANT_R)
            self._structures_sd['temperature'][index] = temperature._value

        self._n_structures_reported += 1
        self._structures_sd.attrs['n_structures_written'] = self._n_structures_reported

        if self._auto_close and self._steps is not None:
            if (self._steps - simulation.currentStep) < self._report_interval:
                self.close()

        pass

    def close(self):

        return self._file_handler.close()

