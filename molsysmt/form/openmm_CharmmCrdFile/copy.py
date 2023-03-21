from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='openmm.CharmmCrdFile')
def copy(item):

    raise NotImplementedMethodError()

