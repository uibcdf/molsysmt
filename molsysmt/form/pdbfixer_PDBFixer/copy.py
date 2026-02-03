from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='pdbfixer.PDBFixer')
def copy(item, skip_digestion=False):

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item
