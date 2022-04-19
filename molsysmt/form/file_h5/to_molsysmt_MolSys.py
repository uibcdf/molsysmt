from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'file:h5')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_mdtraj_HDF5TrajectoryFile
    from .mdtraj_HDF5TrajectoryFile import to_molsysmt_MolSys as mdtraj_HDF5TrajectoryFile_to_molsysmt_MolSys

    tmp_item = to_mdtraj_HDF5TrajectoryFile(item, check=False)
    tmp_item = mdtraj_HDF5TrajectoryFile_to_molsysmt_MolSys(tmp_item, atom_indices=atom_indices,
                                                            structure_indices=structure_indices, check=False)

    return tmp_item

