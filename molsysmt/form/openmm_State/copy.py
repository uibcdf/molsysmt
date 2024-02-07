from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='openmm.State')
def copy(item, skip_digestion=False):

    raise NotImplementedMethodError()

