from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_max_color_value(max_color_value, caller=None):

    if max_color_value is None:
        return None

    if puw.is_quantity(max_color_value):
        max_color_value = puw.get_value(max_color_value)

    if isinstance(max_color_value, (int, float)):
        return max_color_value

    raise ArgumentError('max_color_value', value=max_color_value, caller=caller, message=None)
