from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import arg_digest

@arg_digest(form='openmm.AmberInpcrdFile')
def copy(item, skip_digestion=False):

    raise NotImplementedMethodError()

