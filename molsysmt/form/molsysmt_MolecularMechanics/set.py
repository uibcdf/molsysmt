from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

###### Set

###
## Atom
###

# Mechanical

###
### System
###

# Mechanical

@digest(form='molsysmt.MolecularMechanics')
def set_forcefield_to_system(item, value=None):

    item.forcefield = value

    pass

@digest(form='molsysmt.MolecularMechanics')
def set_non_bonded_method_to_system(item, value=None):

    item.non_bonded_method = value

    pass

@digest(form='molsysmt.MolecularMechanics')
def set_cutoff_distance_to_system(item, value=None):

    item.cutoff_distance = value

    pass

@digest(form='molsysmt.MolecularMechanics')
def set_switch_distance_to_system(item, value=None):

    item.switch_distance = value

    pass

@digest(form='molsysmt.MolecularMechanics')
def set_dispersion_correction_to_system(item, value=None):

    item.dispersion_correction = value

    pass

@digest(form='molsysmt.MolecularMechanics')
def set_ewald_error_tolerance_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_ewald_error_tolerance_to_system as molsysmt_MolecularMechanics_set_ewald_error_tolerance_to_system

    return molsysmt_MolecularMechanics_set_ewald_error_tolerance_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolecularMechanics')
def set_hydrogen_mass_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_hydrogen_mass_to_system as molsysmt_MolecularMechanics_set_hydrogen_mass_to_system

    return molsysmt_MolecularMechanics_set_hydrogen_mass_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolecularMechanics')
def set_constraints_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_constraints_to_system as molsysmt_MolecularMechanics_set_constraints_to_system

    return molsysmt_MolecularMechanics_set_constraints_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolecularMechanics')
def set_flexible_constraints_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_flexible_constraints_to_system as molsysmt_MolecularMechanics_set_flexible_constraints_to_system

    return molsysmt_MolecularMechanics_set_flexible_constraints_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolecularMechanics')
def set_water_model_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_water_model_to_system as molsysmt_MolecularMechanics_set_water_model_to_system

    return molsysmt_MolecularMechanics_set_water_model_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolecularMechanics')
def set_rigid_water_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_rigid_water_to_system as molsysmt_MolecularMechanics_set_rigid_water_to_system

    return molsysmt_MolecularMechanics_set_rigid_water_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolecularMechanics')
def set_implicit_solvent_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_implicit_solvent_to_system as molsysmt_MolecularMechanics_set_implicit_solvent_to_system

    return molsysmt_MolecularMechanics_set_implicit_solvent_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolecularMechanics')
def set_solute_dielectric_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_solute_dielectric_to_system as molsysmt_MolecularMechanics_set_solute_dielectric_to_system

    return molsysmt_MolecularMechanics_set_solute_dielectric_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolecularMechanics')
def set_solvent_dielectric_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_solvent_dielectric_to_system as molsysmt_MolecularMechanics_set_solvent_dielectric_to_system

    return molsysmt_MolecularMechanics_set_solvent_dielectric_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolecularMechanics')
def set_salt_concentration_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_salt_concentration_to_system as molsysmt_MolecularMechanics_set_salt_concentration_to_system

    return molsysmt_MolecularMechanics_set_salt_concentration_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolecularMechanics')
def set_kappa_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_kappa_to_system as molsysmt_MolecularMechanics_set_kappa_to_system

    return molsysmt_MolecularMechanics_set_kappa_to_system(item.molecular_mechanics, value=value)

















