from molsysmt._private.digestion import digest
from copy import copy

@digest(form='string:aminoacids3')
def copy(item):

    return copy(item)

