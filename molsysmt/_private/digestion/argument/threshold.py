import numpy as np
from molsysmt import puw
from ...exceptions import ArgumentError

_distance_threshold_methods = [
        'molsysmt.structure.get_contacts.get_contacts'
        ]

def digest_threshold(threshold, caller=None):

    if puw.is_quantity(threshold):

        if caller in _distance_threshold_methods:
            if puw.check(threshold, dimensionality={'[L]':1}):
                return puw.standardize(threshold)

    raise ArgumentError('threshold', value=threshold, caller=caller, message=None)

