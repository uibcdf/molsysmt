import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

def digest_clearance(clearance, caller=None):

    from .distance import digest_distance

    try:
        return digest_distance(clearance, caller=caller)
    except:
        raise ArgumentError('clearance', value=clearance, caller=caller, message=None)

