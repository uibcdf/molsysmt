from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSysOld')
def copy(item):

    return item.copy()

