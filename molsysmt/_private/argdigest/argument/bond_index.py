from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.variables import is_all
import numpy as np

def digest_bond_index(bond_index, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(bond_index, bool):
            return bond_index
    elif caller=='molsysmt.basic.compare.compare':
        if isinstance(bond_index, bool):
            return bond_index
    elif caller=='molsysmt.basic.select.select':
        if isinstance(bond_index, (int, np.integer, list, tuple, np.ndarray)):
            return bond_index
        elif is_all(bond_index):
            return bond_index

    raise ArgumentError('bond_index', value=bond_index, caller=caller, message=None)
