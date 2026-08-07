from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='biopython.Seq', to_form='biopython.Seq')
def add(to_item, item, group_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

