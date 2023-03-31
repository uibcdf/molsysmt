from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='mdtraj.XTCTrajectoryFile', to_form='mdtraj.XTCTrajectoryFile')
def add(to_item, item, atom_indices='all', structure_indices='all'):

    raise NotImplementedMethodError()

