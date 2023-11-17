from molsysmt._private.digestion import digest

@digest(form='molsysmt.StructuresNEW')
def copy(item):

    return item.copy()

