#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.smonitor import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

form='molsysmt.MolecularMechanics'

###
### Atom
###

# Topology

@arg_digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting atom index from atom in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if is_all(indices):

        n_atoms = get_n_atoms_from_system(item, skip_digestion=True)
        return np.arange(0,n_atoms)

    else:

        return indices

@arg_digest(form=form)
def get_n_atoms_from_atom (item, indices='all', skip_digestion=False):

    """
    Getting n atoms from atom in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = None

    if is_all(indices):

        if item.atoms_ff is not None:
            output = len(item.atoms_ff)

    else:

        output = len(indices)

    return output


## Molecular Mechanics

@arg_digest(form=form)
def get_formal_charge_from_atom (item, indices='all', skip_digestion=False):

    """
    Getting formal charge from atom in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    fc = item.formal_charge
    if fc is None:
        return None
    if is_all(indices):
        return fc
    return fc[indices]

@arg_digest(form=form)
def get_partial_charge_from_atom (item, indices='all', skip_digestion=False):

    """
    Getting partial charge from atom in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    pc = item.partial_charge
    if pc is None:
        return None
    if is_all(indices):
        return pc
    return pc[indices]

@arg_digest(form=form)
def get_atom_ff_type_from_atom (item, indices='all', skip_digestion=False):

    """
    Getting atom ff type from atom in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    aft = item.atom_ff_type
    if aft is None:
        return None
    if is_all(indices):
        return aft
    return aft[indices]

###
### System
###

# Topology

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    """
    Getting n atoms from system in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_atoms_from_atom(item, skip_digestion=True)

## Molecular Mechanics

@arg_digest(form=form)
def get_forcefield_from_system(item, skip_digestion=False):          

    """
    Getting forcefield from system in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return item.forcefield

@arg_digest(form=form)
def get_non_bonded_method_from_system(item, skip_digestion=False):

    """
    Getting non bonded method from system in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return item.non_bonded_method

@arg_digest(form=form)
def get_cutoff_distance_from_system(item, skip_digestion=False):

    """
    Getting cutoff distance from system in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return item.cutoff_distance

@arg_digest(form=form)
def get_switch_distance_from_system(item, skip_digestion=False):

    """
    Getting switch distance from system in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return item.switch_distance

@arg_digest(form=form)
def get_dispersion_correction_from_system(item, skip_digestion=False):

    """
    Getting dispersion correction from system in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return item.dispersion_correction

@arg_digest(form=form)
def get_ewald_error_tolerance_from_system(item, skip_digestion=False):

    """
    Getting ewald error tolerance from system in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return item.ewald_error_tolerance

@arg_digest(form=form)
def get_hydrogen_mass_from_system(item, skip_digestion=False):

    """
    Getting hydrogen mass from system in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return item.hydrogen_mass

@arg_digest(form=form)
def get_constraints_from_system(item, skip_digestion=False):

    """
    Getting constraints from system in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return item.constraints

@arg_digest(form=form)
def get_flexible_constraints_from_system(item, skip_digestion=False):

    """
    Getting flexible constraints from system in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return item.flexible_constraints

@arg_digest(form=form)
def get_water_model_from_system(item, skip_digestion=False):

    """
    Getting water model from system in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return item.water_model

@arg_digest(form=form)
def get_rigid_water_from_system(item, skip_digestion=False):

    """
    Getting rigid water from system in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return item.rigid_water

@arg_digest(form=form)
def get_implicit_solvent_from_system(item, skip_digestion=False):

    """
    Getting implicit solvent from system in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return item.implicit_solvent

@arg_digest(form=form)
def get_solute_dielectric_from_system(item, skip_digestion=False):

    """
    Getting solute dielectric from system in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return item.solute_dielectric

@arg_digest(form=form)
def get_solvent_dielectric_from_system(item, skip_digestion=False):

    """
    Getting solvent dielectric from system in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return item.solvent_dielectric

@arg_digest(form=form)
def get_salt_concentration_from_system(item, skip_digestion=False):

    """
    Getting salt concentration from system in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return item.salt_concentration

@arg_digest(form=form)
def get_kappa_from_system(item, skip_digestion=False):

    """
    Getting kappa from system in form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return item.kappa

