from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='openmm.System')
def copy(item, skip_digestion=False):

    tmp_item = item.__copy__()

    return tmp_item

