from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='string:aminoacids3', to_form='string:aminoacids3')
def add(to_item, item, digest=True):

    raise NotImplementedMethodError()

