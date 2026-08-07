from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.GromacsTopFile', to_form='openmm.GromacsTopFile')
def add(to_item, item, atom_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


