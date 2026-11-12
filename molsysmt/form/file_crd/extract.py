from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.variables import is_all


@arg_digest(form="file:crd")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    output_filename=None,
    copy_if_all=True,
    progress_bar=False,
    skip_digestion=False,
):
    """
    Extracting a subset of elements or structures from form file:crd.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    output_filename : str or pathlib.Path, default=None
        Destination for an independent file. None creates a session-owned
        temporary copy for whole-file extraction; supported subset writers
        follow the same independent-output policy.
    copy_if_all : bool, default=True
        Whether to copy a complete selection. False permits returning the
        source when no distinct destination is requested. A distinct explicit
        destination is honored regardless of this flag.
    progress_bar : object, default=False
        Argument progress_bar.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:crd
        Resulting object in file:crd form.


    Raises
    ------
    ArgumentError
        If a requested copy destination aliases the source or names a directory.


    .. versionadded:: 1.0.0
    """

    if is_all(atom_indices) and is_all(structure_indices):
        if not copy_if_all and (
            output_filename is None or str(output_filename) == str(item)
        ):
            return item
        from molsysmt._private.files_and_directories import copy_file

        return copy_file(item, output_filename, caller="molsysmt.form.file_crd.extract")
    else:
        # from molsysmt.form.mdtraj_HDF5TrajectoryFile.to_mdtraj_HDF5TrajectoryFile import to_mdtraj_HDF5TrajectoryFile
        # from ..mdtraj_HDF5TrajectoryFile.extract import extract as extract_mdtraj_HDF5TrajectoryFile

        # tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
        # tmp_item = extract_mdtraj_HDF5TrajectoryFile(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
        #        output_filename=output_filename, copy_if_all=copy_if_all, progress_bar=progress_bar)
        # tmp_item.close()

        # tmp_item = output_filename

        raise NotImplementedMethodError
