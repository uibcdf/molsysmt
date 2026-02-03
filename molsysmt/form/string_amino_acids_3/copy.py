from molsysmt._private.arg_digestion import arg_digest
from copy import copy

@arg_digest(form='string:amino_acids_3')
def copy(item, skip_digestion=False):

    return copy(item)

