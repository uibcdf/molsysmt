from molsysmt._private.digestion import digest

@digest(form='parmed.Structure')
def copy(item, skip_digestion=False):

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item

