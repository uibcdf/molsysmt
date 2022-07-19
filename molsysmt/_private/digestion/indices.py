import numpy as np
from ..exceptions import WrongIndicesError
from ..lists_and_tuples import is_list_or_tuple

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
        return

    if isinstance(indices, str):
        if indices.lower() == 'all':
            return 'all'
        else:
            raise WrongIndicesError(type(indices), caller)
    elif isinstance(indices, (int, np.int64, np.int32)):
        indices = np.array([indices], dtype='int64')
    elif isinstance(indices, (np.ndarray, list, tuple, range)):
        indices = np.array(indices, dtype='int64')
    else:
        raise WrongIndicesError(type(indices), caller)

    return indices

