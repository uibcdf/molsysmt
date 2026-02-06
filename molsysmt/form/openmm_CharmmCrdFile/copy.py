from molsysmt.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openmm.CharmmCrdFile')
def copy(item, skip_digestion=False):

    raise NotImplementedMethodError()

