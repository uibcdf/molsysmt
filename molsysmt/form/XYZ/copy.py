from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='XYZ')
def copy(item):

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item

