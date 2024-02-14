from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='file:crd')
def extract(item, atom_indices='all', structure_indices='all', output_filename=None, copy_if_all=True,
        progress_bar=False, skip_digestion=False):

    if output_filename is None:
        output_filename = item

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all or (output_filename!=item):

            from shutil import copy as copy_file
            copy_file(item, output_filename)
            tmp_item = output_filename

        else:

            tmp_item = item
    else:

        #from . import to_mdtraj_HDF5TrajectoryFile
        #from ..mdtraj_HDF5TrajectoryFile import extract as extract_mdtraj_HDF5TrajectoryFile

        #tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
        #tmp_item = extract_mdtraj_HDF5TrajectoryFile(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
        #        output_filename=output_filename, copy_if_all=copy_if_all, progress_bar=progress_bar)
        #tmp_item.close()

        #tmp_item = output_filename

        raise NotImplementedMethodError

    return tmp_item

