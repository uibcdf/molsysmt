from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:msmpk', to_form='file:msmpk')
def add(to_item, item, digest=True):

    raise NotImplementedMethodError()

