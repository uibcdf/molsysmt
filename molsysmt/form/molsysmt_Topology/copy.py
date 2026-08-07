from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.Topology')
def copy(item, skip_digestion=False):

    return item.copy()

