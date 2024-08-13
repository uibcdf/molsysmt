from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_color_2(color_2, caller=None):

    if isinstance(color_2, str):
        if len(color_2)==7 and color_2.startswith('#'):
            return color_2

    if isinstance(color_2, (list, tuple, np.ndarray)):
        if len(color_2)==3:
            return color_2

    raise ArgumentError('color_2', value=color_2, caller=caller, message=None)
