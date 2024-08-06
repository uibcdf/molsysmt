from ...exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

methods_where_bool = [
]

def digest_origin(origin, caller=None):

    if caller in methods_where_bool:
        if isinstance(origin, bool):
            return origin

    if caller.endswith('add_arrows'):
        if origin is None:
            return None

    value = puw.get_value(origin)
    unit = puw.get_unit(origin)

    if not puw.check(unit, dimensionality={'[L]':1}):
        raise ArgumentError('origin', value=origin, caller=caller, message=None)

    if not isinstance(value, np.ndarray):
        value = np.array(value)

    shape = value.shape

    if len(shape) == 1:
        if shape[0] == 3:
            return puw.quantity(value[np.newaxis, np.newaxis, :], unit, standardized=True)
    elif len(shape) == 2:
        if shape[1] == 3:
            return puw.quantity(value[np.newaxis, :, :], unit, standardized=True)
    elif len(shape) == 3:
        if shape[2] == 3:
            return puw.quantity(value, unit, standardized=True)

    raise ArgumentError('origin', value=origin, caller=caller, message=None)

