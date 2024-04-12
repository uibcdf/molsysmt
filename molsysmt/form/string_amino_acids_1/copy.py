from molsysmt._private.digestion import digest
from copy import copy

@digest(form='string:aminoacids1')
def extract(item, skip_digestion=False):

    return copy(item)

