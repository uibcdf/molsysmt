from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:mol2', to_form='file:mol2')
def add(to_item, item):

    raise NotImplementedMethodError()

