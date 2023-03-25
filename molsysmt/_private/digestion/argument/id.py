from ...exceptions import ArgumentError
from ...variables import is_all
import numpy as np

def digest_id(id, caller=None):

    if isinstance(id, (tuple, list)):
        id=np.ndarray(id)

    if isinstance(id, np.ndarray):
        return id

    raise ArgumentError('id', caller=caller, message=None)

