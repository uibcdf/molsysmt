from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_color_values(color_values, caller=None):

    if color_values is None:
        return color_values

    if isinstance(color_values, (list, tuple, range, np.ndarray)):
        return color_values

    if puw.is_quantity(color_values):
        return puw.get_value(color_values)

    raise ArgumentError('color_values', value=color_values, caller=caller, message=None)

