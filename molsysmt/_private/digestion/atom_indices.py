import numpy as np

def digest_atom_indices(atom_indices):

    if type(atom_indices)==str:
        if atom_indices in ['all', 'All', 'ALL']:
            atom_indices = 'all'
        else:
            raise ValueError()
    elif type(atom_indices) in [int, np.int64, np.int32]:
        atom_indices = np.array([atom_indices], dtype='int64')
    elif hasattr(atom_indices, '__iter__'):
        atom_indices = np.array(atom_indices, dtype='int64')

    return atom_indices

