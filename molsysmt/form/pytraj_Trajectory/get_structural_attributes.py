from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='pytraj.Trajectory'


@arg_digest(form=form)
def get_coordinates_from_atom(
    item,
    indices='all',
    structure_indices='all',
    skip_digestion=False,
):
    """
    Getting coordinates from atom in form pytraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """

    coordinates = item.xyz
    if not is_all(structure_indices):
        coordinates = coordinates[structure_indices, :, :]
    if not is_all(indices):
        coordinates = coordinates[:, indices, :]

    coordinates = puw.quantity(coordinates, 'angstrom')
    return puw.standardize(coordinates)


@arg_digest(form=form)
def get_n_structures_from_system(
    item,
    structure_indices='all',
    skip_digestion=False,
):
    """
    Getting n structures from system in form pytraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """

    if is_all(structure_indices):
        return item.n_frames
    return len(structure_indices)


@arg_digest(form=form)
def get_box_from_system(
    item,
    structure_indices='all',
    skip_digestion=False,
):
    """
    Getting box from system in form pytraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """

    unitcells = item.unitcells
    if unitcells is None:
        return None
    if not is_all(structure_indices):
        unitcells = unitcells[structure_indices, :]

    from molsysmt.pbc import get_box_from_lengths_and_angles

    box_lengths = puw.quantity(np.asarray(unitcells[:, :3]), 'angstrom')
    box_angles = puw.quantity(np.asarray(unitcells[:, 3:]), 'degree')
    return get_box_from_lengths_and_angles(
        box_lengths,
        box_angles,
        skip_digestion=True,
    )


@arg_digest(form=form)
def get_time_from_system(
    item,
    structure_indices='all',
    skip_digestion=False,
):
    """
    Getting time from system in form pytraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """

    if item.time is None:
        return None
    time = item.time
    if not is_all(structure_indices):
        time = time[structure_indices]
    return puw.standardize(puw.quantity(time, 'picosecond'))


@arg_digest(form=form)
def get_structure_id_from_system(
    item,
    structure_indices='all',
    skip_digestion=False,
):
    """
    Getting structure id from system in form pytraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """

    return None


# List of functions to be imported
import types
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
