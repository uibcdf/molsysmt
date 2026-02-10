import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError

common_functions_with_angle_threshold = [
    'molsysmt.hbonds.get_luzard_chandler_hbonds.get_luzard_chandler_hbonds',
]

common_functions_with_angle_threshold_and_None = [
]

def digest_angle_threshold(angle_threshold, caller=None):

    if isinstance(angle_threshold, str):
        angle_threshold = puw.parse(angle_threshold)

    if caller in common_functions_with_angle_threshold:

        if puw.is_quantity(angle_threshold):
            if puw.are_compatible(angle_threshold, '0.0 radians'):
                return puw.standardize(angle_threshold)

    elif caller in common_functions_with_angle_threshold_and_None:

        if angle_threshold is None:
            return None

        if puw.is_quantity(angle_threshold):
            if puw.are_compatible(angle_threshold, '0.0 radians'):
                return puw.standardize(angle_threshold)

    raise ArgumentError('angle_threshold', value=angle_threshold, caller=caller, message=None)

