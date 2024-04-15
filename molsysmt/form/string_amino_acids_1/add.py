from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='string:amino_acids_1', to_form='string:amino_acids_1')
def add(to_item, item, group_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

