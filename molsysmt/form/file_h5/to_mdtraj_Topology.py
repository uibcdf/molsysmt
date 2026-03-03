from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:h5')
def to_mdtraj_Topology(item, atom_indices='all', skip_digestion=False):

    from ..mdtraj_HDF5TrajectoryFile.to_mdtraj_HDF5TrajectoryFile import to_mdtraj_HDF5TrajectoryFile
    from ..mdtraj_HDF5TrajectoryFile.to_mdtraj_Topology import to_mdtraj_Topology as mdtraj_HDF5TrajectoryFile_to_mdtraj_Topology

    tmp_item = to_mdtraj_HDF5TrajectoryFile(item, skip_digestion=True)
    tmp_item = mdtraj_HDF5TrajectoryFile_to_mdtraj_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

