import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_remarks(remarks, caller=None):
    if remarks is None or isinstance(remarks, (list, tuple)):
        return remarks
    if isinstance(remarks, np.ndarray) and remarks.ndim == 1:
        return remarks
    raise ArgumentError("remarks", caller=caller)
