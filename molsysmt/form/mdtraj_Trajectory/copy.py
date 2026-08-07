from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.Trajectory')
def copy(item, skip_digestion=False):

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item

