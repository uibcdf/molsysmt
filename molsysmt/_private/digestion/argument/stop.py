import numpy as np
from molsysmt._private.exceptions import ArgumentError

def digest_stop(stop, caller=None):

    if stop is None:
        return None

    if isinstance(stop, (int, np.int64, np.int32)):
        return stop

    raise ArgumentError('stop', value=stop, caller=caller, message=None)

