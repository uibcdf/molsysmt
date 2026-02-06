from molsysmt.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='molsysmt.StructuresDict', to_form='molsysmt.StructuresDict')
def add(to_item, item, atom_indices='all', structure_indices='all'):

    raise NotImplementedMethodError()

