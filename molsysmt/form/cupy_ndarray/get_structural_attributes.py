from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form = 'cupy_ndarray'

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    """
    Getting coordinates from atom in form cupy_ndarray.

    Parameters
    ----------
    item : cupy_ndarray
        Source item in cupy_ndarray form.
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
    val = puw.get_value(item)
    unit = puw.get_unit(item)
    
    if len(val.shape) == 1:
        tmp = val[np.newaxis, np.newaxis, :]
    elif len(val.shape) == 2:
        tmp = val[np.newaxis, :, :]
    else:
        tmp = val
        
    if not is_all(indices):
        tmp = tmp[:, indices, :]
    if not is_all(structure_indices):
        tmp = tmp[structure_indices, :, :]
        
    return puw.quantity(tmp, unit)

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting n structures from system in form cupy_ndarray.

    Parameters
    ----------
    item : cupy_ndarray
        Source item in cupy_ndarray form.
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
        val = puw.get_value(item)
        if len(val.shape) == 3:
            return val.shape[0]
        return 1
    else:
        return len(structure_indices)
