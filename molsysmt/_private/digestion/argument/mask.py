from molsysmt._private.exceptions import ArgumentError
from molsysmt._private.variables import is_all
import numpy as np

def digest_mask(mask, caller=None):

    if caller in ['molsysmt.basic.select.select', 'molsysmt.basic.get.get']:

        if mask is None:
            return mask
        elif isinstance(mask, (str, list, tuple, np.ndarray)):
            return mask
        elif is_all(mask):
            return 'all'

    else:

        if mask is None:
            return mask
        elif isinstance(mask, (list, tuple, np.ndarray)):
            return mask
        elif is_all(mask):
            return 'all'

    raise ArgumentError('mask', value=mask, caller=caller, message=None)
