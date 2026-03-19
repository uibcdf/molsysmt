from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:top')
def append_structures(to_item, item, structure_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()
