import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

def digest_width(width, caller=None):

    if puw.is_quantity(width):
        if puw.check(width, dimensionality={'[L]':1}):
            return puw.standardize(width)

    raise ArgumentError('width', value=width, caller=caller, message=None)

