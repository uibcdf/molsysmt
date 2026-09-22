import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_to_group_names(to_group_names, caller):

    if isinstance(to_group_names, str):
        return [to_group_names]
    elif isinstance(to_group_names, (np.ndarray, list, tuple, range)):
        if all([isinstance(ii, str) for ii in to_group_names]):
            return to_group_names

    raise ArgumentError("group_indices", caller=caller, message=None)
