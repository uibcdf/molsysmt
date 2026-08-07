from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.variables import is_all
import numpy as np
from argdigest.core.caller import caller_matches
import pandas as pd

def digest_bond_type(bond_type, caller=None):

    if caller_matches(caller, 'add_bond'):
        if bond_type is None:
            return None
        if isinstance(bond_type, str):
            return bond_type

    if caller=='molsysmt.basic.get.get':
        if isinstance(bond_type, bool):
            return bond_type
    elif caller=='molsysmt.basic.compare.compare':
        if isinstance(bond_type, bool):
            return bond_type
    elif caller=='molsysmt.basic.select.select':
        if isinstance(bond_type, (str, list, tuple, np.ndarray)):
            return bond_type
        elif is_all(bond_type):
            return bond_type
    elif caller == 'molsysmt.basic.set.set':
        if bond_type is None or bond_type is pd.NA:
            return bond_type
        values = [bond_type] if isinstance(bond_type, str) else list(bond_type)
        if all(value is None or value is pd.NA or value in {'covalent', 'dative', 'unknown'} for value in values):
            return values[0] if isinstance(bond_type, str) else values

    raise ArgumentError('bond_type', value=bond_type, caller=caller, message=None)
