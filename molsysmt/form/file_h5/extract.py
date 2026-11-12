from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form="file:h5")
@dep_digest("mdtraj")
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
    Extracting a subset of elements or structures from form file:h5.


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
        temporary copy for whole-file extraction. Subset serialization needs
        an explicit distinct destination; use native conversion for an
        in-memory subset.
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
    file:h5
        Resulting object in file:h5 form.


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

        return copy_file(item, output_filename, caller="molsysmt.form.file_h5.extract")
    else:
        from molsysmt._private.files_and_directories import validate_copy_destination
        from molsysmt._private.smonitor import ArgumentError

        from ..mdtraj_HDF5TrajectoryFile.extract import (
            extract as extract_mdtraj_HDF5TrajectoryFile,
        )
        from .to_mdtraj_HDF5TrajectoryFile import to_mdtraj_HDF5TrajectoryFile

        if output_filename is None:
            raise ArgumentError(
                "output_filename",
                value=None,
                caller="molsysmt.form.file_h5.extract",
                message="HDF5 subset extraction requires a distinct output_filename; convert to native structures for an in-memory selection.",
            )
        validate_copy_destination(
            item, output_filename, caller="molsysmt.form.file_h5.extract"
        )
        destination = output_filename
        reader = to_mdtraj_HDF5TrajectoryFile(item, skip_digestion=True)
        extracted = None
        try:
            extracted = extract_mdtraj_HDF5TrajectoryFile(
                reader,
                atom_indices=atom_indices,
                structure_indices=structure_indices,
                output_filename=destination,
                copy_if_all=copy_if_all,
                progress_bar=progress_bar,
                skip_digestion=True,
            )
        finally:
            try:
                if extracted is not None and extracted is not reader:
                    extracted.close()
            finally:
                reader.close()
        tmp_item = destination

    return tmp_item
