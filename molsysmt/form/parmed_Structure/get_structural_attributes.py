"""Delivering ParmEd coordinate frames, unit cells, and B factors."""

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

form = 'parmed.Structure'


def _selected_frame_indices(item, structure_indices):
    coordinates = item.get_coordinates('all')
    n_structures = 0 if coordinates is None else coordinates.shape[0]
    if is_all(structure_indices):
        return np.arange(n_structures, dtype=np.int64)
    return np.asarray(structure_indices, dtype=np.int64)


@arg_digest(form=form)
def get_coordinates_from_atom(
    item, indices='all', structure_indices='all', skip_digestion=False
):
    """
    Getting coordinates from atom in form parmed.Structure.


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

    coordinates = item.get_coordinates('all')
    if coordinates is None:
        return None
    frame_indices = _selected_frame_indices(item, structure_indices)
    coordinates = np.asarray(coordinates[frame_indices], dtype=np.float64)
    if not is_all(indices):
        coordinates = coordinates[:, indices, :]
    return puw.standardize(puw.quantity(coordinates, 'angstrom'))


@arg_digest(form=form)
def get_structure_id_from_system(
    item, structure_indices='all', skip_digestion=False
):
    """
    Getting structure id from system in form parmed.Structure.


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

    return _selected_frame_indices(item, structure_indices)


@arg_digest(form=form)
def get_structure_index_from_system(
    item, structure_indices='all', skip_digestion=False
):
    """
    Getting structure index from system in form parmed.Structure.


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

    return _selected_frame_indices(item, structure_indices)


@arg_digest(form=form)
def get_n_structures_from_system(
    item, structure_indices='all', skip_digestion=False
):
    """
    Getting n structures from system in form parmed.Structure.


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

    return len(_selected_frame_indices(item, structure_indices))


@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting time from system in form parmed.Structure.


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


@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting box from system in form parmed.Structure.


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

    boxes = item.get_box('all')
    if boxes is None:
        return None
    if is_all(structure_indices):
        structure_indices = np.arange(len(boxes), dtype=np.int64)
    boxes = np.asarray(boxes, dtype=np.float64)[structure_indices]
    from molsysmt.pbc import get_box_from_lengths_and_angles

    return get_box_from_lengths_and_angles(
        puw.quantity(boxes[:, :3], 'angstrom'),
        puw.quantity(boxes[:, 3:], 'degree'),
        skip_digestion=True,
    )


@arg_digest(form=form)
def get_b_factor_from_atom(
    item, indices='all', structure_indices='all', skip_digestion=False
):
    """
    Getting b factor from atom in form parmed.Structure.


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

    frame_indices = _selected_frame_indices(item, structure_indices)
    if len(frame_indices) == 0:
        return None
    values = np.asarray([atom.bfactor for atom in item.atoms], dtype=np.float64)
    if not np.any(values):
        return None
    if not is_all(indices):
        values = values[indices]
    values = np.repeat(values[None, :], len(frame_indices), axis=0)
    return puw.standardize(puw.quantity(values, 'angstrom**2'))
