from molsysmt._private.digestion import digest

@digest(form='molsysmt.Structures')
def copy(item):

    return item.copy()

