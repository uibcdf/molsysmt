from molsysm._private.exception import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:gro', to_form='file:gro')
def add(to_item, item):

    raise NotImplementedMethodError()

