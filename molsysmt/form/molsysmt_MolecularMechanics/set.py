from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

###### Set

###
## Atom
###

# Mechanical

@digest(form='molsysmt.MolecularMechanics')
def set_formal_charge_to_atom(item, atom_indices='all', value=None, skip_digestion=False):

    if is_all(atom_indices):

        item.formal_charge = value

    else:
        item.formal_charge[atom_indices] = value

    pass

@digest(form='molsysmt.MolecularMechanics')
def set_partial_charge_to_atom(item, atom_indices='all', value=None, skip_digestion=False):

    if is_all(atom_indices):

        item.partial_charge = value

    else:
        item.partial_charge[atom_indices] = value

    pass

###
### System
###

# Mechanical

@digest(form='molsysmt.MolecularMechanics')
def set_forcefield_to_system(item, value=None, skip_digestion=False):

    item.forcefield = value

    pass

@digest(form='molsysmt.MolecularMechanics')
def set_non_bonded_method_to_system(item, value=None, skip_digestion=False):

    item.non_bonded_method = value

    pass

@digest(form='molsysmt.MolecularMechanics')
def set_cutoff_distance_to_system(item, value=None, skip_digestion=False):

    item.cutoff_distance = value

    pass

@digest(form='molsysmt.MolecularMechanics')
def set_switch_distance_to_system(item, value=None, skip_digestion=False):

    item.switch_distance = value

    pass

@digest(form='molsysmt.MolecularMechanics')
def set_dispersion_correction_to_system(item, value=None, skip_digestion=False):

    item.dispersion_correction = value

    pass

@digest(form='molsysmt.MolecularMechanics')
def set_ewald_error_tolerance_to_system(item, value=None, skip_digestion=False):

    item.ewald_error_tolerance = value

    pass

@digest(form='molsysmt.MolecularMechanics')
def set_hydrogen_mass_to_system(item, value=None, skip_digestion=False):

    item.hydrogen_mass = value

    pass


@digest(form='molsysmt.MolecularMechanics')
def set_constraints_to_system(item, value=None, skip_digestion=False):

    item.constraints = value

    pass

@digest(form='molsysmt.MolecularMechanics')
def set_flexible_constraints_to_system(item, value=None, skip_digestion=False):

    item.flexible_constraints = value

    pass

@digest(form='molsysmt.MolecularMechanics')
def set_water_model_to_system(item, value=None, skip_digestion=False):

    item.water_model = value

    pass

@digest(form='molsysmt.MolecularMechanics')
def set_rigid_water_to_system(item, value=None, skip_digestion=False):

    item.rigid_water = value

    pass

@digest(form='molsysmt.MolecularMechanics')
def set_implicit_solvent_to_system(item, value=None, skip_digestion=False):

    item.implicit_solvent = value

    pass

@digest(form='molsysmt.MolecularMechanics')
def set_solute_dielectric_to_system(item, value=None, skip_digestion=False):

    item.solute_dielectric = value

    pass

@digest(form='molsysmt.MolecularMechanics')
def set_solvent_dielectric_to_system(item, value=None, skip_digestion=False):

    item.solvent_dielectric = value

    pass

@digest(form='molsysmt.MolecularMechanics')
def set_salt_concentration_to_system(item, value=None, skip_digestion=False):

    item.salt_concentration = value

    pass

@digest(form='molsysmt.MolecularMechanics')
def set_kappa_to_system(item, value=None, skip_digestion=False):

    item.kappa = value

    pass

















