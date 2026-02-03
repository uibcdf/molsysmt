from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import arg_digest

@arg_digest(form='molsysmt.MolecularMechanics')
def copy(item, skip_digestion=False):

    return item.copy()

