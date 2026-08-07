from molsysmt._private.smonitor import ArgumentError
from argdigest.core.caller import caller_matches
import numpy as np
import pandas as pd

def digest_bond_order(bond_order, caller=None):

    if caller_matches(caller, 'add_bond'):
        if bond_order is None:
            return None
        if isinstance(bond_order, (str, int, float, np.integer, np.floating)):
            return str(bond_order)

    if caller=='molsysmt.basic.get.get':
        if isinstance(bond_order, bool):
            return bond_order
    elif caller=='molsysmt.basic.compare.compare':
        if isinstance(bond_order, bool):
            return bond_order
    elif caller == 'molsysmt.basic.set.set':
        if bond_order is None or bond_order is pd.NA:
            return bond_order
        values = [bond_order] if np.isscalar(bond_order) else list(bond_order)
        if all(
            value is None or value is pd.NA
            or (
                isinstance(value, (int, np.integer))
                and not isinstance(value, (bool, np.bool_))
                and 0 <= int(value) <= 255
            )
            for value in values
        ):
            normalized = [
                value if value is None or value is pd.NA else int(value)
                for value in values
            ]
            return normalized[0] if np.isscalar(bond_order) else normalized

    raise ArgumentError('bond_order', value=bond_order, caller=caller, message=None)
