from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import puw

def digest_max_value(max_value, caller=None):

    if max_value is None:
        return None

    if isinstance(max_value, [int, float]):
        return max_value

    if puw.is_quantity(max_value):
        return max_value

    raise ArgumentError('max_value', value=max_value, caller=caller, message=None)
