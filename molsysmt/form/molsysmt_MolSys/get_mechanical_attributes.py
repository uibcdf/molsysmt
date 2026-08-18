from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
import numpy as np
import types

form = 'molsysmt.MolSys'


#######################################################################
#                 To be customized for each form                      #
#######################################################################


# From atom

@arg_digest(form=form)
def get_formal_charge_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting formal charge from atom in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_Topology import get_formal_charge_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_partial_charge_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting partial charge from atom in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolecularMechanics import get_partial_charge_from_atom as aux_get
    return aux_get(item.molecular_mechanics, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_atom_ff_type_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting atom ff type from atom in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolecularMechanics import get_atom_ff_type_from_atom as aux_get
    return aux_get(item.molecular_mechanics, indices=indices, skip_digestion=True)


# From system

@arg_digest(form=form)
def get_formal_charge_from_system(item, skip_digestion=False):
    """
    Getting formal charge from system in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_formal_charge_from_atom(item, skip_digestion=True)


@arg_digest(form=form)
def get_partial_charge_from_system(item, skip_digestion=False):
    """
    Getting partial charge from system in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_partial_charge_from_atom(item, skip_digestion=True)


@arg_digest(form=form)
def get_atom_ff_type_from_system(item, skip_digestion=False):
    """
    Getting atom ff type from system in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_atom_ff_type_from_atom(item, skip_digestion=True)


@arg_digest(form=form)
def get_forcefield_from_system(item, skip_digestion=False):

    """
    Getting forcefield from system in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolecularMechanics import get_forcefield_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@arg_digest(form=form)
def get_non_bonded_method_from_system(item, skip_digestion=False):

    """
    Getting non bonded method from system in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolecularMechanics import get_non_bonded_method_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@arg_digest(form=form)
def get_cutoff_distance_from_system(item, skip_digestion=False):

    """
    Getting cutoff distance from system in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolecularMechanics import get_cutoff_distance_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@arg_digest(form=form)
def get_switch_distance_from_system(item, skip_digestion=False):

    """
    Getting switch distance from system in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolecularMechanics import get_switch_distance_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@arg_digest(form=form)
def get_dispersion_correction_from_system(item, skip_digestion=False):

    """
    Getting dispersion correction from system in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolecularMechanics import get_dispersion_correction_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@arg_digest(form=form)
def get_ewald_error_tolerance_from_system(item, skip_digestion=False):

    """
    Getting ewald error tolerance from system in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolecularMechanics import get_ewald_error_tolerance_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@arg_digest(form=form)
def get_hydrogen_mass_from_system(item, skip_digestion=False):

    """
    Getting hydrogen mass from system in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolecularMechanics import get_hydrogen_mass_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@arg_digest(form=form)
def get_constraints_from_system(item, skip_digestion=False):

    """
    Getting constraints from system in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolecularMechanics import get_constraints_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@arg_digest(form=form)
def get_flexible_constraints_from_system(item, skip_digestion=False):

    """
    Getting flexible constraints from system in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolecularMechanics import get_flexible_constraints_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@arg_digest(form=form)
def get_water_model_from_system(item, skip_digestion=False):

    """
    Getting water model from system in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolecularMechanics import get_water_model_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@arg_digest(form=form)
def get_rigid_water_from_system(item, skip_digestion=False):

    """
    Getting rigid water from system in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolecularMechanics import get_rigid_water_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@arg_digest(form=form)
def get_implicit_solvent_from_system(item, skip_digestion=False):

    """
    Getting implicit solvent from system in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolecularMechanics import get_implicit_solvent_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@arg_digest(form=form)
def get_solute_dielectric_from_system(item, skip_digestion=False):

    """
    Getting solute dielectric from system in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolecularMechanics import get_solute_dielectric_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@arg_digest(form=form)
def get_solvent_dielectric_from_system(item, skip_digestion=False):

    """
    Getting solvent dielectric from system in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolecularMechanics import get_solvent_dielectric_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@arg_digest(form=form)
def get_salt_concentration_from_system(item, skip_digestion=False):

    """
    Getting salt concentration from system in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolecularMechanics import get_salt_concentration_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

@arg_digest(form=form)
def get_kappa_from_system(item, skip_digestion=False):

    """
    Getting kappa from system in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolecularMechanics import get_kappa_from_system as aux_get
    return aux_get(item.molecular_mechanics, skip_digestion=True)

# List of functions to be imported


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
