import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from ._quantity_parsing import parse_quantity_string

def digest_length(length, caller=None):

    if isinstance(length, str):
        length = parse_quantity_string('length', length, caller=caller)

    if puw.is_quantity(length):
        if puw.check(length, dimensionality={'[L]':1}):
            return puw.standardize(length)

    raise ArgumentError('length', value=length, caller=caller, message=None)

