from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='MDAnalysis.Universe')
def copy(item):

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item

