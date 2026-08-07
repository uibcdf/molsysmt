from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def extract(item, copy_if_all=True, skip_digestion=False):

    if copy_if_all:
        return item.copy()
    else:
        return item

