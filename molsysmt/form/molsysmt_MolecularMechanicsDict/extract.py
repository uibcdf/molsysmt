from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='molsysmt.MolecularMechanicsDict')
def extract(item, copy_if_all=True):

    if copy_if_all:
        return item.copy()
    else:
        return item

