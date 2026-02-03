from molsysmt._private.exceptions import ArgumentError
from molsysmt._private.variables import is_iterable
import numpy as np

def digest_acceptors(acceptors, syntax="MolSysMT", caller=None):
    """
    """

    if syntax=='MolSysMT':
        if isinstance(acceptors, str):
            return acceptors
        elif isinstance(acceptors, (int, np.int64, np.int32)):
            return [acceptors]
        elif is_iterable(acceptors):
            if all([isinstance(ii, (int, np.int64, np.int32)) for ii in acceptors]):
                return list(acceptors)
            else:
                return list([digest_acceptors(ii, syntax=syntax, caller=caller) for ii in acceptors])
        elif isinstance(acceptors, range):
            return list(acceptors)
        elif acceptors is None:
            return None
    else:
        if isinstance(acceptors, str):
            return acceptors
        elif isinstance(acceptors, (int, np.int64, np.int32)):
            return np.array([acceptors], dtype='int64')
        elif isinstance(acceptors, (np.ndarray, list, tuple, range)):
            return np.array(acceptors, dtype='int64')
        elif isinstance(acceptors, range):
            return list(acceptors)
        elif acceptors is None:
            return None

    raise ArgumentError('acceptors', value=acceptors, caller=caller, message=None)

