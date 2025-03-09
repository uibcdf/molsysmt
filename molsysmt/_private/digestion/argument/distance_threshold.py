import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

common_functions_with_distance_threshold = [
    'molsysmt.hbonds.get_buch_hbonds.get_buch_hbonds',
    'molsysmt.hbonds.get_luzard_chandler_hbonds.get_luzard_chandler_hbonds',
]

common_functions_with_distance_threshold_and_None = [
]

def digest_distance_threshold(distance_threshold, caller=None):

    if caller in common_functions_with_distance_threshold:

        if puw.is_quantity(distance_threshold):
            if puw.check(distance_threshold, dimensionality={'[L]':1}):
                return puw.standardize(distance_threshold)

    elif caller in common_functions_with_distance_threshold_and_None:

        if distance_threshold is None:
            return None

        if puw.is_quantity(distance_threshold):
            if puw.check(distance_threshold, dimensionality={'[L]':1}):
                return puw.standardize(distance_threshold)

    raise ArgumentError('distance_threshold', value=distance_threshold, caller=caller, message=None)

