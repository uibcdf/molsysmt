from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys', to_form='molsysmt.MolSys')
def add(to_item, item, digest=True):

    to_item.add(item, digest=False)

    pass

