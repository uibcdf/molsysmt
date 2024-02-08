from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='string:aminoacids3')
def merge(items, group_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

