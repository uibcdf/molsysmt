from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:crd', to_form='file:crd')
def add(to_item, item):

    raise NotImplementedMethodError()

