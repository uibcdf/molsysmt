from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='biopython.SeqRecord')
def merge(items, group_indices='all'):

    raise NotImplementedMethodError()

