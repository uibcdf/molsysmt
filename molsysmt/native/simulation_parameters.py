from molsysmt._private_tools.exceptions import *

class Simulation():

    def __init__(self, molecular_system=None, forcefield=None, water_model=None, implicit_solvent=None,
                 non_bonded_method='no_cutoff', non_bonded_cutoff=None, switch_distance=None,
                 use_dispersion_correction=False, ewald_error_tolerance=0.0001,
                 constraints=None, flexible_constraints=False,
                 rigid_water=True, remove_cm_motion=True, hydrogen_mass=None,
                 implicit_solvent_salt_conc='0.0 mol/L', implicit_solvent_kappa='0.0 1/nm',
                 solute_dielectric=1.0, solvent_dielectric=78.5,
                 integrator='Langevin', temperature='300.0K', collisions_rate='1.0 1/ps', integration_timestep='2.0 fs',
                 platform='CUDA'):

        self._molecular_system = molecular_system

        self.forcefield = forcefield
        self.water_model = water_model
        self.implicit_solvent = implicit_solvent

        self.non_bonded_method = non_bonded_method
        self.non_bonded_cutoff = non_bonded_cutoff
        self.switch_distance = switch_distance
        self.use_dispersion_correction = use_dispersion_correction
        self.ewald_error_tolerance = ewald_error_tolerance

        self.constraints = constraints
        self.flexible_constraints = flexible_constraints
        self.rigid_water = rigid_water
        self.remove_cm_motion = remove_cm_motion
        self.hydrogen_mass = hydrogen_mass
        self.solute_dielectric = solute_dielectric
        self.solvent_dielectric = solvent_dielectric

        self.integrator = integrator
        self.temperature = temperature
        self.collisions_rate = collisions_rate
        self.integration_timestep = integration_timestep

        self.platform = platform

    def get_openmm_forcefield_names(self):

        pass

    def to_openmm_ForceField(self):

        from simtk.openmm.app import ForceField

        forcefield_names = self.to_openmm_forcefield_names()
        forcefield = ForceField(*forcefield_names)

        return forcefield

    def get_openmm_System_parameters(self):

        output = {}

        return output

    def to_openmm_System(self, molecular_system=None, selection='all', frame_indices='all'):

        from molsysmt.multitool import convert

        if molecular_system is None:
            molecular_system = self._molecular_system
        else:
            molecular_system = digest_molecular_system(molecular_system)

        if molecular_system is None:
            raise NoMolecularSystemError()

        topology = convert(molecular_system, selection=selection)

        forcefield = self.to_openmm_ForceField()
        system_parameters = self.to_openmm_System_parameters()
        system = forcefield.createSystem(topology, **system_parameters)

        if self.use_dispersion_correction or self.ewald_error_tolerance:
            forces = {ii.__class__.__name__ : ii for ii in tmp_item.getForces()}
            if self.use_dispersion_correction:
                forces['NonbondedForce'].setUseDispersionCorrection(True)
            if self.ewald_error_tolerance:
                forces['NonbondedForce'].setEwaldErrorTolerance(self.ewald_error_tolerance)

        return output

    def get_openmm_Simulation_parameters(self):

        output = {}

        return output

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

