import numpy as np
from molsysmt import puw
from ...exceptions import ArgumentError

def digest_angles(angles, caller=None):

    if puw.is_quantity(angles):
        if puw.check(angles, dimensionality={}):
            return puw.standardize(angles)

    raise ArgumentError('angles', value=angles, caller=caller, message=None)

