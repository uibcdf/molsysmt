from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='openmm.AmberInpcrdFile', to_form='openmm.AmberInpcrdFile')
def add(to_item, item, digest=True):

    raise NotImplementedMethodError()

