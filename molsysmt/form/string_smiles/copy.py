from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='string:smiles')
def copy(item, skip_digestion=False):

    from copy import copy as _copy
    return _copy(item)
