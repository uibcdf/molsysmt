import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

def digest_distance(distance, caller=None):

    if puw.is_quantity(distance):
        if puw.check(distance, dimensionality={'[L]':1}):
            return puw.standardize(distance)

    raise ArgumentError('distance', value=distance, caller=caller, message=None)

