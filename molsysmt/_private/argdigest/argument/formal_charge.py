import numpy as np
from molsysmt._private.smonitor import ArgumentError
from molsysmt import pyunitwizard as puw

functions_where_boolean = (
    'molsysmt.basic.get.get',
    'molsysmt.basic.compare.compare',
    'molsysmt.basic.iterator.__init__',
    '.iterators.__init__'
    )

def digest_formal_charge(formal_charge, caller=None):

    # Imported here, not at module level: ArgDigest loads every digester in this
    # package when it initializes, so a top-level import made any digested call pay
    # for a heavy library that most calls never need.
    import pandas as pd

    if caller is not None:

        if caller.endswith(functions_where_boolean):
            if isinstance(formal_charge, bool):
                return formal_charge
            else:
                raise ArgumentError('formal_charge', value=formal_charge, caller=caller, message=None)

    if formal_charge is None:
        return None

    if isinstance(formal_charge, (int, np.integer)):
        return int(formal_charge)

    if isinstance(formal_charge, (list, tuple, np.ndarray)):
        value = np.asarray(formal_charge, dtype=object)
        if value.ndim == 1 and all(
            entry is None or entry is pd.NA
            or isinstance(entry, (int, np.integer)) and not isinstance(entry, bool)
            for entry in value
        ):
            if any(entry is None or entry is pd.NA for entry in value):
                return value.tolist()
            return value.astype(np.int16)
        raise ArgumentError('formal_charge', value=formal_charge, caller=caller, message=None)

    value = puw.get_value(formal_charge)
    unit = puw.get_unit(formal_charge)

    if not puw.check(unit, dimensionality={'[T]':1, '[A]':1}):
        raise ArgumentError('formal_charge', value=formal_charge, caller=caller, message=None)

    if not isinstance(value, np.ndarray):
        value = np.array(value)

    shape = value.shape

    if len(shape) == 1:
        return puw.standardize(puw.quantity(value, unit))

    raise ArgumentError('formal_charge', value=formal_charge, caller=caller, message=None)
