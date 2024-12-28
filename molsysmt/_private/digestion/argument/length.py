import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

def digest_length(length, caller=None):

    if puw.is_quantity(length):
        if puw.check(length, dimensionality={'[L]':1}):
            return puw.standardize(length)

    raise ArgumentError('length', value=length, caller=caller, message=None)

