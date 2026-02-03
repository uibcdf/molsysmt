from ...exceptions import ArgumentError
import numpy as np

def digest_quartets(quartets, caller=None):

    if quartets is None:
        return None

    if isinstance(quartets, (list, tuple, np.ndarray)):
        if not isinstance(quartets, np.ndarray):
            quartets = np.array(quartets)
        shape = quartets.shape
        if len(shape) == 1:
            if shape[0] == 4:
                return quartets[np.newaxis, :]
        if len(shape) == 2:
            if shape[1] == 4:
                return quartets

    raise ArgumentError('quartets', value=quartets, caller=caller, message=None)

