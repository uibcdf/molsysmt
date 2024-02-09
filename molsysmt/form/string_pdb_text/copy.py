from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='string:pdb_text')
def copy(item, skip_digestion=False):

    from copy import copy
    tmp_item = copy(item)

    return tmp_item

