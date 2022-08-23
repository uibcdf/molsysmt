from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_value(value, caller=None):

    if value is not None:
        if puw.is_quantity(value):
            return puw.standardize(value)

    raise ArgumentError('value', value=value, caller=caller, message=None)
