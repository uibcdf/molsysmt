from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.TopologyNEW', to_form='molsysmt.TopologyNEW')
def add(to_item, item):

    raise NotImplementedError
