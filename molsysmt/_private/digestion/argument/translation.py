import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

def digest_translation(translation, caller=None):

    from .coordinates import arg_digest_coordinates

    try:
        return digest_coordinates(translation, caller=caller)
    except:
        raise ArgumentError('translation', value=translation, caller=caller, message=None)

