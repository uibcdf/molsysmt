from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.Trajectory', to_form='mdtraj.Trajectory')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):

   raise NotImplementedMethodError()

