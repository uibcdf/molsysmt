from molsysmt._private.smonitor import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_colormap_2(colormap_2, caller=None):

    # Imported here, not at module level: ArgDigest loads every digester in this
    # package when it initializes, so a top-level import made any digested call pay
    # for a heavy library that most calls never need.
    from matplotlib.pyplot import colormaps
    from matplotlib.colors import LinearSegmentedColormap

    if colormap_2 is None:
        return None

    if isinstance(colormap_2, str):
        if colormap_2 in colormaps:
            return colormaps[colormap_2]

    if isinstance(colormap_2, LinearSegmentedColormap):
        return colormap_2

    raise ArgumentError('colormap_2', value=colormap_2, caller=caller, message=None)
