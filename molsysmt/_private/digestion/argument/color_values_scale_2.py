from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_color_values_scale_2(color_values_scale_2, caller=None):

    if color_values_scale_2 is None:
        return color_values_scale_2

    if isinstance(color_values_scale_2, str):
        if color_values_scale_2 in ['linear', 'log']:
            return color_values_scale_2

    raise ArgumentError('color_values_scale_2', value=color_values_scale_2, caller=caller, message=None)

