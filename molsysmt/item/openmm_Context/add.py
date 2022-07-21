from molsysm._private.exception import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='openmm.Context', to_form='openmm.Context')
def add(to_item, item):

    raise NotImplementedMethodError()

