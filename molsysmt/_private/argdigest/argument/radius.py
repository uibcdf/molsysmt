import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from ._quantity_parsing import parse_quantity_string

def digest_radius(radius, caller=None):

    if isinstance(radius, str):
        radius = parse_quantity_string('radius', radius, caller=caller)

    if puw.is_quantity(radius):
        if puw.check(radius, dimensionality={'[L]':1}):
            return puw.standardize(radius)

    raise ArgumentError('radius', value=radius, caller=caller, message=None)

