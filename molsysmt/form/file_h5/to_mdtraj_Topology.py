from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:h5')
def to_mdtraj_Topology(item, atom_indices='all', skip_digestion=False):

    from .to_mdtraj_HDF5TrajectoryFile import to_mdtraj_HDF5TrajectoryFile
    from molsysmt.form.mdtraj_HDF5TrajectoryFile.to_mdtraj_Topology import to_mdtraj_Topology as mdtraj_HDF5TrajectoryFile_to_mdtraj_Topology

    source = to_mdtraj_HDF5TrajectoryFile(item, skip_digestion=True)
    try:
        tmp_item = mdtraj_HDF5TrajectoryFile_to_mdtraj_Topology(
            source,
            atom_indices=atom_indices,
            skip_digestion=True,
        )
    finally:
        source.close()

    return tmp_item
