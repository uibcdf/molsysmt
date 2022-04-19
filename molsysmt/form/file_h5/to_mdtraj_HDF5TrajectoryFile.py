from molsysmt._private.digestion import digest_item, digest_atom_indices

def to_mdtraj_HDF5TrajectoryFile(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'file:h5')
        atom_indices = digest_atom_indices(atom_indices)

    from mdtraj.formats import HDF5TrajectoryFile
    from ..mdtraj_HDF5TrajectoryFile import extract as extract_mdtraj_HDF5TrajectoryFile

    tmp_item = HDF5TrajectoryFile(item)
    tmp_item = extract_mdtraj_HDF5TrajectoryFile(tmp_item, atom_indices=atom_indices,
                                                 structure_indices=structure_indices,
                                                 copy_if_all=False, check=False)

    return tmp_item

