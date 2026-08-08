from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.variables import is_all
import numpy as np

def digest_bond_id(bond_id, caller=None):

    # Imported here, not at module level: ArgDigest loads every digester in this
    # package when it initializes, so a top-level import made any digested call pay
    # for a heavy library that most calls never need.
    import pandas as pd

    if caller=='molsysmt.basic.get.get':
        if isinstance(bond_id, bool):
            return bond_id
    elif caller=='molsysmt.basic.compare.compare':
        if isinstance(bond_id, bool):
            return bond_id
    elif caller=='molsysmt.basic.select.select':
        if isinstance(bond_id, (int, np.integer, str, list, tuple, np.ndarray)):
            return bond_id
        elif is_all(bond_id):
            return bond_id
    elif caller == 'molsysmt.basic.set.set':
        if bond_id is None or bond_id is pd.NA:
            return bond_id
        if np.isscalar(bond_id):
            return str(bond_id)
        values = np.asarray(bond_id, dtype=object)
        if values.ndim == 1:
            return [pd.NA if value is pd.NA or value is None else str(value) for value in values]

    raise ArgumentError('bond_id', value=bond_id, caller=caller, message=None)
