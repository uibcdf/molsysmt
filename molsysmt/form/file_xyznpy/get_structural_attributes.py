from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import types

form = 'file:xyznpy'


def _read_shape(item):
    with open(item, 'rb') as file:
        return tuple(int(value) for value in np.load(file))


def _read_coordinates(item):
    with open(item, 'rb') as file:
        np.load(file)
        coordinates = np.load(file)
    return puw.standardize(coordinates * puw.unit('nm'))


@arg_digest(form=form)
def get_n_structures_from_system(
    item, structure_indices='all', skip_digestion=False
):
    """
    Getting n structures from system in form file:xyznpy.

    Parameters
    ----------
    item : file:xyznpy
        Source item in file:xyznpy form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if is_all(structure_indices):
        return _read_shape(item)[0]
    return len(structure_indices)


@arg_digest(form=form)
def get_structure_index_from_system(
    item, structure_indices='all', skip_digestion=False
):
    """
    Getting structure index from system in form file:xyznpy.

    Parameters
    ----------
    item : file:xyznpy
        Source item in file:xyznpy form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = np.arange(_read_shape(item)[0], dtype=int)
    if not is_all(structure_indices):
        output = output[structure_indices]
    return output.tolist()


@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    """
    Getting coordinates from atom in form file:xyznpy.

    Parameters
    ----------
    item : file:xyznpy
        Source item in file:xyznpy form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices is None or structure_indices is None:
        return None

    output = _read_coordinates(item)
    if not is_all(structure_indices):
        if not is_all(indices):
            output = output[np.ix_(structure_indices, indices)]
        else:
            output = output[structure_indices, :, :]
    elif not is_all(indices):
        output = output[:, indices, :]
    return output


@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting coordinates from system in form file:xyznpy.

    Parameters
    ----------
    item : file:xyznpy
        Source item in file:xyznpy form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if structure_indices is None:
        return None

    output = _read_coordinates(item)
    if not is_all(structure_indices):
        output = output[structure_indices, :, :]
    return output


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
