from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='string:aminoacids1', to_form='string:aminoacids1')
def add(to_item, item, group_indices='all'):

    raise NotImplementedMethodError()

