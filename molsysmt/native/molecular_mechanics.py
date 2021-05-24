from molsysmt._private_tools.exceptions import *
from molsysmt import puw

class MolecularMechanics():

    def __init__(self, molecular_system=None, forcefield=None, water_model=None, implicit_solvent=None,
                 non_bonded_method='no_cutoff', non_bonded_cutoff=None, switch_distance=None,
                 use_dispersion_correction=False, ewald_error_tolerance=0.0001,
                 constraints=None, flexible_constraints=False,
                 rigid_water=True, hydrogen_mass=None,
                 residue_templates={}, ignore_external_bonds=False,
                 implicit_solvent_salt_conc='0.0 mol/L', implicit_solvent_kappa='0.0 1/nm',
                 solute_dielectric=1.0, solvent_dielectric=78.5):

        self._molecular_system = molecular_system

        self.forcefield = forcefield

        self.non_bonded_method = non_bonded_method
        self.non_bonded_cutoff = non_bonded_cutoff
        self.switch_distance = switch_distance
        self.use_dispersion_correction = use_dispersion_correction
        self.ewald_error_tolerance = ewald_error_tolerance

        self.hydrogen_mass = hydrogen_mass

        self.constraints = constraints
        self.flexible_constraints = flexible_constraints

        self.water_model = water_model
        self.rigid_water = rigid_water
        self.residue_templates = residue_templates
        self.ignore_external_bonds = ignore_external_bonds

        self.implicit_solvent = implicit_solvent
        self.solute_dielectric = solute_dielectric
        self.solvent_dielectric = solvent_dielectric
        self.implicit_solvent_salt_conc = implicit_solvent_salt_conc
        self.implicit_solvent_kappa = implicit_solvent_kappa

    def to_dict(self):

        tmp_dict = {
            'forcefield' : self.forcefield,
            'non_bonded_method' : self.non_bonded_method,
            'non_bonded_cutoff' : self.non_bonded_cutoff,
            'switch_distance' : self.switch_distance,
            'use_dispersion_correction' : self.use_dispersion_correction,
            'ewald_error_tolerance' : self.ewald_error_tolerance,
            'hydrogen_mass' : self.hydrogen_mass,
            'constraints' : self.constraints,
            'flexible_constraints' : self.flexible_constraints,
            'water_model' : self.water_model,
            'rigid_water' : self.rigid_water,
            'residue_templates' : self.residue_templates,
            'ignore_external_bonds' : self.ignore_external_bonds,
            'implicit_solvent' : self.implicit_solvent,
            'solute_dielectric' : self.solute_dielectric,
            'solvent_dielectric' : self.solvent_dielectric,
            'implicit_solvent_salt_conc' : self.implicit_solvent_salt_conc,
            'implicit_solvent_kappa' : self.implicit_solvent_kappa,
       }

    def copy(self):

        tmp_molecular_mechanics = MolecularMechanics()

        tmp_molecular_mechanics._molecular_system = self._molecular_system

        tmp_molecular_mechanics.forcefield = self.forcefield

        tmp_molecular_mechanics.non_bonded_method = self.non_bonded_method
        tmp_molecular_mechanics.non_bonded_cutoff = self.non_bonded_cutoff
        tmp_molecular_mechanics.switch_distance = self.switch_distance
        tmp_molecular_mechanics.use_dispersion_correction = self.use_dispersion_correction
        tmp_molecular_mechanics.ewald_error_tolerance = self.ewald_error_tolerance

        tmp_molecular_mechanics.hydrogen_mass = self.hydrogen_mass

        tmp_molecular_mechanics.constraints = self.constraints
        tmp_molecular_mechanics.flexible_constraints = self.flexible_constraints

        tmp_molecular_mechanics.water_model = self.water_model
        tmp_molecular_mechanics.rigid_water = self.rigid_water
        tmp_molecular_mechanics.residue_templates = self.residue_templates
        tmp_molecular_mechanics.ignore_external_bonds = self.ignore_external_bonds

        tmp_molecular_mechanics.implicit_solvent = self.implicit_solvent
        tmp_molecular_mechanics.solute_dielectric = self.solute_dielectric
        tmp_molecular_mechanics.solvent_dielectric = self.solvent_dielectric
        tmp_molecular_mechanics.implicit_solvent_salt_conc = self.implicit_solvent_salt_conc
        tmp_molecular_mechanics.implicit_solvent_kappa = self.implicit_solvent_kappa

        return tmp_molecular_mechanics

    def set_parameters(self, return_non_processed=False, **kwargs):

        for argument, value in kwargs.items():
            if argument.lower() in self.__dict__.keys():
                self.__dict__[argument]=puw.standardize(value)
                del(kwargs[argment.lower()])

        if return_non_processed:
            return kwargs
        else:
            pass

    def get_leap_parameters(self):

        from molsysmt.native.forcefields import get_forcefield_names

        parameters = {}

        parameters['forcefield'] = get_forcefield_names(self.forcefield, 'LEaP', water_model=self.water_model, implicit_solvent=self.implicit_solvent)
        parameters['water_model'] = self.water_model
        parameters['implicit_solvent'] = self.implicit_solvent

        return parameters

    def get_openmm_forcefield_names(self):

        from molsysmt.native.forcefields import get_forcefield_names

        return  get_forcefield_names(self.forcefield, 'OpenMM', water_model=self.water_model, implicit_solvent=self.implicit_solvent)

    def to_openmm_ForceField(self):

        from simtk.openmm.app import ForceField

        forcefield_names = self.get_openmm_forcefield_names()
        forcefield = ForceField(*forcefield_names)

        return forcefield

    def get_openmm_System_parameters(self):

        from simtk.openmm import app

        parameters = {}

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

        if self.non_bonded_cutoff is not None:
            parameters['nonbondedCutoff']=puw.convert(self.non_bonded_cutoff, to_form='simtk.unit',
                                                      to_unit='nm')

        if self.switch_distance is not None:
            parameters['switchDistance']=puw.convert(self.switch_distance, to_form='simtk.unit',
                                                       to_unit='nm')

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
        #parameters['removeCMMotion']=self.remove_cm_motion
        parameters['residueTemplates']=self.residue_templates
        parameters['ignoreExternalBonds']=self.ignore_external_bonds
        parameters['flexibleConstraints']=self.flexible_constraints

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

            parameters['implicitSolventSaltConc']=puw.convert(self.implicit_solvent_salt_cont,
                                                              to_unit='mole/liter', to_form='simtk.unit')
            parameters['implicitSolventKappa']=puw.convert(self.implicit_solvent_salt_kappa,
                                                           to_unit='1/nm', to_form='simtk.unit')
            parameters['soluteDielectric']=self.solute_dielectric
            parameters['solventDielectric']=self.solvent_dielectric

        else:
            parameters['implicitSolvent']=None

        #parameters['useDispersionCorrection']=self.use_dispersion_correction
        #parameters['ewaldErrorTolerance']=self.ewald_error_tolerance

        return parameters

    def to_openmm_System(self, molecular_system=None, selection='all', frame_indices='all'):

        from molsysmt.multitool import convert

        if molecular_system is None:
            molecular_system = self._molecular_system
        else:
            molecular_system = digest_molecular_system(molecular_system)

        if molecular_system is None:
            raise NoMolecularSystemError()

        system = convert([molecular_system, self], selection=selection, to_form='openmm.System')

        return system

