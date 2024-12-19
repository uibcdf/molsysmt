import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

def digest_direction(direction, caller=None):

    if caller.endswith('move_away'):
        if direction is None:
            return direction

    if isinstance(direction, (list, tuple)):
        direction = np.array(direction, dtype=np.float64)

    if isinstance(direction, np.ndarray):
        if (len(direction.shape)==1) and (direction.shape[0]==3):
            direction = np.array(direction).reshape(1, 3)
            direction = direction.astype(np.float64)
            direction[0] = direction[0]/np.linalg.norm(direction[0])
            return direction
        if (len(direction.shape)==2) and (direction.shape[1]==3): # structure_index, xyz
            direction = direction.astype(np.float64)
            for ii in range(len(direction.shape[0])):
                direction[ii] = direction[ii]/np.linalg.norm(direction[ii])
            return direction

    raise ArgumentError('direction', value=direction, caller=caller, message=None)

