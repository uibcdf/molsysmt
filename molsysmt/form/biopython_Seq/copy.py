from molsysmt._private.digestion import digest

@digest(form='biopython.Seq')
def copy(item):

    return item.copy()

