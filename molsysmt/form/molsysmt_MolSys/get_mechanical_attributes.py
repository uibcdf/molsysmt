from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np
import types

form = 'molsysmt.MolSys'


#######################################################################
#                 To be customized for each form                      #
#######################################################################


# From atom


# From system


@digest(form=form)
def get_forcefield_from_system(item, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import get_forcefield_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@digest(form=form)
def get_non_bonded_method_from_system(item, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import get_non_bonded_method_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@digest(form=form)
def get_cutoff_distance_from_system(item, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import get_cutoff_distance_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@digest(form=form)
def get_switch_distance_from_system(item, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import get_switch_distance_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@digest(form=form)
def get_dispersion_correction_from_system(item, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import get_dispersion_correction_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@digest(form=form)
def get_ewald_error_tolerance_from_system(item, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import get_ewald_error_tolerance_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@digest(form=form)
def get_hydrogen_mass_from_system(item, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import get_hydrogen_mass_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@digest(form=form)
def get_constraints_from_system(item, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import get_constraints_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@digest(form=form)
def get_flexible_constraints_from_system(item, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import get_flexible_constraints_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@digest(form=form)
def get_water_model_from_system(item, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import get_water_model_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@digest(form=form)
def get_rigid_water_from_system(item, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import get_rigid_water_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@digest(form=form)
def get_implicit_solvent_from_system(item, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import get_implicit_solvent_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@digest(form=form)
def get_solute_dielectric_from_system(item, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import get_solute_dielectric_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@digest(form=form)
def get_solvent_dielectric_from_system(item, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import get_solvent_dielectric_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@digest(form=form)
def get_salt_concentration_from_system(item, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import get_salt_concentration_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@digest(form=form)
def get_kappa_from_system(item, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import get_kappa_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

# List of functions to be imported


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]

