from molsysmt._private.digestion import digest

@digest(form='molsysmt.TopologyOld')
def copy(item, skip_digestion=False):

    return item.copy()

