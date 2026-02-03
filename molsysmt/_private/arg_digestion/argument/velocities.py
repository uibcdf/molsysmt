from ...exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

functions_where_boolean = (
    'molsysmt.basic.get.get',
    'molsysmt.basic.compare.compare',
    'molsysmt.basic.iterator.__init__',
    '.iterators.__init__'
    )

def digest_velocities(velocities, caller=None):

    if caller.endswith(functions_where_boolean):
        if isinstance(velocities, bool):
            return velocities

    if velocities is None:
        return None

    value = puw.get_value(velocities)
    unit = puw.get_unit(velocities)

    if not puw.check(unit, dimensionality={'[L]':1, '[T]':-1}):
        raise ArgumentError('velocities', value=velocities, caller=caller, message=None)

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

    raise ArgumentError('velocities', value=velocities, caller=caller, message=None)

