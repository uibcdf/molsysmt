from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolecularMechanics', to_form='molsysmt.MolecularMechanics')
def add(to_item, item, atom_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

