import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

def digest_force(force, caller=None):

    if puw.is_quantity(force):
        if puw.check(force, dimensionality={'[L]':1, '[M]':1, '[T]':-2, '[mol]':-1}):
            return puw.standardize(force)

    raise ArgumentError('force', value=force, caller=caller, message=None)

