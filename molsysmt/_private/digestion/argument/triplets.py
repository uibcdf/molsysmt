from ...exceptions import ArgumentError
import numpy as np

def digest_triplets(triplets, caller=None):

    if triplets is None:
        return None

    if isinstance(triplets, (list, tuple, np.ndarray)):
        if not isinstance(triplets, np.ndarray):
            triplets = np.array(triplets)
        shape = triplets.shape
        if len(shape) == 1:
            if shape[0] == 3:
                return triplets[np.newaxis, :]
        if len(shape) == 2:
            if shape[1] == 3:
                return triplets

    raise ArgumentError('triplets', value=triplets, caller=caller, message=None)

