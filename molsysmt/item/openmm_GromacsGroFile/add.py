from molsysm._private.exception import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='openmm.GromacsGroFile', to_form='openmm.GromacsGroFile')
def add(to_item, item):

    raise NotImplementedMethodError()


