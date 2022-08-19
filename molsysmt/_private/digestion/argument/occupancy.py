import numpy as np
from ...exceptions import ArgumentError

def digest_occupancy(occupancy, caller=None):

    if caller=='molsysmt.basic.get.get':

        if isinstance(occupancy, bool):
            return occupancy

    raise ArgumentError('occupancy', value=occupancy, caller=caller, message=None)
