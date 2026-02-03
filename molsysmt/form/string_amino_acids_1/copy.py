from molsysmt._private.digestion import arg_digest
from copy import copy

@arg_digest(form='string:amino_acids_1')
def extract(item, skip_digestion=False):

    return copy(item)

