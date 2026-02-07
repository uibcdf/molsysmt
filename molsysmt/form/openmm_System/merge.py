from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openmm.System')
def merge(items, atom_indices='all', structure_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

