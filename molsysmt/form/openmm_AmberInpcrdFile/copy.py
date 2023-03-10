from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='openmm.AmberInpcrdFile')
def extract(item):

    raise NotImplementedMethodError()

