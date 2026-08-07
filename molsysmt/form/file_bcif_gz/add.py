from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:bcif.gz', to_form='file:bcif.gz')
def add(to_item, item, atom_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

