from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from copy import copy

@digest(form='string:amino_acids_3')
def extract(item, group_indices='all', copy_if_all=True, skip_digestion=False):

    if is_all(group_indices):

        if copy_if_all:
            tmp_item = copy(item)
        else:
            tmp_item = item
    else:

        raise NotImplementedMethodError

    return tmp_item

