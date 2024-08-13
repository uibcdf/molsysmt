from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_mid_color_value_2(mid_color_value_2, caller=None):

    if mid_color_value_2 is None:
        return None

    if puw.is_quantity(mid_color_value_2):
        mid_color_value_2 = puw.get_value_2(mid_color_value_2)

    if isinstance(mid_color_value_2, (int, float)):
        return mid_color_value_2

    raise ArgumentError('mid_color_value_2', value_2=mid_color_value_2, caller=caller, message=None)
