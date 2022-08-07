import numpy as np
from ...exceptions import ArgumentError
from ...variables import is_all


def digest_structure_indices_A(structure_indices_A, caller=None):
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

    # Depending on the method this could digest multiple structure_indices

    if structure_indices_A is None:
        return None
    elif is_all(structure_indices_A):
        return 'all'
    elif isinstance(structure_indices_A, (int, np.int64, np.int32)):
        return np.array([structure_indices_A], dtype='int64')
    elif isinstance(structure_indices_A, (np.ndarray, list, tuple, range)):
        return np.array(structure_indices_A, dtype='int64')

    raise ArgumentError('structure_indices_A', value=structure_indices_A, caller=caller, message=None)

