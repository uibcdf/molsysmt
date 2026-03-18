from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='string:smiles')
def to_string_smiles(item, skip_digestion=False):

    from copy import copy
    return copy(item)
