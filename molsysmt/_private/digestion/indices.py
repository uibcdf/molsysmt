import numpy as np
from ..exceptions import WrongIndicesError

def digest_indices(indices):

    if type(indices)==str:
        if indices in ['all', 'All', 'ALL']:
            indices = 'all'
        else:
            raise ValueError()
    elif type(indices) in [int, np.int64, np.int32]:
        indices = np.array([indices], dtype='int64')
    elif hasattr(indices, '__iter__'):
        indices = np.array(indices, dtype='int64')

    return indices


# def digest_indices(indices):
#     """ Checks if indices are of the expected type and value. """
#     # TODO: duplicate code in atom_indices.py
#
#     if isinstance(indices, str):
#         indices = indices.lower()
#         if indices == 'all':
#             return indices
#         else:
#             raise WrongIndicesError(f"{indices} is not a valid indices.")
#     elif isinstance(indices, (int, np.int64, np.int32)):
#         indices = np.array([indices], dtype='int64')
#     elif hasattr(indices, '__iter__'):
#         indices = np.array(indices, dtype='int64')
#
#     return indices
