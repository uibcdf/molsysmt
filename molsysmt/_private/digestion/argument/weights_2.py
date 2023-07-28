from molsysmt._private.exceptions import ArgumentError
import numpy as np

def digest_weights_2(weights_2, syntax="MolSysMT", caller=None):

    if weights_2 is None:
        return None

    from .weights import digest_weights

    try:
        return digest_weights(weights_2, syntax=syntax, caller=caller)
    except:
        raise ArgumentError('weights_2', value=weights_2, caller=caller, message=None)

