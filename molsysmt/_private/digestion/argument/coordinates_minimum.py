from ...exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_coordinates_minimum(coordinates_minimum, caller=None):

    if coordinates_minimum is None:
        return None

    value, unit = puw.get_value_and_unit(coordinates_minimum)

    if not puw.check(unit, dimensionality={'[L]':1}):
        raise ArgumentError('coordinates_minimum', value=coordinates_minimum, caller=caller, message=None)

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

    raise ArgumentError('coordinates_minimum', value=coordinates_minimum, caller=caller, message=None)

