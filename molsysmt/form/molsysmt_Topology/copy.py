from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology')
def copy(item):

    return item.copy()

