import numpy as np
from molsysmt._private.exceptions import ArgumentError

def digest_index(index, caller=None):

    if isinstance(index, (int, np.int64, np.int32)):
        return index

    raise ArgumentError('index', value=index, caller=caller, message=None)

