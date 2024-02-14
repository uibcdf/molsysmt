from molsysmt._private.digestion import digest

@digest(form='biopython.Seq')
def copy(item, skip_digestion=False):

    return item.copy()

