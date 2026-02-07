import numpy as np
from molsysmt._private.smonitor import ArgumentError

def digest_reference_weights(reference_weights, caller=None):

    from .weights import arg_digest_weights

    try:
        return digest_weights(reference_weights, caller=caller)
    except:
        raise ArgumentError('reference_weights', value=reference_weights, caller=caller, message=None)

