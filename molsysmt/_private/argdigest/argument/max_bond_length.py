import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from ._quantity_parsing import parse_quantity_string

def digest_max_bond_length(max_bond_length, caller=None):

    if isinstance(max_bond_length, str):
        max_bond_length = parse_quantity_string('max_bond_length', max_bond_length, caller=caller)

    if max_bond_length is None:
        return None

    if puw.is_quantity(max_bond_length):
        if puw.check(max_bond_length, dimensionality={'[L]':1}):
            return puw.standardize(max_bond_length)

    raise ArgumentError('max_bond_length', value=max_bond_length, caller=caller, message=None)
