from ...exceptions import ArgumentError
from ...variables import is_all
from numpy import ndarray

def digest_disulfide_group_names(disulfide_group_names, caller=None):

    output = True

    if not isinstance(disulfide_group_names, (list, tuple, ndarray)):
        aux_disulfide_group_names = [disulfide_group_names]
    else:
        aux_disulfide_group_names = disulfide_group_names

    for group_name in aux_disulfide_group_names:
        if not isinstance(group_name, str):
            output = False
            break

    if output:
        return aux_disulfide_group_names

    raise ArgumentError('disulfide_group_names', value=disulfide_group_names, caller=caller, message=None)
