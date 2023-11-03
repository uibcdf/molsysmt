import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

def digest_z0(z0, caller=None):

    if puw.is_quantity(z0):
        if puw.check(z0, dimensionality={'[L]':1}):
            return puw.standardize(z0)

    raise ArgumentError('z0', value=z0, caller=caller, message=None)

