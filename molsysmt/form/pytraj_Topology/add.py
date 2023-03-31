from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='pytraj.Topology', to_form='pytraj.Topology')
def add(to_item, item, atom_indices='all'):

    raise NotImplementedMethodError()

