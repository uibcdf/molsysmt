from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_color_values_scale(color_values_scale, caller=None):

    if color_values_scale is None:
        return color_values_scale

    if isinstance(color_values_scale, str):
        if color_values_scale in ['linear', 'log']:
            return color_values_scale

    raise ArgumentError('color_values_scale', value=color_values_scale, caller=caller, message=None)

