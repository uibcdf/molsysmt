from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='molsysmt.MolecularMechanics')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    raise NotWithThisMolecularSystemError()

