from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openmm.AmberPrmtopFile')
def copy(item, skip_digestion=False):

    raise NotImplementedMethodError()
