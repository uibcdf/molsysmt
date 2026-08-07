import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError

def digest_clearance(clearance, caller=None):

    from .distance import digest_distance

    try:
        return digest_distance(clearance, caller=caller)
    except Exception:
        raise ArgumentError('clearance', value=clearance, caller=caller, message=None)

