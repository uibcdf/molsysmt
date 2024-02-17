from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSysOld')
def copy(item, skip_digestion=False):

    return item.copy()

