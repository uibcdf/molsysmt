from molsysmt._private.digestion import digest

@digest(form='file:h5')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all'):

    from . import to_mdtraj_HDF5TrajectoryFile
    from .mdtraj_HDF5TrajectoryFile import to_mdtraj_Trajectory as mdtraj_HDF5TrajectoryFile_to_mdtraj_Trajectory

    tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
    tmp_item = mdtraj_HDF5TrajectoryFile_to_mdtraj_Trajectory(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            )

    return tmp_item

