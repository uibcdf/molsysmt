import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError
from scipy.spatial.transform import Rotation

def digest_rotation(rotation, caller=None):

    if isinstance(rotation, (list, tuple)):
        rotation = np.array(rotation)

    if isinstance(rotation, np.ndarray):
        if rotation.shape == (3,3):
            return rotation[np.newaxis,np.newaxis,:,:]
        elif len(rotation.shape)==3 and rotation.shape[1:]==(3,3):
            return rotation[np.newaxis,:,:,:]
        elif len(rotation.shape)==4 and rotation.shape[2:]==(3,3):
            return rotation

    if isinstance(rotation, Rotation):
        return rotation

    raise ArgumentError('rotation', value=rotation, caller=caller, message=None)


