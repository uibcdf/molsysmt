import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError




def digest_vector(vector, caller=None):

    if isinstance(vector, (list, tuple)):
        vector = np.array(vector, dtype=np.float64)

    if isinstance(vector, np.ndarray):
        if (len(vector.shape)==1) and (vector.shape[0]==3):
            vector = vector.astype(np.float64)
            return vector

    raise ArgumentError('vector', value=vector, caller=caller, message=None)

