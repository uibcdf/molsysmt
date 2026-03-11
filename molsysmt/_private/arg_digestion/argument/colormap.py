from molsysmt._private.smonitor import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw
from matplotlib.pyplot import colormaps
from matplotlib.colors import Colormap

def digest_colormap(colormap, caller=None):

    if colormap is None:
        return None

    if isinstance(colormap, str):
        if colormap in colormaps:
            return colormaps[colormap]

    if isinstance(colormap, Colormap):
        return colormap

    raise ArgumentError('colormap', value=colormap, caller=caller, message=None)
