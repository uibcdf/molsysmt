from molsysmt._private.smonitor import ArgumentError
from ...variables import is_all
import numpy as np

def digest_name(name, caller=None):

    if isinstance(name, (tuple, list)):
        name=np.ndarray(name)

    if isinstance(name, np.ndarray):
        return name

    raise ArgumentError('name', caller=caller, message=None)
