import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from ._quantity_parsing import parse_quantity_string

def digest_z0(z0, caller=None):

    if isinstance(z0, str):
        z0 = parse_quantity_string('z0', z0, caller=caller)

    if puw.is_quantity(z0):
        if puw.check(z0, dimensionality={'[L]':1}):
            return puw.standardize(z0)

    raise ArgumentError('z0', value=z0, caller=caller, message=None)

