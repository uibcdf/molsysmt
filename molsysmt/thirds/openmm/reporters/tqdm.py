import openmm as mm
from openmm import unit
from tqdm.auto import tqdm
import time

class TQDMReporter(object):

    def __init__(self, reportInterval, total_n_steps, potential_energy=True, temperature=True,
            volume=False):

        self._pbar = None
        self._report_interval = reportInterval
        if self._report_interval==0:
            self._report_interval=1

        self._total_n_steps = total_n_steps

        self._with_potential_energy = potential_energy
        self._potential_energy = None
        self._with_temperature = temperature
        self._temperature = None
        self._with_volume = volume
        self._volume = None

        self._needs_positions = False
        self._needs_velocities = False
        self._needs_forces = False
        self._needs_energy = (potential_energy or temperature)
        self._initialized = False

        self._dof = 0

        self._U = 0.0 * unit.kilojoules_per_mole
        self._U2 = 0.0 * unit.kilojoules_per_mole**2
        self._T = 0.0 * unit.kelvin
        self._T2 = 0.0 * unit.kelvin**2
        self._V = 0.0 * unit.nanometers**3
        self._V2 = 0.0 * unit.nanometers**6
        self._iters = 0

        self._start_time = None
        self._end_time = None

        self._start_md_time = None
        self._end_md_time = None
        self._md_time_step = None

    def _initialize(self, simulation):

        self._start_time = time.time()

        self._pbar = tqdm(total=self._total_n_steps, position=0, leave=True)

        post_fix_dict={}
        if self._with_potential_energy:
            post_fix_dict['potential_energy'] = None
        if self._with_temperature:
            post_fix_dict['temperature'] = None
        if self._with_volume:
            post_fix_dict['volume'] = None

        self._pbar.set_postfix(post_fix_dict)

        if self._with_temperature:

            frclist = simulation.system.getForces()
            dof = 0
            for i in range(simulation.system.getNumParticles()):
                if simulation.system.getParticleMass(i) > 0.0*unit.dalton:
                    dof += 3
            dof -= simulation.system.getNumConstraints()
            if any(isinstance(frc, mm.CMMotionRemover) for frc in frclist):
                dof -= 3
            self._dof = dof

        initial_state = simulation.context.getState(getPositions=self._needs_positions,
                                                    getVelocities=self._needs_velocities,
                                                    getForces=self._needs_forces,
                                                    getEnergy=self._needs_energy)

        self._start_md_time = initial_state.getTime()
        self._md_time_step = simulation.integrator.getStepSize()

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

        post_fix_dict={}

        if self._with_potential_energy:
            aux = state.getPotentialEnergy()
            self._U += aux
            self._U2 += aux**2
            post_fix_dict['potential_energy'] = aux.format("%.2f")

        if self._with_temperature:
            aux = 2 * state.getKineticEnergy() / (self._dof * unit.MOLAR_GAS_CONSTANT_R)
            self._T += aux
            self._T2 += aux**2
            post_fix_dict['temperature'] = aux.format("%.2f")

        if self._with_volume:
            aux = state.getPeriodicBoxVolume()
            self._V += aux
            self._V2 += aux**2
            post_fix_dict['volume'] = aux.format("%.2f")

        self._iters +=1

        self._pbar.set_postfix(post_fix_dict)

        if simulation.currentStep == 0:
            self._pbar.update(0)
        else:
            self._pbar.update(self._report_interval)

        if (self._total_n_steps - simulation.currentStep) < self._report_interval:

            self.finalize(state)

    def finalize(self, state):

        self._pbar.close()

        self._end_md_time = state.getTime()
        self._end_time = time.time()

        execution_time = self._end_time - self._start_time
        days, remainder = divmod(execution_time, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        days = int(days)
        hours = int(hours)
        minutes = int(minutes)
        seconds = round(seconds,2)

        nanoseconds_md = (self._end_md_time-self._start_md_time).in_units_of(unit.nanoseconds)
        nanoseconds_per_hour = (nanoseconds_md._value / execution_time)*3600*24
        nanoseconds_per_hour = round(nanoseconds_per_hour,3)

        print('')
        if self._with_potential_energy:
            mean = self._U / self._iters
            std = (self._U2 / self._iters - mean**2)**0.5
            print(f'Potential energy: {mean.format("%.2f")} ± {std.format("%.2f")}')
        if self._with_temperature:
            mean = self._T / self._iters
            std = (self._T2 / self._iters - mean**2)**0.5
            print(f'Temperature: {mean.format("%.2f")} ± {std.format("%.2f")}')
        if self._with_volume:
            mean = self._V / self._iters
            std = (self._V2 / self._iters - mean**2)**0.5
            print(f'Volume: {mean.format("%.2f")} ± {std.format("%.2f")}')
        print('')
        print(f'Execution time: {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds ({nanoseconds_per_hour} ns/day).')
        print('')

        pass

