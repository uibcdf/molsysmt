from ...exceptions import ArgumentError
from ...variables import is_all
import numpy as np

def digest_groups_of_atoms(groups_of_atoms, caller=None):

    from .indices import digest_indices

    if groups_of_atoms is None:
        return None
    elif isinstance(groups_of_atoms, (np.ndarray, list, tuple, range)):
        try:
            return [digest_indices(ii, caller=caller) for ii in groups_of_atoms]
        except:
            raise ArgumentError('groups_of_atoms', value=groups_of_atoms, caller=caller, message=None)

    raise ArgumentError('groups_of_atoms', value=groups_of_atoms, caller=caller, message=None)

