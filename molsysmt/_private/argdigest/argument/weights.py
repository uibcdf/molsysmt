import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError

def digest_weights(weights, caller=None):

    if weights is None:
        return weights

    if isinstance(weights, str):
        if weights in ['masses']:
            return weights

    if isinstance(weights, (list, tuple, np.ndarray, range)):
        return weights

    if puw.is_quantity(weights):
        return weights

    raise ArgumentError('weights', value=weights, caller=caller, message=None)
