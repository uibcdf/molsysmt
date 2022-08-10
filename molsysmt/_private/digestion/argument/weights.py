import numpy as np
from ...exceptions import ArgumentError

def digest_weights(weights, caller=None):

    if caller=='molsysmt.structure.get_center.get_center':
        if weights is None:
            return weights
        if isinstance(weights, str):
            if weights in ['masses']:
                return weights

    elif caller=='molsysmt.structure.center.center':
        if weights is None:
            return weights
        if isinstance(weights, str):
            if weights in ['masses']:
                return weights

    if isinstance(weights, (list, tuple, np.ndarray, range)):
        return weights

    raise ArgumentError('weights', value=weights, caller=caller, message=None)

