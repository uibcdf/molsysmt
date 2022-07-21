from molsysm._private.exception import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:mol2', to_form='file:mol2')
def add(to_item, item, check=True):

    raise NotImplementedMethodError()

