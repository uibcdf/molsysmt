import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

def digest_box_center(box_center, caller=None):

    if box_center is None:
        return box_center

    try:
        value, unit = puw.get_value_and_unit(box_center)
    except:
        raise ArgumentError('box_center', value=box_center, caller=caller, message=None)

    if not puw.check(unit, dimensionality={'[L]':1}):
        raise ArgumentError('box_center', value=box_center, caller=caller, message=None)

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

    raise ArgumentError('box_center', value=box_center, caller=caller, message=None)

