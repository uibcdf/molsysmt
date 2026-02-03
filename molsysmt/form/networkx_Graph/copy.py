from molsysmt._private.digestion import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='networkx.Graph')
def copy(item, skip_digestion=False):

    tmp_item = item.copy()

    return tmp_item

