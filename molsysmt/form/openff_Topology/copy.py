from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openff.Topology')
def copy(item, skip_digestion=False):

    from copy import deepcopy
    return deepcopy(item)
