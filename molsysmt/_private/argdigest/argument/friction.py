from molsysmt._private.smonitor import ArgumentError
from molsysmt import pyunitwizard as puw
import numpy as np

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        )

def digest_friction(friction, caller=None):

    if caller is not None and caller.endswith(functions_with_boolean):
        if isinstance(friction, bool):
            return friction

    try:
        value, unit = puw.get_value_and_unit(friction)
    except Exception:
        raise ArgumentError('friction', value=friction, caller=caller, message=None)

    if not puw.check(unit, dimensionality={'[T]':-1}):
        raise ArgumentError('friction', value=friction, caller=caller, message=None)

    if isinstance(value, (int, np.int64, float, np.float64)):
        return puw.standardize(puw.quantity(value, unit))

    raise ArgumentError('friction', value=friction, caller=caller, message=None)

