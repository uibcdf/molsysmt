import numpy as np

def is_list_of_lists(list_of_lists):
    return all(isinstance(i, list) for i in list_of_lists)

def sorted_list_of_pairs(list_of_pairs, extra_list=None):

    output = np.sort(list_of_pairs, axis=1)
    sort_indices = np.lexsort((output[:, 1], output[:, 0]))
    output = output[sort_indices].tolist()

    if extra_list is None:
        return output
    else:
        if is_list_of_lists(extra_list):
            sorted_extra = [np.array(extra_list[i])[sort_indices].tolist() for i in range(len(extra_list))]
            return sorted_pairs.tolist(), *sorted_extra
        else:
            sorted_extra = np.array(extra_list)[sort_indices].tolist()
            return sorted_pairs.tolist(), sorted_extra
