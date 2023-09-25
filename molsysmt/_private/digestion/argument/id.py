from ...exceptions import ArgumentError
from ...variables import is_all
import numpy as np

def digest_id(id, caller=None):

    if caller.endswith('.define_new_chain'):
        from .chain_id import digest_chain_id
        return digest_chain_id(id, caller=caller)

    if isinstance(id, (tuple, list)):
        id=np.ndarray(id)

    if isinstance(id, np.ndarray):
        return id

    raise ArgumentError('id', caller=caller, message=None)

