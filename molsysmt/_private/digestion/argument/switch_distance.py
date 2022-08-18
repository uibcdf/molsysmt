import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

def digest_switch_distance(switch_distance, caller=None):

    if puw.is_quantity(switch_distance):
        if puw.check(switch_distance, dimensionality={'[L]':1}):
            return puw.standardize(switch_distance)

    raise ArgumentError('switch_distance', value=switch_distance, caller=caller, message=None)

