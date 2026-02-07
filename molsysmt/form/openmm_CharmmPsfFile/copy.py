from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openmm.CharmmPsfFile')
def copy(item, skip_digestion=False):

    raise NotImplementedMethodError()

