from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_min_color_value_2(min_color_value_2, caller=None):

    if min_color_value_2 is None:
        return None

    if puw.is_quantity(min_color_value_2):
        min_color_value_2 = puw.get_value(min_color_value_2)

    if isinstance(min_color_value_2, (int, float)):
        return min_color_value_2

    raise ArgumentError('min_color_value_2', value=min_color_value_2, caller=caller, message=None)
