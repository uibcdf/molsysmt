from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='biopython.SeqRecord', to_form='biopython.SeqRecord')
def add(to_item, item, group_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

