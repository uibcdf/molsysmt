import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

def digest_threshold(threshold, caller=None):

    if caller in 'molsysmt.structure.get_contacts.get_contacts':

        if puw.is_quantity(threshold):
            if puw.check(threshold, dimensionality={'[L]':1}):
                return puw.standardize(threshold)

    if caller in 'molsysmt.structure.get_neighbors.get_neighbors':

        if threshold is None:
            return None

        if puw.is_quantity(threshold):
            if puw.check(threshold, dimensionality={'[L]':1}):
                return puw.standardize(threshold)

    if caller in 'molsysmt.build.get_missing_bonds.get_missing_bonds':

        if puw.is_quantity(threshold):
            if puw.check(threshold, dimensionality={'[L]':1}):
                return puw.standardize(threshold)

    raise ArgumentError('threshold', value=threshold, caller=caller, message=None)

