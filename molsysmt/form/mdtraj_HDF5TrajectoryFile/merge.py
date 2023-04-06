from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='mdtraj.HDF5TrajectoryFile')
def merge(items, atom_indices='all', structure_indices='all'):

    raise NotImplementedMethodError()

