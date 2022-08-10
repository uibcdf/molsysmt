from ...exceptions import ArgumentError
import numpy as np
from molsysmt import puw

def digest_coordinates(coordinates, caller=None):

    if caller == 'molsysmt.basic.get.get':
        if isinstance(coordinates, bool):
            return coordinates

    value = puw.get_value(coordinates)
    unit = puw.get_unit(coordinates)

    if not puw.check(unit, dimensionality={'[L]':1}):
        raise ArgumentError('coordinates', value=coordinates, caller=caller, message=None)

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

    raise ArgumentError('coordinates', value=coordinates, caller=caller, message=None)

