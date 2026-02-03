import numpy as np
from ...exceptions import ArgumentError

functions_where_boolean = (
    'molsysmt.basic.get.get',
    'molsysmt.basic.compare.compare',
    'molsysmt.basic.iterator.__init__',
    '.iterators.__init__'
    )

def digest_formal_charge(formal_charge, caller=None):

    if caller is not None:

        if caller.endswith(functions_where_boolean):
            if isinstance(formal_charge, bool):
                return formal_charge
            else:
                raise ArgumentError('formal_charge', value=formal_charge, caller=caller, message=None)

    if formal_charge is None:
        return None

    value = puw.get_value(formal_charge)
    unit = puw.get_unit(formal_charge)

    if not puw.check(unit, dimensionality={'[T]':1, '[A]':1}):
        raise ArgumentError('formal_charge', value=formal_charge, caller=caller, message=None)

    if not isinstance(value, np.ndarray):
        value = np.array(value)

    shape = value.shape

    if len(shape) == 1:
        return puw.quantity(value, unit, standardized=True)

    raise ArgumentError('formal_charge', value=formal_charge, caller=caller, message=None)
