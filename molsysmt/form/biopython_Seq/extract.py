from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='biopython.Seq')
def extract(item, group_indices='all', copy_if_all=True):

    if is_all(group_indices):

        if copy_if_all:
            tmp_item = item.copy()
        else:
            tmp_item = item
    else:

        raise NotImplementedMethodError

    return tmp_item

