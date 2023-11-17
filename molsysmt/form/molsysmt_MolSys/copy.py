from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSysNEW')
def copy(item):

    return item.copy()

