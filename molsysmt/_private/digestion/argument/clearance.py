import numpy as np
from molsysmt import puw
from ...exceptions import ArgumentError

def digest_clearance(clearance, caller=None):

    if puw.is_quantity(clearance):
        if puw.check(clearance, dimensionality={'[L]':1}):
            return puw.standardize(clearance)

    raise ArgumentError('clearance', value=clearance, caller=caller, message=None)

