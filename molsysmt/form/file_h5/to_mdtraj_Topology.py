from molsysmt._private.digestion import digest

@digest(form='file:h5')
def to_mdtraj_Topology(item, atom_indices='all'):

    from . import to_mdtraj_HDF5TrajectoryFile
    from ..mdtraj_HDF5TrajectoryFile import to_mdtraj_Topology as mdtraj_HDF5TrajectoryFile_to_mdtraj_Topology

    tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
    tmp_item = mdtraj_HDF5TrajectoryFile_to_mdtraj_Topology(tmp_item, atom_indices=atom_indices)

    return tmp_item

