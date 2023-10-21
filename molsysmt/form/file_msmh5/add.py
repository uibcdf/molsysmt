from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:msmh5', to_form='file:msmh5')
def add(to_item, item, atom_indices='all', structure_indices='all'):

    raise NotImplementedMethodError()

