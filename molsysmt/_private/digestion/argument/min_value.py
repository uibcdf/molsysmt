from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_min_value(min_value, caller=None):

    if min_value is None:
        return None

    if puw.is_quantity(min_value):
        min_value = puw.get_value(min_value)

    if isinstance(min_value, (int, float)):
        return min_value

    raise ArgumentError('min_value', value=min_value, caller=caller, message=None)
