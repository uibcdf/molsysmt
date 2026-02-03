from ...exceptions import ArgumentError
from ...variables import is_all
import numpy as np

def digest_to_group_names(to_group_names, caller):

    if isinstance(to_group_names, str):
        return [to_group_names]
    elif isinstance(to_group_names, (np.ndarray, list, tuple, range)):
        if all([isinstance(ii, str) for ii in to_group_names]):
            return to_group_names

    raise ArgumentError('group_indices', caller=caller, message=None)

