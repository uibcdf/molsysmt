from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolecularMechanicsDict')
def copy(item):

    return item.copy()

