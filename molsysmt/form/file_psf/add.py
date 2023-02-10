from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:psf', to_form='file:psf')
def add(to_item, item):

    raise NotImplementedMethodError()

