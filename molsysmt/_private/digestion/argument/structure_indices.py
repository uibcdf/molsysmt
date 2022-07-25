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

    # Depending on the method this could digest multiple structure_indices

    if structure_indices is None:
        pass
    elif is_all(structure_indices):
        structure_indices = 'all'
    elif isinstance(structure_indices, (int, np.int64, np.int32)):
        structure_indices = np.array([structure_indices], dtype='int64')
    elif isinstance(structure_indices, (np.ndarray, list, tuple, range)):
        structure_indices = np.array(structure_indices, dtype='int64')
    else:
        raise ArgumentError('structure_indices', caller=caller, message=None)

    return structure_indices

#
#def digest_multiple_structure_indices(structure_indices, caller=None):
#    """ Checks if multiple_structure_indices has the expected type and value.
#
#    Parameters
#    ----------
#    multiple_structure_indices : list or tuple of str, or list or tuple of int, or list or tuple of
#    lists, or list or tuple of tuples, or list or tuple of ranges).
#        The list or tuple of structure indices
#
#    caller: str, optional
#        Name of the function or method that is being digested.
#        For debugging purposes.
#
#    Returns
#    -------
#    list of str or list of ndarrays or None
#        Either None, or a list of 'all' strings and numpy arrays of integers.
#
#    Raises
#    -------
#    WrongStructureIndicesError
#        If the given indices are not of the correct type.
#    """
#
#    if is_list_or_tuple(structure_indices):
#        return [digest_structure_indices(ii, caller=caller) for ii in structure_indices]
#    else:
#        return digest_structure_indices(structure_indices, caller=caller)
