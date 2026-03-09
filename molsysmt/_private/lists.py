import numpy as np
from molsysmt import pyunitwizard as puw

def is_list_of_lists(list_of_lists):
    return all(isinstance(i, list) for i in list_of_lists)

def sorted_list_of_pairs(list_of_pairs, extra_list=None):

    if len(list_of_pairs) == 0:
        if extra_list is None:
            return []
        else:
            return [], []

    list_of_pairs = np.asarray(list_of_pairs)
    
    if list_of_pairs.ndim == 1:
        # If it's a single pair [a, b] instead of [[a, b]]
        list_of_pairs = list_of_pairs.reshape(1, -1)

    output = np.sort(list_of_pairs, axis=1)
    sort_indices = np.lexsort((output[:, 1], output[:, 0]))
    output = output[sort_indices].tolist()

    if extra_list is None:
        return output
    else:
        if is_list_of_lists(extra_list):
            raise NotImplementedError
        else:
            sorted_extra = puw.utils.sequences.slice(extra_list, sort_indices, value_type='list')
            return output, sorted_extra
