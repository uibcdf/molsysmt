import numpy as np
from ...exceptions import ArgumentError
from ...variables import is_all


def digest_structure_indices(structure_indices, caller=None):
    """ Checks if atom_indices has the expected type and value.

    Parameters
    ----------
    structure_indices : str or int or list or tuple or range.
        The structure indices.

    caller: str, optional
        Name of the function or method that is being digested.
        For debugging purposes.

    Returns
    -------
    str or ndarray or None
        Either None, 'all' or an numpy array of integers with the indices.

    Raises
    -------
    WrongIndicesError
        If the given structure_indices has not of the correct type.
    """

    if structure_indices is None:
        return None
    elif is_all(structure_indices):
        return 'all'
    elif isinstance(structure_indices, (int, np.int64, np.int32)):
        return np.array([structure_indices], dtype='int64')
    elif isinstance(structure_indices, (np.ndarray, list, tuple, range)):
        if all(isinstance(ii, (int, np.int64, np.int32)) for ii in structure_indices):
            return np.array(structure_indices, dtype='int64')
        else:
            return [digest_structure_indices(ii) for ii in structure_indices]

    raise ArgumentError('structure_indices', caller=caller, message=None)

