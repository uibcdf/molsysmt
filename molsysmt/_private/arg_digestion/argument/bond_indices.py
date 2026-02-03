from ...exceptions import ArgumentError
from ...variables import is_all
import numpy as np

def digest_bond_indices(bond_indices, caller=None):
    """ Checks if bond_indices has the expected type and value.

    Parameters
    ----------
    indices : str or int or list or tuple or range.
        The indices

    caller: str, optional
        Name of the function or method that is being digested.
        For debugging purposes.

    Returns
    -------
    str or ndarray or None
        Either None, 'all' or an numpy array of integers with the indices.

    Raises
    -------
    ArgumentError
        If the given indices are not of the correct type.
    """

    if bond_indices is None:
        return None
    elif is_all(bond_indices):
        return 'all'
    elif isinstance(bond_indices, (int, np.int64, np.int32)):
        return np.array([bond_indices], dtype='int64')
    elif isinstance(bond_indices, (np.ndarray, list, tuple, range)):
        if all(isinstance(ii, (int, np.int64, np.int32)) for ii in bond_indices):
            return np.array(bond_indices, dtype='int64')
        else:
            return [digest_bond_indices(ii) for ii in bond_indices]

    raise ArgumentError('bond_indices', caller=caller, message=None)

