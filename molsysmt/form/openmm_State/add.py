from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openmm.State', to_form='openmm.State')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

