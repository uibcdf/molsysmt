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
    item : XYZ
        Source item in XYZ form.
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
    item : XYZ
        Source item in XYZ form.
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
            value=value)


