from molsysmt._private.exceptions import ArgumentError
from molsysmt._private.variables import is_iterable
import numpy as np

def digest_donors(donors, syntax="MolSysMT", caller=None):
    """
    """

    if syntax=='MolSysMT':
        if isinstance(donors, str):
            return donors
        elif isinstance(donors, (int, np.int64, np.int32)):
            return [donors]
        elif is_iterable(donors):
            if all([isinstance(ii, (int, np.int64, np.int32)) for ii in donors]):
                return list(donors)
            else:
                return list([digest_donors(ii, syntax=syntax, caller=caller) for ii in donors])
        elif isinstance(donors, range):
            return list(donors)
        elif donors is None:
            return None
    else:
        if isinstance(donors, str):
            return donors
        elif isinstance(donors, (int, np.int64, np.int32)):
            return np.array([donors], dtype='int64')
        elif isinstance(donors, (np.ndarray, list, tuple, range)):
            return np.array(donors, dtype='int64')
        elif isinstance(donors, range):
            return list(donors)
        elif donors is None:
            return None

    raise ArgumentError('donors', value=donors, caller=caller, message=None)

