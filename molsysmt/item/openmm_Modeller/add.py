from molsysm._private.exception import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='openmm.Modeller', to_form='openmm.Modeller')
def add(to_item, item):

    raise NotImplementedMethodError()

