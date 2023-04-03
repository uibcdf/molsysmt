from molsysmt._private.exceptions import *
from molsysmt import pyunitwizard as puw
from copy import deepcopy

class MolecularMechanics():

    def __init__(self, forcefield=None, water_model=None, implicit_solvent=None,
                 non_bonded_method=None, cutoff_distance=None, switch_distance=None,
                 dispersion_correction=None, ewald_error_tolerance=None,
                 constraints=None, flexible_constraints=None,
                 rigid_water=None, hydrogen_mass=None,
                 salt_concentration=None, kappa=None,
                 solute_dielectric=None, solvent_dielectric=None,
                 formal_charge=None, partial_charge=None):

        # default values:
        # non_bonded_method='no_cutoff'
        # use_dispersion_correction=False
        # ewald_error_tolerance=0.0001
        # flexible_constraints=False
        # rigid_water=True
        # ignore_external_bonds=False
        # implicit_solvent_salt_conc=0.0 mol/L
        # implicit_solvent_kappa=0.0 1/nm
        # solute_dielectric=1.0
        # solvent_dielectric=78.5

        self.formal_charge = formal_charge
        self.partial_charge = partial_charge

        self.forcefield = forcefield

        self.non_bonded_method = non_bonded_method
        self.cutoff_distance = cutoff_distance
        self.switch_distance = switch_distance
        self.dispersion_correction = dispersion_correction
        self.ewald_error_tolerance = ewald_error_tolerance

        self.hydrogen_mass = hydrogen_mass

        self.constraints = constraints
        self.flexible_constraints = flexible_constraints

        self.water_model = water_model
        self.rigid_water = rigid_water
        #self.residue_templates = residue_templates
        #self.ignore_external_bonds = ignore_external_bonds

        self.implicit_solvent = implicit_solvent
        self.solute_dielectric = solute_dielectric
        self.solvent_dielectric = solvent_dielectric
        self.salt_concentration = salt_concentration
        self.kappa = kappa

    def to_dict(self):

        tmp_dict = {
                'formal_charge': self.formal_charge,
                'partial_charge': self.partial_charge,
                'forcefield' : self.forcefield,
                'non_bonded_method' : self.non_bonded_method,
                'cutoff_distance' : self.cutoff_distance,
                'switch_distance' : self.switch_distance,
                'dispersion_correction' : self.dispersion_correction,
                'ewald_error_tolerance' : self.ewald_error_tolerance,
                'hydrogen_mass' : self.hydrogen_mass,
                'constraints' : self.constraints,
                'flexible_constraints' : self.flexible_constraints,
                'water_model' : self.water_model,
                'rigid_water' : self.rigid_water,
                'implicit_solvent' : self.implicit_solvent,
                'solute_dielectric' : self.solute_dielectric,
                'solvent_dielectric' : self.solvent_dielectric,
                'salt_concentration' : self.salt_concentration,
                'kappa' : self.kappa,
       }

    def copy(self):

        tmp_molecular_mechanics = MolecularMechanics()

        tmp_molecular_mechanics.formal_charge = deepcopy(self.formal_charge)
        tmp_molecular_mechanics.partial_charge = deepcopy(self.partial_charge)

        tmp_molecular_mechanics.forcefield = deepcopy(self.forcefield)

        tmp_molecular_mechanics.non_bonded_method = deepcopy(self.non_bonded_method)
        tmp_molecular_mechanics.cutoff_distance = deepcopy(self.cutoff_distance)
        tmp_molecular_mechanics.switch_distance = deepcopy(self.switch_distance)
        tmp_molecular_mechanics.dispersion_correction = deepcopy(self.dispersion_correction)
        tmp_molecular_mechanics.ewald_error_tolerance = deepcopy(self.ewald_error_tolerance)

        tmp_molecular_mechanics.hydrogen_mass = deepcopy(self.hydrogen_mass)

        tmp_molecular_mechanics.constraints = deepcopy(self.constraints)
        tmp_molecular_mechanics.flexible_constraints = deepcopy(self.flexible_constraints)

        tmp_molecular_mechanics.water_model = deepcopy(self.water_model)
        tmp_molecular_mechanics.rigid_water = deepcopy(self.rigid_water)

        tmp_molecular_mechanics.implicit_solvent = deepcopy(self.implicit_solvent)
        tmp_molecular_mechanics.solute_dielectric = deepcopy(self.solute_dielectric)
        tmp_molecular_mechanics.solvent_dielectric = deepcopy(self.solvent_dielectric)
        tmp_molecular_mechanics.salt_concentration = deepcopy(self.salt_concentration)
        tmp_molecular_mechanics.kappa = deepcopy(self.kappa)

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

        from molsysmt.molecular_mechanics.forcefields import get_forcefield_names

        parameters = {}

        parameters['forcefield'] = get_forcefield_names(self.forcefield, 'LEaP', water_model=self.water_model, implicit_solvent=self.implicit_solvent)
        parameters['water_model'] = self.water_model
        parameters['implicit_solvent'] = self.implicit_solvent

        return parameters

    def get_openmm_forcefield_names(self):

        from molsysmt.molecular_mechanics.forcefields import get_forcefield_names

        return  get_forcefield_names(self.forcefield, 'OpenMM', water_model=self.water_model, implicit_solvent=self.implicit_solvent)

    def to_openmm_ForceField(self):

        from openmm.app import ForceField

        forcefield_names = self.get_openmm_forcefield_names()
        forcefield = ForceField(*forcefield_names)

        return forcefield

    def get_openmm_System_parameters(self):

        from openmm import app

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
            parameters['nonbondedCutoff']=puw.convert(self.cutoff_distance, to_form='openmm.unit',
                                                      to_unit='nm')

        if self.switch_distance is not None:
            parameters['switchDistance']=puw.convert(self.switch_distance, to_form='openmm.unit',
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

            parameters['implicitSolventSaltConc']=puw.convert(self.salt_concentration,
                                                              to_unit='mole/liter', to_form='openmm.unit')
            parameters['implicitSolventKappa']=puw.convert(self.kappa,
                                                           to_unit='1/nm', to_form='openmm.unit')
            parameters['soluteDielectric']=self.solute_dielectric
            parameters['solventDielectric']=self.solvent_dielectric

        else:
            parameters['implicitSolvent']=None

        return parameters

