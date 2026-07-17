import pandas as pd
from molsysmt._private.smonitor import *
from molsysmt import pyunitwizard as puw
from copy import deepcopy

class MolecularMechanics():
    """Container for molecular mechanics force-field settings.

    Per-atom force-field parameters (formal_charge, partial_charge,
    atom_ff_type) are grouped in the ``atoms_ff`` DataFrame, indexed by
    atom position (0..n_atoms-1).  The DataFrame is None when no per-atom
    FF data has been assigned.
    """

    def __init__(self, forcefield=None, water_model=None, implicit_solvent=None,
                 non_bonded_method=None, cutoff_distance=None, switch_distance=None,
                 dispersion_correction=None, ewald_error_tolerance=None,
                 constraints=None, flexible_constraints=None,
                 rigid_water=None, hydrogen_mass=None,
                 salt_concentration=None, kappa=None,
                 solute_dielectric=None, solvent_dielectric=None,
                 formal_charge=None, partial_charge=None, atom_ff_type=None):
        """Initialize molecular mechanics parameters."""

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

        # Per-atom FF parameters: stored in atoms_ff DataFrame
        self.atoms_ff = None
        if formal_charge is not None:
            self.formal_charge = formal_charge
        if partial_charge is not None:
            self.partial_charge = partial_charge
        if atom_ff_type is not None:
            self.atom_ff_type = atom_ff_type

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

    def __setstate__(self, state):
        """Restore current storage or stage legacy charge arrays for MolSys."""

        legacy_formal_charge = state.pop('formal_charge', None)
        legacy_partial_charge = state.pop('partial_charge', None)
        restored = type(self)()
        self.__dict__.update(restored.__dict__)
        self.__dict__.update(state)
        if legacy_formal_charge is not None:
            self._legacy_formal_charge = legacy_formal_charge
        if legacy_partial_charge is not None:
            self._legacy_partial_charge = legacy_partial_charge

    # ------------------------------------------------------------------
    # atoms_ff helpers
    # ------------------------------------------------------------------

    def _ensure_atoms_ff(self, n_atoms):
        """Create atoms_ff DataFrame if it does not exist yet."""
        if self.atoms_ff is None:
            self.atoms_ff = pd.DataFrame(index=range(n_atoms))

    def _get_atoms_ff_column(self, column):
        """Return the column values, or None if absent/all-null."""
        if self.atoms_ff is None or column not in self.atoms_ff.columns:
            return None
        col = self.atoms_ff[column]
        if col.isnull().all():
            return None
        return col.to_numpy(dtype=object)

    def _set_atoms_ff_column(self, column, value):
        """Write *value* into the given atoms_ff column."""
        if value is None:
            if self.atoms_ff is not None and column in self.atoms_ff.columns:
                self.atoms_ff = self.atoms_ff.drop(columns=column)
                if self.atoms_ff.shape[1] == 0:
                    self.atoms_ff = None
            return
        self._ensure_atoms_ff(len(value))
        self.atoms_ff[column] = value

    # ------------------------------------------------------------------
    # Per-atom properties (backed by atoms_ff)
    # ------------------------------------------------------------------

    @property
    def formal_charge(self):
        return self._get_atoms_ff_column('formal_charge')

    @formal_charge.setter
    def formal_charge(self, value):
        self._set_atoms_ff_column('formal_charge', value)

    @property
    def partial_charge(self):
        return self._get_atoms_ff_column('partial_charge')

    @partial_charge.setter
    def partial_charge(self, value):
        self._set_atoms_ff_column('partial_charge', value)

    @property
    def atom_ff_type(self):
        return self._get_atoms_ff_column('atom_ff_type')

    @atom_ff_type.setter
    def atom_ff_type(self, value):
        self._set_atoms_ff_column('atom_ff_type', value)

    # ------------------------------------------------------------------

    def to_dict(self):
        """Return a dictionary representation of the parameters."""

        tmp_dict = {
                'formal_charge': self.formal_charge,
                'partial_charge': self.partial_charge,
                'atom_ff_type': self.atom_ff_type,
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

        return tmp_dict

    def copy(self):
        """Create a deep copy of the MolecularMechanics object."""

        tmp_molecular_mechanics = MolecularMechanics()

        tmp_molecular_mechanics.atoms_ff = deepcopy(self.atoms_ff)

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
        """Standardize and set available parameters from keyword arguments."""

        for argument, value in kwargs.items():
            if argument.lower() in self.__dict__.keys():
                self.__dict__[argument]=puw.standardize(value)
                del(kwargs[argument.lower()])

        if return_non_processed:
            return kwargs
        else:
            pass

    def get_leap_parameters(self):
        """Get parameter names for LEaP-compatible force fields."""

        from molsysmt.molecular_mechanics.forcefields import get_forcefield_names

        parameters = {}

        parameters['forcefield'] = get_forcefield_names(self.forcefield, 'LEaP', water_model=self.water_model, implicit_solvent=self.implicit_solvent)
        parameters['water_model'] = self.water_model
        parameters['implicit_solvent'] = self.implicit_solvent

        return parameters

    def get_openmm_forcefield_names(self):
        """Resolve OpenMM force field names for the configured options."""

        from molsysmt.molecular_mechanics.forcefields import get_forcefield_names

        return  get_forcefield_names(self.forcefield, 'OpenMM', water_model=self.water_model, implicit_solvent=self.implicit_solvent)

    def to_openmm_ForceField(self):
        """Instantiate an OpenMM ForceField object."""

        from openmm.app import ForceField

        forcefield_names = self.get_openmm_forcefield_names()
        forcefield = ForceField(*forcefield_names)

        return forcefield

    def get_openmm_System_parameters(self):
        """Build the keyword dictionary for creating an OpenMM System."""

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

        if self.cutoff_distance is not None:
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
