from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.variables import is_all
import numpy as np

def digest_bond_type(bond_type, caller=None):

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

    raise ArgumentError('bond_type', value=bond_type, caller=caller, message=None)
