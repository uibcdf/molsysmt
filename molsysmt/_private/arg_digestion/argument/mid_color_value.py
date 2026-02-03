from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_mid_color_value(mid_color_value, caller=None):

    if mid_color_value is None:
        return None

    if puw.is_quantity(mid_color_value):
        mid_color_value = puw.get_value(mid_color_value)

    if isinstance(mid_color_value, (int, float)):
        return mid_color_value

    raise ArgumentError('mid_color_value', value=mid_color_value, caller=caller, message=None)
