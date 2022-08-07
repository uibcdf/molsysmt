from ...exceptions import ArgumentError
from ...variables import is_all
from numpy import ndarray

def digest_group_names(group_names, caller=None):

    output = True

    if not isinstance(group_names, (list, tuple, ndarray)):
        aux_group_names = [group_names]
    else:
        aux_group_names = group_names

    for group_name in aux_group_names:
        if not isinstance(group_name, str):
            output = False
            break

    if output:
        return aux_group_names

    raise ArgumentError('group_names', value=group_names, caller=caller, message=None)
