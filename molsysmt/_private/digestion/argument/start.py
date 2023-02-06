import numpy as np
from molsysmt._private.exceptions import ArgumentError

def digest_start(start, caller=None):

    if isinstance(start, (int, np.int64, np.int32)):
        return start

    raise ArgumentError('start', value=start, caller=caller, message=None)

