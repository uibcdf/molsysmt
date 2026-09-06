import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from ._quantity_parsing import parse_quantity_string

def digest_cutoff_distance(cutoff_distance, caller=None):

    if isinstance(cutoff_distance, str):
        cutoff_distance = parse_quantity_string('cutoff_distance', cutoff_distance, caller=caller)

    if caller is not None and caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        if cutoff_distance is None:
            return cutoff_distance

    if puw.is_quantity(cutoff_distance):
        if puw.check(cutoff_distance, dimensionality={'[L]':1}):
            return puw.standardize(cutoff_distance)

    raise ArgumentError('cutoff_distance', value=cutoff_distance, caller=caller, message=None)

