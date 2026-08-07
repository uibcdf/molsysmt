from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='openmm.State')
def copy(item, skip_digestion=False):

    raise NotImplementedMethodError()

