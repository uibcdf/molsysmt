import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

def digest_radius(radius, caller=None):

    if puw.is_quantity(radius):
        if puw.check(radius, dimensionality={'[L]':1}):
            return puw.standardize(radius)

    raise ArgumentError('radius', value=radius, caller=caller, message=None)

