import numpy as np
from ...exceptions import ArgumentError
from molsysmt import pyunitwizard as puw

functions_where_boolean = (
    'molsysmt.basic.get.get',
    'molsysmt.basic.compare.compare',
    'molsysmt.basic.iterator.__init__',
    '.iterators.__init__'
    )

def digest_b_factor(b_factor, caller=None):

    if caller is not None:

        if caller.endswith(functions_where_boolean):
            if isinstance(b_factor, bool):
                return b_factor

    if b_factor is None:
        return None

    value = puw.get_value(b_factor)
    unit = puw.get_unit(b_factor)

    if not puw.check(unit, dimensionality={'[L]':2}):
        raise ArgumentError('b_factor', value=b_factor, caller=caller, message=None)

    if not isinstance(value, np.ndarray):
        value = np.array(value)

    if len(value.shape) == 1:
        return puw.quantity(value[np.newaxis, :], unit, standardized=True)
    elif len(value.shape) == 2:
        return puw.quantity(value, unit, standardized=True)

    raise ArgumentError('b_factor', value=b_factor, caller=caller, message=None)
