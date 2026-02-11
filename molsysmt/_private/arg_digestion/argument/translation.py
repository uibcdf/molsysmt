import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from .coordinates import digest_coordinates

def digest_translation(translation, caller=None):

    try:
        return digest_coordinates(translation, caller=caller)
    except Exception:
        raise ArgumentError('translation', value=translation, caller=caller, message=None)
