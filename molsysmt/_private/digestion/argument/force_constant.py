import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

def digest_force_constant(force_constant, caller=None):

    if puw.is_quantity(force_constant):
        if puw.check(force_constant, dimensionality={'[M]':1, '[T]':-2, '[mol]':-1}):
            return puw.standardize(force_constant)

    raise ArgumentError('force_constant', value=force_constant, caller=caller, message=None)

