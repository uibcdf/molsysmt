from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='pytraj.Topology', to_form='pytraj.Topology')
def add(to_item, item, atom_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

