from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

###### Set

###
## Atom
###

# Mechanical

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def set_formal_charge_to_atom(item, atom_indices='all', value=None, skip_digestion=False):

    """
    Setting formal charge to atom on form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    if is_all(atom_indices):

        item['formal_charge'] = value

    else:

        item['formal_charge'][atom_indices] = value

    pass

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def set_partial_charge_to_atom(item, atom_indices='all', value=None, skip_digestion=False):

    """
    Setting partial charge to atom on form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    if is_all(atom_indices):

        item['partial_charge'] = value

    else:

        item['partial_charge'][atom_indices] = value

    pass

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def set_atom_ff_type_to_atom(item, atom_indices='all', value=None, skip_digestion=False):

    """
    Setting atom ff type to atom on form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    if is_all(atom_indices):

        item['atom_ff_type'] = value

    else:

        item['atom_ff_type'][atom_indices] = value

    pass

###
### System
###

# Mechanical

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def set_forcefield_to_system(item, value=None, skip_digestion=False):

    """
    Setting forcefield to system on form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item['forcefield'] = value

    pass

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def set_non_bonded_method_to_system(item, value=None, skip_digestion=False):

    """
    Setting non bonded method to system on form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item['non_bonded_method'] = value

    pass

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def set_cutoff_distance_to_system(item, value=None, skip_digestion=False):

    """
    Setting cutoff distance to system on form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item['cutoff_distance'] = value

    pass

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def set_switch_distance_to_system(item, value=None, skip_digestion=False):

    """
    Setting switch distance to system on form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item['switch_distance'] = value

    pass

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def set_dispersion_correction_to_system(item, value=None, skip_digestion=False):

    """
    Setting dispersion correction to system on form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item['dispersion_correction'] = value

    pass

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def set_ewald_error_tolerance_to_system(item, value=None, skip_digestion=False):

    """
    Setting ewald error tolerance to system on form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item['ewald_error_tolerance'] = value

    pass

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def set_hydrogen_mass_to_system(item, value=None, skip_digestion=False):

    """
    Setting hydrogen mass to system on form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item['hydrogen_mass'] = value

    pass


@arg_digest(form='molsysmt.MolecularMechanicsDict')
def set_constraints_to_system(item, value=None, skip_digestion=False):

    """
    Setting constraints to system on form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item['constraints'] = value

    pass

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def set_flexible_constraints_to_system(item, value=None, skip_digestion=False):

    """
    Setting flexible constraints to system on form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item['flexible_constraints'] = value

    pass

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def set_water_model_to_system(item, value=None, skip_digestion=False):

    """
    Setting water model to system on form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item['water_model'] = value

    pass

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def set_rigid_water_to_system(item, value=None, skip_digestion=False):

    """
    Setting rigid water to system on form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item['rigid_water'] = value

    pass

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def set_implicit_solvent_to_system(item, value=None, skip_digestion=False):

    """
    Setting implicit solvent to system on form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item['implicit_solvent'] = value

    pass

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def set_solute_dielectric_to_system(item, value=None, skip_digestion=False):

    """
    Setting solute dielectric to system on form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item['solute_dielectric'] = value

    pass

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def set_solvent_dielectric_to_system(item, value=None, skip_digestion=False):

    """
    Setting solvent dielectric to system on form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item['solvent_dielectric'] = value

    pass

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def set_salt_concentration_to_system(item, value=None, skip_digestion=False):

    """
    Setting salt concentration to system on form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item['salt_concentration'] = value

    pass

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def set_kappa_to_system(item, value=None, skip_digestion=False):

    """
    Setting kappa to system on form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item['kappa'] = value

    pass

















