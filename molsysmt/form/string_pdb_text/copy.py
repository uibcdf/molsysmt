from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='string:pdb_text')
def copy(item, skip_digestion=False):

    from copy import copy
    tmp_item = copy(item)

    return tmp_item

