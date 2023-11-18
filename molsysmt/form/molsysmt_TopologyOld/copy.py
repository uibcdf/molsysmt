from molsysmt._private.digestion import digest

@digest(form='molsysmt.TopologyOld')
def copy(item):

    return item.copy()

