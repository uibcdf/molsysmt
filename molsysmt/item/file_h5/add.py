from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:h5', to_form='file:h5')
def add(to_item, item):

    raise NotImplementedMethodError()

