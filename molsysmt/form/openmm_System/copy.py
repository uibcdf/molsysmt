from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openmm.System')
def copy(item, skip_digestion=False):

    tmp_item = item.__copy__()

    return tmp_item

