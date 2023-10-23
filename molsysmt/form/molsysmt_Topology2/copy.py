from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology2')
def copy(item):

    return item.copy()

