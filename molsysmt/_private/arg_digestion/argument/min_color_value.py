from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_min_color_value(min_color_value, caller=None):

    if min_color_value is None:
        return None

    if puw.is_quantity(min_color_value):
        min_color_value = puw.get_value(min_color_value)

    if isinstance(min_color_value, (int, float)):
        return min_color_value

    raise ArgumentError('min_color_value', value=min_color_value, caller=caller, message=None)
