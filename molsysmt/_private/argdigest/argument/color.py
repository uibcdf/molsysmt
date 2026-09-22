import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_color(color, caller=None):

    if isinstance(color, str):
        if len(color) == 7 and color.startswith("#"):
            return color

    if isinstance(color, (list, tuple, np.ndarray)):
        if len(color) == 3:
            return color

    if isinstance(color, str):
        return color

    raise ArgumentError("color", value=color, caller=caller, message=None)
