from molsysmt._private.digestion import digest

@digest(form='file:h5')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', digest=True):

    from . import to_mdtraj_HDF5TrajectoryFile
    from ..mdtraj_HDF5TrajectoryFile import to_molsysmt_MolSys as mdtraj_HDF5TrajectoryFile_to_molsysmt_MolSys

    tmp_item = to_mdtraj_HDF5TrajectoryFile(item, digest=False)
    tmp_item = mdtraj_HDF5TrajectoryFile_to_molsysmt_MolSys(tmp_item, atom_indices=atom_indices,
                                                            structure_indices=structure_indices, digest=False)

    return tmp_item

