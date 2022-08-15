from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='mdtraj.HDF5TrajectoryFile', to_form='mdtraj.HDF5TrajectoryFile')
def add(to_item, item):

    raise NotImplementedMethodError()

