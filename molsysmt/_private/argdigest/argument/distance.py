import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from ._quantity_parsing import parse_quantity_string

def digest_distance(distance, caller=None):

    if isinstance(distance, str):
        distance = parse_quantity_string('distance', distance, caller=caller)

    if puw.is_quantity(distance):
        if puw.check(distance, dimensionality={'[L]':1}):
            return puw.standardize(distance)

    raise ArgumentError('distance', value=distance, caller=caller, message=None)

