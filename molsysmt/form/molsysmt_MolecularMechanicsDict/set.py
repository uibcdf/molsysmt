from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

###### Set

###
## Atom
###

# Mechanical

@digest(form='molsysmt.MolecularMechanicsDict')
def set_formal_charge_to_atom(item, atom_indices='all', value=None):

    if is_all(atom_indices):

        item['formal_charge'] = value

    else:

        item['formal_charge'][atom_indices] = value

    pass

@digest(form='molsysmt.MolecularMechanicsDict')
def set_partial_charge_to_atom(item, atom_indices='all', value=None):

    if is_all(atom_indices):

        item['partial_charge'] = value

    else:

        item['partial_charge'][atom_indices] = value

    pass

###
### System
###

# Mechanical

@digest(form='molsysmt.MolecularMechanicsDict')
def set_forcefield_to_system(item, value=None):

    item['forcefield'] = value

    pass

@digest(form='molsysmt.MolecularMechanicsDict')
def set_non_bonded_method_to_system(item, value=None):

    item['non_bonded_method'] = value

    pass

@digest(form='molsysmt.MolecularMechanicsDict')
def set_cutoff_distance_to_system(item, value=None):

    item['cutoff_distance'] = value

    pass

@digest(form='molsysmt.MolecularMechanicsDict')
def set_switch_distance_to_system(item, value=None):

    item['switch_distance'] = value

    pass

@digest(form='molsysmt.MolecularMechanicsDict')
def set_dispersion_correction_to_system(item, value=None):

    item['dispersion_correction'] = value

    pass

@digest(form='molsysmt.MolecularMechanicsDict')
def set_ewald_error_tolerance_to_system(item, value=None):

    item['ewald_error_tolerance'] = value

    pass

@digest(form='molsysmt.MolecularMechanicsDict')
def set_hydrogen_mass_to_system(item, value=None):

    item['hydrogen_mass'] = value

    pass


@digest(form='molsysmt.MolecularMechanicsDict')
def set_constraints_to_system(item, value=None):

    item['constraints'] = value

    pass

@digest(form='molsysmt.MolecularMechanicsDict')
def set_flexible_constraints_to_system(item, value=None):

    item['flexible_constraints'] = value

    pass

@digest(form='molsysmt.MolecularMechanicsDict')
def set_water_model_to_system(item, value=None):

    item['water_model'] = value

    pass

@digest(form='molsysmt.MolecularMechanicsDict')
def set_rigid_water_to_system(item, value=None):

    item['rigid_water'] = value

    pass

@digest(form='molsysmt.MolecularMechanicsDict')
def set_implicit_solvent_to_system(item, value=None):

    item['implicit_solvent'] = value

    pass

@digest(form='molsysmt.MolecularMechanicsDict')
def set_solute_dielectric_to_system(item, value=None):

    item['solute_dielectric'] = value

    pass

@digest(form='molsysmt.MolecularMechanicsDict')
def set_solvent_dielectric_to_system(item, value=None):

    item['solvent_dielectric'] = value

    pass

@digest(form='molsysmt.MolecularMechanicsDict')
def set_salt_concentration_to_system(item, value=None):

    item['salt_concentration'] = value

    pass

@digest(form='molsysmt.MolecularMechanicsDict')
def set_kappa_to_system(item, value=None):

    item['kappa'] = value

    pass

















