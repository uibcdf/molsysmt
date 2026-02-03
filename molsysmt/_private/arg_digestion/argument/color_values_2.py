from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_color_values_2(color_values_2, caller=None):

    if color_values_2 is None:
        return color_values_2

    if isinstance(color_values_2, (list, tuple, range, np.ndarray)):
        return color_values_2

    if puw.is_quantity(color_values_2):
        return puw.get_value(color_values_2)

    raise ArgumentError('color_values_2', value=color_values_2, caller=caller, message=None)

