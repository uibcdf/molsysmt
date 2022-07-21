from molsysm._private.exception import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:xyznpy', to_form='file:xyznpy')
def add(to_item, item):

    raise NotImplementedMethodError()

