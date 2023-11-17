from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def copy(item):

    return item.copy()

