from molsysm._private.exception import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='openmm.Topology', to_form='openmm.Topology')
def add(to_item, item):

    raise NotImplementedMethodError()

