from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_cmap(cmap, caller=None):

    if cmap is None:
        return None

    raise ArgumentError('cmap', value=cmap, caller=caller, message=None)
