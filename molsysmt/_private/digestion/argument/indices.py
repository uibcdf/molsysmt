import numpy as np
from molsysmt._private.exceptions import ArgumentError
from molsysmt._private.variables import is_all, is_iterable_of_iterables

def digest_indices(indices, caller=None):
    """ Checks if indices has the expected type and value.

        Parameters
        ----------
        indices : str or int or list or tuple or range.
            The indices.

        caller: str, optional
            Name of the function or method that is being digested.

        Returns
        -------
        str or np.ndarray
            Either 'all' or an array with the indices.

        Raises
        -------
        WrongIndicesError
            If the given indices are not of the correct type.
    """
    if indices is None:
        return None
    elif is_all(indices):
        return 'all'
    elif isinstance(indices, (int, np.int64, np.int32)):
        return [indices]
    elif isinstance(indices, range):
        return list(indices)
    elif isinstance(indices, tuple):
        return list(indices)
    elif isinstance(indices, np.ndarray):
        return indices.tolist()
    elif isinstance(indices, list):
        return indices

    raise ArgumentError('indices', value=indices, caller=caller, message=None)

