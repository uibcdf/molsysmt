import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

def digest_max_bond_distance(max_bond_distance, caller=None):

    if max_bond_distance is None:
        return None

    if puw.is_quantity(max_bond_distance):
        if puw.check(max_bond_distance, dimensionality={'[L]':1}):
            return puw.standardize(max_bond_distance)

    raise ArgumentError('max_bond_distance', value=max_bond_distance, caller=caller, message=None)

