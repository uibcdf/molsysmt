from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='pytraj.Topology', to_form='pytraj.Topology')
def add(to_item, item, atom_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

