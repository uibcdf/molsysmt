from molsysmt._private.argdigest import arg_digest
import os

@arg_digest(form='file:h5')
def to_mdtraj_HDF5TrajectoryFile(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:h5 to mdtraj.HDF5TrajectoryFile.

    Parameters
    ----------
    item : file:h5
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.HDF5TrajectoryFile
        Converted molecular system representation.
    """

    from mdtraj.formats import HDF5TrajectoryFile
    from molsysmt.form.mdtraj_HDF5TrajectoryFile.extract import extract as extract_mdtraj_HDF5TrajectoryFile

    if isinstance(item, (str, os.PathLike)):
        tmp_item = HDF5TrajectoryFile(str(item), mode='r')
    else:
        tmp_item = item

    tmp_item = extract_mdtraj_HDF5TrajectoryFile(tmp_item, atom_indices=atom_indices,
                                                 structure_indices=structure_indices,
                                                 copy_if_all=False, skip_digestion=True)

    return tmp_item
