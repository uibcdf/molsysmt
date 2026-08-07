from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='biopython.SeqRecord', to_form='biopython.SeqRecord')
def add(to_item, item, group_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

