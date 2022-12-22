from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:xtc', to_form='file:xtc')
def add(to_item, item, digest=True):

    raise NotImplementedMethodError()

