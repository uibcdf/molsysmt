from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:dcd', to_form='file:dcd')
def add(to_item, item, digest=True):

    raise NotImplementedMethodError()

