from molsysmt._private.digestion import digest

@digest(form='file:h5')
def to_openmm_Topology(item, atom_indices='all', digest=True):

    from . import to_mdtraj_HDF5TrajectoryFile
    from .mdtraj_HDF5TrajectoryFile import to_openmm_Topology as mdtraj_HDF5TrajectoryFile_to_openmm_Topology

    tmp_item = to_mdtraj_HDF5TrajectoryFile(item, digest=False)
    tmp_item = mdtraj_HDF5TrajectoryFile_to_openmm_Topology(tmp_item, atom_indices=atom_indices, digest=False)

    return tmp_item

