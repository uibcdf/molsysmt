from molsysmt._private.exceptions import ArgumentError
import numpy as np

def digest_bond_type(bond_type, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(bond_type, bool):
            return bond_type

    if isinstance(bond_type, str):
        return bond_type

    elif isinstance(bond_type, list):
        return bond_type

    elif isinstance(bond_type, tuple):
        return list(bond_type)

    elif isinstance(bond_type, np.ndarray):
        return bond_type.tolist()

    raise ArgumentError('bond_type', value=bond_type, caller=caller, message=None)

