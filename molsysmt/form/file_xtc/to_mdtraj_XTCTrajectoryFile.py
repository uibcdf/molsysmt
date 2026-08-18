from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:xtc')
def to_mdtraj_XTCTrajectoryFile(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:xtc to mdtraj.XTCTrajectoryFile.

    Parameters
    ----------
    item : file:xtc
        Source item in file:xtc form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.XTCTrajectoryFile
        Resulting object in mdtraj.XTCTrajectoryFile form.

    .. versionadded:: 1.0.0
    """

    from mdtraj.formats import XTCTrajectoryFile
    from ..mdtraj_XTCTrajectoryFile.extract import extract as extract_mdtraj_XTCTrajectoryFile

    tmp_item = XTCTrajectoryFile(item)
    tmp_item = extract_mdtraj_XTCTrajectoryFile(tmp_item, atom_indices=atom_indices,
                                                structure_indices=structure_indices,
                                                copy_if_all=False, skip_digestion=True)

    return tmp_item

