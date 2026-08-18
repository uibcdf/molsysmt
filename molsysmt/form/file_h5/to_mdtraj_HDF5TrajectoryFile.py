from molsysmt._private.argdigest import arg_digest
import os

@arg_digest(form='file:h5')
def to_mdtraj_HDF5TrajectoryFile(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:h5 to mdtraj.HDF5TrajectoryFile.

    Parameters
    ----------
    item : file:h5
        Source item in file:h5 form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.HDF5TrajectoryFile
        Resulting object in mdtraj.HDF5TrajectoryFile form.

    .. versionadded:: 1.0.0
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
