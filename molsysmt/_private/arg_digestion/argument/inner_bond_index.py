from molsysmt._private.smonitor import ArgumentError
import numpy as np

def digest_inner_bond_index(inner_bond_index, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(inner_bond_index, bool):
            return inner_bond_index
    elif caller=='molsysmt.basic.compare.compare':
        if isinstance(inner_bond_index, bool):
            return inner_bond_index

    raise ArgumentError('inner_bond_index', value=inner_bond_index, caller=caller, message=None)
