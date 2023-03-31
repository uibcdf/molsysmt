from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.Structures', to_form='molsysmt.Structures')
def add(to_item, item, atom_indices='all', structure_indices='all'):

    to_item.add(item)

    pass

