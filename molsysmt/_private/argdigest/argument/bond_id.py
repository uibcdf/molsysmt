from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.variables import is_all
import numpy as np
import pandas as pd

def digest_bond_id(bond_id, caller=None):

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
