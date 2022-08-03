import numpy as np
from molsysmt import puw
from ...exceptions import ArgumentError

def digest_translation(translation, caller=None):

    if not puw.is_quantity(translation):
        raise ArgumentError('translation', caller=caller, message=None)

    value = puw.get_value(translation)
    unit = puw.get_unit(translation)

    if not puw.check(unit, dimensionality={'[L]':1}):
        raise ArgumentError('translation', caller=caller, message=None)

    if not isinstance(value, np.ndarray):
        value = np.array(value)

    shape = value.shape

    if len(shape) == 1:
        if shape[0] != 3:
            raise ArgumentError('translation', caller=caller, message=None)
    elif len(shape) == 2:
        if shape[1] != 3:
            raise ArgumentError('translation', caller=caller, message=None)
    else:
        raise ArgumentError('translation', caller=caller, message=None)

    translation = puw.quantity(value, unit)
    translation = puw.standardize(translation)

    return translation

