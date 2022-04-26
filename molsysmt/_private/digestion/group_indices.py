import numpy as np

def digest_group_indices(group_indices):

    if type(group_indices)==str:
        if group_indices in ['all', 'All', 'ALL']:
            group_indices = 'all'
        else:
            raise ValueError()
    elif type(group_indices) in [int, np.int64, np.int32]:
        group_indices = np.array([group_indices], dtype='int64')
    elif hasattr(group_indices, '__iter__'):
        group_indices = np.array(group_indices, dtype='int64')

    return group_indices

