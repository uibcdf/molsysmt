from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_mid_value(mid_value, caller=None):

    if mid_value is None:
        return None

    if puw.is_quantity(mid_value):
        mid_value = puw.get_value(mid_value)

    if isinstance(mid_value, (int, float)):
        return mid_value

    raise ArgumentError('mid_value', value=mid_value, caller=caller, message=None)
