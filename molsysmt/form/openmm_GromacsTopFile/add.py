from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='openmm.GromacsTopFile', to_form='openmm.GromacsTopFile')
def add(to_item, item):

    raise NotImplementedMethodError()


