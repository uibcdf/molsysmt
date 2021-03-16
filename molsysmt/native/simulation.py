from molsysmt._private_tools.exceptions import *
from molsysmt import puw

class Simulation():

    def __init__(self, molecular_system=None, remove_cm_motion=True,
                 integrator=None, temperature=None, collisions_rate=None, integration_timestep=None,
                 initial_velocities_to_temperature = True,
                 platform='CUDA', cuda_precision='mixed'):

        self._molecular_system = molecular_system

        self.remove_cm_motion = remove_cm_motion

        self.integrator = integrator
        self.temperature = temperature
        self.collisions_rate = collisions_rate
        self.integration_timestep = integration_timestep

        self.initial_velocities_to_temperature = initial_velocities_to_temperature

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

        from simtk.openmm.app import LangevinInegrator

        temperature = puw.translate(self.temperature, in_units='K', to_form='simtk.unit')
        collisions_rate = puw.translate(self.temperature, in_units='1/ps', to_form='simtk.unit')
        integration_timestep = puw.translate(self.temperature, in_units='fs', to_form='simtk.unit')

        if self.integrator=='Langevin':
            integrator = LangevinIntegrator(temperature, collisions_rate, integration_timestep)
            if self.constraint_tolerance is not None:
                integrator.setConstraintTolerance(self.constraint_tolerance)
        else:
            raise NotImplementedError()

    def to_openmm_Platform(self):

        from simtk.openmm.app import Platform

        if self.platform in ['CUDA', 'CPU']:
            platform = Platform.getPlaformByName(platform)
        else:
            raise NotImplementedError()

    def get_openmm_Simulation_parameters(self):

        parameters = {}

        if platform=='CUDA':
            simulation_properties['CudaPrecision']='mixed'

        return parameters

    def to_openmm_Simulation(self, molecular_system=None, selection='all', frame_indices='all'):

        from molsysmt.multitool import convert

        if molecular_system is None:
            molecular_system = self._molecular_system
        else:
            molecular_system = digest_molecular_system(molecular_system)

        if molecular_system is None:
            raise NoMolecularSystemError()

        simulation = convert(molecular_system, selection=selection, simulation=self, to_form='openmm.Simulation')

        return simulation

