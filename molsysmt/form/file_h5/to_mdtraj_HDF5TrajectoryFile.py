from molsysmt._private.digestion import digest
import os

@digest(form='file:h5')
def to_mdtraj_HDF5TrajectoryFile(item, atom_indices='all', structure_indices='all'):

    from mdtraj.formats import HDF5TrajectoryFile
    from ..mdtraj_HDF5TrajectoryFile import extract as extract_mdtraj_HDF5TrajectoryFile

    tmp_item = HDF5TrajectoryFile(item, mode='r')

    tmp_item = extract_mdtraj_HDF5TrajectoryFile(tmp_item, atom_indices=atom_indices,
                                                 structure_indices=structure_indices,
                                                 copy_if_all=False)

    return tmp_item

def _to_mdtraj_HDF5TrajectoryFile(item, atom_indices='all', structure_indices='all'):

    return to_mdtraj_HDF5TrajectoryFile(item, atom_indices=atom_indices, structure_indices=structure_indices)
