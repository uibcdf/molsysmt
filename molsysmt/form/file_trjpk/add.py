from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:trjpk', to_form='file:trjpk')
def add(to_item, item, digest=True):

    raise NotImplementedMethodError()

