import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

def digest_mic_origin(mic_origin, caller=None):

    if mic_origin is None:
        return mic_origin

    try:
        value, unit = puw.get_value_and_unit(mic_origin)
    except:
        raise ArgumentError('mic_origin', value=mic_origin, caller=caller, message=None)

    if not puw.check(unit, dimensionality={'[L]':1}):
        raise ArgumentError('mic_origin', value=mic_origin, caller=caller, message=None)

    if not isinstance(value, np.ndarray):
        value = np.array(value)

    value = value.astype(np.float64)
    shape = value.shape

    if len(shape) == 1:
        if shape[0] == 3:
            return puw.quantity(value, unit, standardized=True)
    elif len(shape) == 2:
        if shape[1] == 3 and shape[0] == 1:
            return puw.quantity(value[0], unit, standardized=True)
    elif len(shape) == 3:
        if shape[2] == 3 and shape[0] == 1 and shape[1] == 1:
            return puw.quantity(value[0,0], unit, standardized=True)

    raise ArgumentError('mic_origin', value=mic_origin, caller=caller, message=None)

