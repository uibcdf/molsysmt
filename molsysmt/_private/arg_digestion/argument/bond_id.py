from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.variables import is_all
import numpy as np

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

    raise ArgumentError('bond_id', value=bond_id, caller=caller, message=None)
