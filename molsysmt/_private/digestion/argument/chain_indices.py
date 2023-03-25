from ...exceptions import ArgumentError
from ...variables import is_all
import numpy as np

def digest_chain_indices(chain_indices, caller=None):
    """ Checks if chain_indices has the expected type and value.

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

    if caller is not None:
        if caller.endswith('digest_bioassembly'):
            if isinstance(chain_indices,(np.ndarray, list, tuple)):
                return [digest_chain_indices(ii) for ii in chain_indices]

    if chain_indices is None:
        return None
    elif is_all(chain_indices):
        return 'all'
    elif isinstance(chain_indices, (int, np.int64, np.int32)):
        return np.array([chain_indices], dtype='int64')
    elif isinstance(chain_indices, (np.ndarray, list, tuple, range)):
        if all(isinstance(ii, (int, np.int64, np.int32)) for ii in chain_indices):
            return np.array(chain_indices, dtype='int64')
        else:
            return [digest_chain_indices(ii) for ii in chain_indices]

    raise ArgumentError('chain_indices', caller=caller, message=None)

