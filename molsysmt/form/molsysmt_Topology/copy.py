from molsysmt._private.digestion import digest

@digest(form='molsysmt.TopologyNEW')
def copy(item):

    return item.copy()

