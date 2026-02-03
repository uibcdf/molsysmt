from molsysmt._private.exceptions import ArgumentError
from molsysmt import pyunitwizard as puw
import numpy as np

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        )

def digest_friction(friction, caller=None):

    if caller.endswith(functions_with_boolean):
        if isinstance(friction, bool):
            return friction

    value, unit = puw.get_value_and_unit(friction)

    if not puw.check(unit, dimensionality={'[T]':-1}):
        raise ArgumentError('friction', value=friction, caller=caller, message=None)

    if isinstance(value, (int, np.int64, float, np.float64)):
        return puw.quantity(value, unit, standardized=True)

    raise ArgumentError('friction', value=friction, caller=caller, message=None)

