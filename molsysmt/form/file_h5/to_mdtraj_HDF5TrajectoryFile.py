from molsysmt._private.digestion import digest
import os

@digest(form='file:h5')
def to_mdtraj_HDF5TrajectoryFile(item, atom_indices='all', structure_indices='all', mode='auto'):

    from mdtraj.formats import HDF5TrajectoryFile
    from ..mdtraj_HDF5TrajectoryFile import extract as extract_mdtraj_HDF5TrajectoryFile

    if mode=='auto':

        if os.path.isfile(item):
            mode = 'read'
        else:
            mode = 'write'

    if mode=='read':

        tmp_item = HDF5TrajectoryFile(item, mode='r')

        tmp_item = extract_mdtraj_HDF5TrajectoryFile(tmp_item, atom_indices=atom_indices,
                                                     structure_indices=structure_indices,
                                                     copy_if_all=False)

    elif mode=='write':

        tmp_item = HDF5TrajectoryFile(item, mode='w')


    return tmp_item

