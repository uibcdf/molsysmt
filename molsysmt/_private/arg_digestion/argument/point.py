from ...exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_point(point, caller=None):

    if point is None:
        return None

    value, unit = puw.get_value_and_unit(point)

    if not puw.check(unit, dimensionality={'[L]':1}):
        raise ArgumentError('point', value=point, caller=caller, message=None)

    if not isinstance(value, np.ndarray):
        value = np.array(value)


    value = value.astype(np.float64)
    shape = value.shape

    if len(shape) == 1:
        if shape[0] == 3:
            return puw.quantity(value[np.newaxis, :], unit, standardized=True)
    elif len(shape) == 2:
        if shape[1] == 3:
            return puw.quantity(value, unit, standardized=True)

    raise ArgumentError('point', value=point, caller=caller, message=None)

