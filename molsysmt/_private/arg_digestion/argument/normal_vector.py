import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError


def digest_normal_vector(normal_vector, caller=None):

    if isinstance(normal_vector, (list, tuple)):
        normal_vector = np.array(normal_vector, dtype=np.float64)
        normal_vector = normal_vector/np.linalg.norm(normal_vector)
        return normal_vector

    if isinstance(normal_vector, np.ndarray):
        if (len(normal_vector.shape)==1) and (normal_vector.shape[0]==3):
            normal_vector = normal_vector.astype(np.float64)
            normal_vector = normal_vector/np.linalg.norm(normal_vector)
            return normal_vector

    raise ArgumentError('normal_vector', value=normal_vector, caller=caller, message=None)

