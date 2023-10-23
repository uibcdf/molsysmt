from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology2', to_form='molsysmt.Topology2')
def add(to_item, item):

    raise NotImplementedError
