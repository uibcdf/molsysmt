from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolecularMechanics')
def copy(item, skip_digestion=False):

    return item.copy()

