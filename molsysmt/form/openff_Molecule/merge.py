from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openff.Molecule')
def merge(items, atom_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()
