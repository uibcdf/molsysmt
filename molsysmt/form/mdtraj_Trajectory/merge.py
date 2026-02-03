from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import arg_digest

@arg_digest(form='mdtraj.Trajectory')
def merge(items, atom_indices='all', structure_indices='all', skip_digestion=False):

   raise NotImplementedMethodError()

