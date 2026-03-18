from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openff.Topology', to_form='openff.Topology')
def add(to_item, item, atom_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()
