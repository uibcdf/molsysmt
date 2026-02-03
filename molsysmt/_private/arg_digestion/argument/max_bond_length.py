import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

def digest_max_bond_length(max_bond_length, caller=None):

    if max_bond_length is None:
        return None

    if puw.is_quantity(max_bond_length):
        if puw.check(max_bond_length, dimensionality={'[L]':1}):
            return puw.standardize(max_bond_length)

    raise ArgumentError('max_bond_length', value=max_bond_length, caller=caller, message=None)

