import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

def digest_rotation(rotation, caller=None):

    if caller is not None:
        if caller.startswith('molsysmt.structure.rotate'):
            if isinstance(rotation, np.ndarray):
                if rotation.shape == (3,3):
                    return rotation
            elif isinstance(rotation, (list, tuple)):
                rotation = np.array(rotation)
                if rotation.shape == (3,3):
                    return rotation

    if isinstance(rotation, np.ndarray):
        if rotation.shape == (3,3):
            return rotation
        elif isinstance(rotation, (list, tuple)):
            rotation = np.array(rotation)
            if rotation.shape == (3,3):
                return rotation

    raise ArgumentError('rotation', value=rotation, caller=caller, message=None)


