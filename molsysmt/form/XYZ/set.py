from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
import numpy as np

###### Set

## Atom

@arg_digest(form='XYZ')
def set_coordinates_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    """
    Setting coordinates to atom on form XYZ.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    value : object, default=None
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        if is_all(structure_indices):
            item[:,:,:]=value[:,:,:]
        else:
            item[structure_indices,:,:] = value[:,:,:]
    else:
        if is_all(structure_indices):
            item[:,indices,:] = value[:,:,:]
        else:
            item[np.ix_(structure_indices, indices)]=value[:,:,:]

    pass

## System

@arg_digest(form='XYZ')
def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    """
    Setting coordinates to system on form XYZ.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    value : object, default=None
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    return set_coordinates_to_atom(item, indices='all', structure_indices=structure_indices,
            value=value)


