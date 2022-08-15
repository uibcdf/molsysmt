from molsysmt._private.exceptions import ArgumentError
from molsysmt._private.variables import is_all
import numpy as np

def digest_blocks(blocks, caller=None):

    if blocks is None:
        return None

    if isinstance(blocks, (list, tuple, np.ndarray)):
        if np.all([isinstance(ii, (list, tuple, np.ndarray)) for ii in blocks]):
            return blocks

    raise ArgumentError('blocks', value=blocks, caller=caller, message=None)
