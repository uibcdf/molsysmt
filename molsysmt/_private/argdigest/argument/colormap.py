from molsysmt._private.smonitor import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_colormap(colormap, caller=None):

    # Imported here, not at module level: ArgDigest loads every digester in this
    # package when it initializes, so a top-level import made any digested call pay
    # for a heavy library that most calls never need.
    from matplotlib.pyplot import colormaps
    from matplotlib.colors import Colormap

    if colormap is None:
        return None

    if isinstance(colormap, str):
        if colormap in colormaps:
            return colormaps[colormap]

    if isinstance(colormap, Colormap):
        return colormap

    raise ArgumentError('colormap', value=colormap, caller=caller, message=None)
