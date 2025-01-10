import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

def digest_bond_length(bond_length, caller=None):

    if puw.is_quantity(bond_length):
        if puw.check(bond_length, dimensionality={'[L]':1}):
            return puw.standardize(bond_length)

    raise ArgumentError('bond_length', value=bond_length, caller=caller, message=None)

