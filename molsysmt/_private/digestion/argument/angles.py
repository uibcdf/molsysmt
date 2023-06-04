import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

def digest_angles(angles, caller=None):

    if puw.is_quantity(angles):
        if puw.are_compatible(angles, '0.0 radians'):

            value, unit = puw.get_value_and_unit(angles)

            if isinstance(value, (int, float)):
                value = np.array([value])

            if isinstance(value, (list, tuple)):
                value = np.array(value)

            if not isinstance(value, np.ndarray):
                value = np.array(value)

            shape = value.shape

            if len(shape) == 1:
                return puw.quantity(value[np.newaxis, :], unit, standardized=True)
            elif len(shape) == 2:
                return puw.quantity(value, unit, standardized=True)

    raise ArgumentError('angles', value=angles, caller=caller, message=None)

