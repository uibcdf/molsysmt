import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_id(id, caller=None):

    if isinstance(id, (tuple, list)):
        id = np.array(id)

    if isinstance(id, np.ndarray):
        return id

    raise ArgumentError("id", caller=caller, message=None)
