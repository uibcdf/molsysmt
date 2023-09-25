from ...exceptions import ArgumentError
from ...variables import is_all
import numpy as np

def digest_name(name, caller=None):

    if caller.endswith('.define_new_chain'):
        from .chain_name import digest_chain_name
        return digest_chain_name(name, caller=caller)

    if isinstance(name, (tuple, list)):
        name=np.ndarray(name)

    if isinstance(name, np.ndarray):
        return name

    raise ArgumentError('name', caller=caller, message=None)

