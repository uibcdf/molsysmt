from molsysm._private.exception import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:msmpk', to_form='file:msmpk')
def add(to_item, item, check=True):

    raise NotImplementedMethodError()

