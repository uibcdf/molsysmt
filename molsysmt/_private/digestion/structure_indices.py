import numpy as np

def digest_structure_indices(structure_indices):

    if type(structure_indices)==str:
        if structure_indices in ['all', 'All', 'ALL']:
            structure_indices = 'all'
        else:
            raise ValueError()
    elif type(structure_indices) in [int, np.int64, np.int32]:
        structure_indices = np.array([structure_indices], dtype='int64')
    elif hasattr(structure_indices, '__iter__'):
        structure_indices = np.array(structure_indices, dtype='int64')
    else:
        raise ValueError()
    return structure_indices

def digest_multiple_structure_indices(structure_indices):

    from ..lists_and_tuples import is_list_or_tuple

    output = None

    if is_list_or_tuple(structure_indices):

        output = [digest_structure_indices(ii) for ii in structure_indices]

    else:

        output = digest_structure_indices(structure_indices)

    return output

