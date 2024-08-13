from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_max_color_value_2(max_color_value_2, caller=None):

    if max_color_value_2 is None:
        return None

    if puw.is_quantity(max_color_value_2):
        max_color_value_2 = puw.get_value_2(max_color_value_2)

    if isinstance(max_color_value_2, (int, float)):
        return max_color_value_2

    raise ArgumentError('max_color_value_2', value_2=max_color_value_2, caller=caller, message=None)
