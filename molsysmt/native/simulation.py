from molsysmt._private_tools.exceptions import *

class Simulation():

    def __init__(self, molecular_system=None, forcefield=None, water_model=None, implicit_solvent=None,
                 non_bonded_method='no_cutoff', non_bonded_cutoff=None, switch_distance=None,
                 use_dispersion_correction=False, ewald_error_tolerance=0.0001,
                 constraints=None, flexible_constraints=False, constraint_tolerance=0.00001,
                 rigid_water=True, remove_cm_motion=True, hydrogen_mass=None,
                 residue_templates={}, ignore_external_bonds=False,
                 implicit_solvent_salt_conc='0.0 mol/L', implicit_solvent_kappa='0.0 1/nm',
                 solute_dielectric=1.0, solvent_dielectric=78.5,
                 integrator='Langevin', temperature='300.0K', collisions_rate='1.0 1/ps', integration_timestep='2.0 fs',
                 initial_velocities_to_temperature = True,
                 platform='CUDA'):

        self._molecular_system = molecular_system

        self.forcefield = forcefield

        self.non_bonded_method = non_bonded_method
        self.non_bonded_cutoff = non_bonded_cutoff
        self.switch_distance = switch_distance
        self.use_dispersion_correction = use_dispersion_correction
        self.ewald_error_tolerance = ewald_error_tolerance

        self.hydrogen_mass = hydrogen_mass
        self.remove_cm_motion = remove_cm_motion

        self.constraints = constraints
        self.flexible_constraints = flexible_constraints
        self.constraint_tolerance = constraint_tolerance

        self.water_model = water_model
        self.rigid_water = rigid_water
        self.residue_templates = residue_templates
        self.ignore_external_bonds = ignore_external_bonds

        self.implicit_solvent = implicit_solvent
        self.solute_dielectric = solute_dielectric
        self.solvent_dielectric = solvent_dielectric
        self.implicit_solvent_salt_conc = implicit_solvent_salt_conc
        self.implicit_solvent_kappa = implicit_solvent_kappa

        self.integrator = integrator
        self.temperature = temperature
        self.collisions_rate = collisions_rate
        self.integration_timestep = integration_timestep

        self.initial_velocities_to_temperature = initial_velocities_to_temperature

        self.platform = platform

    def get_openmm_forcefield_names(self):

        pass

    def to_openmm_ForceField(self):

        from simtk.openmm.app import ForceField

        forcefield_names = self.to_openmm_forcefield_names()
        forcefield = ForceField(*forcefield_names)

        return forcefield

    def get_openmm_System_parameters(self):

        from simtk.openmm import app

        parameters = {}

        if self.platform == 'CUDA':
            parameters['CudaPrecision']='mixed'

        if self.non_bonded_method=='no_cutoff':
            parameters['nonbondedMethod']=app.NoCutoff
        elif self.non_bonded_method=='cutoff_non_periodic':
            parameters['nonbondedMethod']=app.CutoffNonPeriodic
        elif self.non_bonded_method=='cutoff_periodic':
            parameters['nonbondedMethod']=app.CutoffPeriodic
        elif self.non_bonded_method=='Ewald':
            parameters['nonbondedMethod']=app.Ewald
        elif self.non_bonded_method=='PME':
            parameters['nonbondedMethod']=app.PME
        elif self.non_bonded_method=='LJPME':
            parameters['nonbondedMethod']=app.LJPME
        else:
            raise NotImplementedError()

        parameters['nonbondedCutoff']=puw.translate(self.non_bonded_cutoff, in_units='nm', to_form='simtk.unit')
        parameters['switchDistance']=puw.translate(self.switch_distance, in_units='nm', to_form='simtk.unit')

        if self.constraints is not None:
            if self.constraints == 'h_bonds':
                parameters['constraints']=app.HBonds
            elif self.constraints == 'all_bonds':
                parameters['constraints']=app.HBonds
            elif self.constraints == 'h_angles':
                parameters['constraints']=app.HAngles
            else:
                raise NotImplementedError()
        else:
            parameters['constraints']=None

        parameters['hydrogenMass']=self.hydrogen_mass
        parameters['rigidWater']=self.rigid_water
        parameters['removeCMMotion']=self.remove_cm_motion
        parameters['residueTemplates']=self.residue_templates
        parameters['ignoreExternalBonds']=self.ignore_external_bonds
        parameters['flexibleConstraints']=self.flexible_constraints
        parameters['constraintTolerante']=self.constraint_tolerance

        if self.implicit_solvent is not None:

            if self.implicit_solvent == 'HCT':
                parameters['implicitSolvent']=app.HCT
            elif self.implicit_solvent == 'OBC1':
                parameters['implicitSolvent']=app.OBC1
            elif self.implicit_solvent == 'OBC2':
                parameters['implicitSolvent']=app.OBC2
            elif self.implicit_solvent == 'GBn':
                parameters['implicitSolvent']=app.GBn
            elif self.implicit_solvent == 'GBn2':
                parameters['implicitSolvent']=app.GBn2
            else:
                raise NotImplementedError

            parameters['implicitSolventSaltConc']=puw.translate(self.implicit_solvent_salt_cont, in_units='mole/liter', in_form='simtk.unit')
            parameters['implicitSolventKappa']=puw.translate(self.implicit_solvent_salt_kappa, in_units='1/nm', in_form='simtk.unit')
            parameters['soluteDielectric']=self.solute_dielectric
            parameters['solventDielectric']=self.solvent_dielectric

        else:
            parameters['implicitSolvent']=None

        parameters['useDispersionCorrection']=self.use_dispersion_correction
        parameters['ewaldErrorTolerance']=self.ewald_error_tolerance


        return parameters

    def to_openmm_System(self, molecular_system=None, selection='all', frame_indices='all'):

        from molsysmt.multitool import convert

        if molecular_system is None:
            molecular_system = self._molecular_system
        else:
            molecular_system = digest_molecular_system(molecular_system)

        if molecular_system is None:
            raise NoMolecularSystemError()

        system = convert(molecular_system, selection=selection, simulation=self, to_form='openmm.System')

        return system

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

