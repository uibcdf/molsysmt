from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

###### Set

## Atom

@arg_digest(form='molsysmt.Structures')
def set_coordinates_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    """
    Setting coordinates to atom on form molsysmt.Structures.

    Parameters
    ----------
    item : molsysmt.Structures
        Source item in molsysmt.Structures form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item.set_coordinates(indices=indices, structure_indices=structure_indices, value=value,
                         skip_digestion=True)

@arg_digest(form='molsysmt.Structures')
def set_velocities_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    """
    Setting velocities to atom on form molsysmt.Structures.

    Parameters
    ----------
    item : molsysmt.Structures
        Source item in molsysmt.Structures form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item.set_velocities(indices=indices, structure_indices=structure_indices, value=value,
                         skip_digestion=True)

@arg_digest(form='molsysmt.Structures')
def set_occupancy_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    """
    Setting occupancy to atom on form molsysmt.Structures.

    Parameters
    ----------
    item : molsysmt.Structures
        Source item in molsysmt.Structures form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item.set_occupancy(indices=indices, structure_indices=structure_indices, value=value,
                       skip_digestion=True)

@arg_digest(form='molsysmt.Structures')
def set_b_factor_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    """
    Setting b factor to atom on form molsysmt.Structures.

    Parameters
    ----------
    item : molsysmt.Structures
        Source item in molsysmt.Structures form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item.set_b_factor(indices=indices, structure_indices=structure_indices, value=value,
                      skip_digestion=True)

## System

@arg_digest(form='molsysmt.Structures')
def set_structure_id_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    """
    Setting structure id to system on form molsysmt.Structures.

    Parameters
    ----------
    item : molsysmt.Structures
        Source item in molsysmt.Structures form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item.set_structure_id(structure_indices=structure_indices, value=value, skip_digestion=True)

@arg_digest(form='molsysmt.Structures')
def set_time_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    """
    Setting time to system on form molsysmt.Structures.

    Parameters
    ----------
    item : molsysmt.Structures
        Source item in molsysmt.Structures form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item.set_time(structure_indices=structure_indices, value=value, skip_digestion=True)

@arg_digest(form='molsysmt.Structures')
def set_box_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    """
    Setting box to system on form molsysmt.Structures.

    Parameters
    ----------
    item : molsysmt.Structures
        Source item in molsysmt.Structures form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    item.set_box(structure_indices=structure_indices, value=value, skip_digestion=True)

@arg_digest(form='molsysmt.Structures')
def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    """
    Setting coordinates to system on form molsysmt.Structures.

    Parameters
    ----------
    item : molsysmt.Structures
        Source item in molsysmt.Structures form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    return set_coordinates_to_atom(item, indices='all', structure_indices=structure_indices,
            value=value, skip_digestion=True)

@arg_digest(form='molsysmt.Structures')
def set_velocities_to_system(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    """
    Setting velocities to system on form molsysmt.Structures.

    Parameters
    ----------
    item : molsysmt.Structures
        Source item in molsysmt.Structures form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    return set_velocities_to_atom(item, indices='all', structure_indices=structure_indices,
            value=value, skip_digestion=True)

