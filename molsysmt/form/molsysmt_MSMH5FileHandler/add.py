from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.MSMH5FileHandler', to_form='molsysmt.MSMH5FileHandler')
def add(to_item, item, atom_indices='all', structure_indices='all'):

    raise NotImplementedMethodError()

