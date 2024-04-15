from molsysmt._private.digestion import digest
from copy import copy

@digest(form='string:amino_acids_3')
def copy(item, skip_digestion=False):

    return copy(item)

