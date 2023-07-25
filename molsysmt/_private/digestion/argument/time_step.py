from molsysmt._private.exceptions import ArgumentError
from molsysmt import pyunitwizard as puw
import numpy as np

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        )

def digest_time_step(time_step, caller=None):

    if caller.endswith(functions_with_boolean):
        if isinstance(time_step, bool):
            return time_step

    if time_step is None:
        return time_step

    value, unit = puw.get_value_and_unit(time_step)

    if not puw.check(unit, dimensionality={'[T]':1}):
        raise ArgumentError('time_step', value=coordinates, caller=caller, message=None)

    if isinstance(value, (int, np.int64, float, np.float64)):
        return puw.quantity(value, unit, standardized=True)

    raise ArgumentError('time_step', value=time_step, caller=caller, message=None)

