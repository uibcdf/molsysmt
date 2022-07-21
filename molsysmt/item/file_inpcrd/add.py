from molsysm._private.exception import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:inpcrd', to_form='file:inpcrd')
def add(to_item, item):

    raise NotImplementedMethodError()

