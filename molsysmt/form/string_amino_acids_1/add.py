from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='string:amino_acids_1', to_form='string:amino_acids_1')
def add(to_item, item, group_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

