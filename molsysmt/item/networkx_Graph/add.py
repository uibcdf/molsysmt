from molsysm._private.exception import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='networkx.Graph', to_form='networkx.Graph')
def add(to_item, item):

    raise NotImplementedMethodError()

