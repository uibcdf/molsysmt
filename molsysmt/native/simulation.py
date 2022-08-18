from molsysmt._private.exceptions import *
from molsysmt import pyunitwizard as puw

class Simulation():

    def __init__(self, molecular_system=None, remove_cm_motion=True,
                 integrator=None, temperature=None, collisions_rate=None, integration_timestep=None,
                 initial_velocities_to_temperature = True, constraint_tolerance=0.00001,
                 platform='CUDA', cuda_precision='mixed'):

        self._molecular_system = molecular_system

        self.remove_cm_motion = remove_cm_motion

        self.integrator = integrator
        self.temperature = temperature
        self.collisions_rate = collisions_rate
        self.integration_timestep = integration_timestep

        self.initial_velocities_to_temperature = initial_velocities_to_temperature

        self.constraint_tolerance = constraint_tolerance

        self.platform = platform
        self.cuda_precision = cuda_precision

    def to_dict(self):

        tmp_dict = {
            'remove_cm_motion' : self.remove_cm_motion,
            'integrator' : self.integrator,
            'temperature' : self.temperature,
            'collisions_rate' : self.collisions_rate,
            'integration_timestep' : self.integration_timestep,
            'initial_velocities_to_temperature' : self.initial_velocities_to_temperature,
            'constraint_tolerance' : self.constraint_tolerance,
            'platform' : self.platform,
            'cuda_precision' : self.cuda_precision,
        }

        return tmp_dict

    def copy(self):

        tmp_simulation = Simulation()

        tmp_simulation._molecular_system = self._molecular_system

        tmp_simulation.remove_cm_motion = self.remove_cm_motion

        tmp_simulation.integrator = self.integrator
        tmp_simulation.temperature = self.temperature
        tmp_simulation.collisions_rate = self.collisions_rate
        tmp_simulation.integration_timestep = self.integration_timestep

        tmp_simulation.initial_velocities_to_temperature = self.initial_velocities_to_temperature

        tmp_constraint_tolerance = self.constraint_tolerance

        tmp_simulation.platform = self.platform
        tmp_simulation.cuda_precision = self.cuda_precision

        return tmp_simulation

    def set_parameters(self, return_non_processed=False, **kwargs):

        for argument, value in kwargs.items():
            if argument.lower() in self.__dict__.keys():
                self.__dict__[argument]=puw.standardize(value)
                del(kwargs[argment.lower()])

        if return_non_processed:
            return kwargs
        else:
            pass

    def to_openmm_Integrator(self):

        from openmm import LangevinIntegrator

        temperature = puw.convert(self.temperature, to_unit='K', to_form='openmm.unit')
        collisions_rate = puw.convert(self.collisions_rate, to_unit='1/ps', to_form='openmm.unit')
        integration_timestep = puw.convert(self.integration_timestep, to_unit='fs', to_form='openmm.unit')

        if self.integrator=='Langevin':
            integrator = LangevinIntegrator(temperature, collisions_rate, integration_timestep)
            if self.constraint_tolerance is not None:
                integrator.setConstraintTolerance(self.constraint_tolerance)
        else:
            raise NotImplementedError()

        return integrator

    def to_openmm_Platform(self):

        from openmm import Platform

        if self.platform in ['CUDA', 'CPU']:
            platform = Platform.getPlatformByName(self.platform)
        else:
            raise NotImplementedError()

        return platform

    def get_openmm_Context_parameters(self):

        parameters = {}

        if self.platform=='CUDA':
            parameters['CudaPrecision']=self.cuda_precision

        return parameters

    def to_openmm_Context(self, molecular_system=None, selection='all', structure_indices='all'):

        from molsysmt.basic import convert

        if molecular_system is None:
            molecular_system = self._molecular_system
        else:
            molecular_system = digest_molecular_system(molecular_system)

        if molecular_system is None:
            raise NoMolecularSystemError()

        context = convert(molecular_system, to_form='openmm.Context', selection=selection, simulation=self)

        return context

    def get_openmm_Simulation_parameters(self):

        parameters = {}

        if self.platform=='CUDA':
            parameters['CudaPrecision']=self.cuda_precision

        return parameters

    def to_openmm_Simulation(self, molecular_system=None, selection='all', structure_indices='all'):

        from molsysmt.basic import convert

        if molecular_system is None:
            molecular_system = self._molecular_system
        else:
            molecular_system = digest_molecular_system(molecular_system)

        if molecular_system is None:
            raise NoMolecularSystemError()

        simulation = convert(molecular_system, to_form='openmm.Simulation', selection=selection, simulation=self)

        return simulation

simulation_to_potential_energy_minimization = Simulation(integrator='Langevin', temperature='0 K',
                                                         collisions_rate='1.0 1/ps', integration_timestep='2fs',
                                                         initial_velocities_to_temperature = False,
                                                         platform='CUDA', cuda_precision='mixed')


