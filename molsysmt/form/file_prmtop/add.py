from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:prmtop', to_form='file:prmtop')
def add(to_item, item, atom_indices='all'):

    raise NotImplementedMethodError()

