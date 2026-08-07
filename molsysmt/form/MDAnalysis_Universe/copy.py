from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='MDAnalysis.Universe')
def copy(item):

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item

