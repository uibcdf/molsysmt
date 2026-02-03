from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_max_value(max_value, caller=None):

    if max_value is None:
        return None

    if puw.is_quantity(max_value):
        max_value = puw.get_value(max_value)

    if isinstance(max_value, (int, float)):
        return max_value

    raise ArgumentError('max_value', value=max_value, caller=caller, message=None)

