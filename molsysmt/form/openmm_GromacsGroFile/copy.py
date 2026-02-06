from molsysmt.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openmm.GromacsGroFile')
def copy(item, skip_digestion=True):

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item

