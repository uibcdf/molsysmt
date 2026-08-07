from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Molecule')
def copy(item, skip_digestion=False):

    from copy import deepcopy
    return deepcopy(item)
