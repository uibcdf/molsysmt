import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from ._quantity_parsing import parse_quantity_string

def digest_force(force, caller=None):

    if isinstance(force, str):
        force = parse_quantity_string('force', force, caller=caller)

    if puw.is_quantity(force):
        if puw.check(force, dimensionality={'[L]':1, '[M]':1, '[T]':-2, '[mol]':-1}):
            return puw.standardize(force)

    raise ArgumentError('force', value=force, caller=caller, message=None)

