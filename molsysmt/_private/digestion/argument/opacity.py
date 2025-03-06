from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw

def digest_opacity(opacity, caller=None):

    if opacity is None:
        return None

    if isinstance(opacity, (int, float)):
        return opacity

    raise ArgumentError('opacity', value=opacity, caller=caller, message=None)

