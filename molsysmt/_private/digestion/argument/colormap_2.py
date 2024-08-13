from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw
from matplotlib.pyplot import colormaps
from matplotlib.colors import LinearSegmentedColormap

def digest_colormap_2(colormap_2, caller=None):

    if colormap_2 is None:
        return None

    if isinstance(colormap_2, str):
        if colormap_2 in colormaps:
            return colormaps[colormap_2]

    if isinstance(colormap_2, LinearSegmentedColormap):
        return colormap_2

    raise ArgumentError('colormap_2', value=colormap_2, caller=caller, message=None)
