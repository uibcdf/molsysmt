import numpy as np
from ..exceptions import WrongIndicesError


def digest_indices(indices):
    """ Checks if indices are of the expected type and value. """
    # TODO: duplicate code in atom_indices.py
    if isinstance(indices, str):
        if indices.lower() == 'all':
            return 'all'
        else:
            raise WrongIndicesError()
    elif isinstance(indices, (int, np.int64, np.int32)):
        indices = np.array([indices], dtype='int64')
    elif hasattr(indices, '__iter__'):
        indices = np.array(indices, dtype='int64')

    return indices
