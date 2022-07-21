from molsysm._private.exception import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys', to_form='molsysmt.MolSys')
def add(to_item, item):

    to_item.add(item)

    pass

