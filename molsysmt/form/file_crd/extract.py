from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='file:crd')
def extract(item, atom_indices='all', structure_indices='all', output_filename=None, copy_if_all=True,
        progress_bar=False, skip_digestion=False):
    """
    Extracting a subset of elements or structures from form file:crd.

    Parameters
    ----------
    item : file:crd
        Source item in file:crd form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    output_filename : str or pathlib.Path
        Output file path for serialization.
    copy_if_all : object
        Argument copy_if_all.
    progress_bar : object
        Argument progress_bar.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:crd
        Resulting object in file:crd form.

    .. versionadded:: 1.0.0
    """

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

        #from molsysmt.form.mdtraj_HDF5TrajectoryFile.to_mdtraj_HDF5TrajectoryFile import to_mdtraj_HDF5TrajectoryFile
        #from ..mdtraj_HDF5TrajectoryFile.extract import extract as extract_mdtraj_HDF5TrajectoryFile

        #tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
        #tmp_item = extract_mdtraj_HDF5TrajectoryFile(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
        #        output_filename=output_filename, copy_if_all=copy_if_all, progress_bar=progress_bar)
        #tmp_item.close()

        #tmp_item = output_filename

        raise NotImplementedMethodError

    return tmp_item

