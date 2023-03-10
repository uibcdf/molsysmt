from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='openmm.Simulation')
def copy(item):

    raise NotImplementedMethodError()

