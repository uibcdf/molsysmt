from ...exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

methods_where_bool = [
]

def digest_arrows(arrows, caller=None):

    if caller in methods_where_bool:
        if isinstance(arrows, bool):
            return arrows

    value = puw.get_value(arrows)
    unit = puw.get_unit(arrows)

    if not puw.check(unit, dimensionality={'[L]':1}):
        raise ArgumentError('arrows', value=arrows, caller=caller, message=None)

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

    raise ArgumentError('arrows', value=arrows, caller=caller, message=None)

