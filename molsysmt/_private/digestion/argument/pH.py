import numpy as np
from ...exceptions import ArgumentError

def digest_pH(pH, caller=None):

    if isinstance(pH, (int, float)):
        return pH

    raise ArgumentError('pH', value=pH, caller=caller, message=None)

