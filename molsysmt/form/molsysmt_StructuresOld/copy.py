from molsysmt._private.digestion import digest

@digest(form='molsysmt.StructuresOld')
def copy(item):

    return item.copy()

