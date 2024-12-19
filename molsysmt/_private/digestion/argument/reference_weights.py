import numpy as np
from ...exceptions import ArgumentError

def digest_reference_weights(reference_weights, caller=None):

    from .weights import digest_weights

    try:
        return digest_weights(reference_weights, caller=caller)
    except:
        raise ArgumentError('reference_weights', value=reference_weights, caller=caller, message=None)

