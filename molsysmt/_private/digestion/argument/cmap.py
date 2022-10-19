from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw
from matplotlib.pyplot import colormaps
from matplotlib.colors import LinearSegmentedColormap

def digest_cmap(cmap, caller=None):

    if cmap is None:
        return None

    if isinstance(cmap, str):
        if cmap in colormaps:
            return colormaps[cmap]

    if isinstance(cmap, LinearSegmentedColormap):
        return cmap

    raise ArgumentError('cmap', value=cmap, caller=caller, message=None)
