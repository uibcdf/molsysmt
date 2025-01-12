import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

common_functions_with_threshold = [
    'molsysmt.structure.get_contacts.get_contacts',
    'molsysmt.build.remove_overlapping_molecules.remove_overlapping_molecules',
]

def digest_threshold(threshold, caller=None):

    if caller in common_functions_with_threshold:

        if puw.is_quantity(threshold):
            if puw.check(threshold, dimensionality={'[L]':1}):
                return puw.standardize(threshold)

    elif caller in 'molsysmt.structure.get_neighbors.get_neighbors':

        if threshold is None:
            return None

        if puw.is_quantity(threshold):
            if puw.check(threshold, dimensionality={'[L]':1}):
                return puw.standardize(threshold)

    raise ArgumentError('threshold', value=threshold, caller=caller, message=None)

