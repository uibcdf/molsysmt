from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='openmm.Simulation', to_form='openmm.Simulation')
def add(to_item, item, digest=True):

    raise NotImplementedMethodError()

