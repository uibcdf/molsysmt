from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import puw

def digest_value(value, caller=None):

    if value is not None:
        if puw.is_quantity(value):
            value = puw.standardize(value)

    return value

