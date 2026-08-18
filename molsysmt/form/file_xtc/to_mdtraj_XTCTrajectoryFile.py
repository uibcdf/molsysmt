from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:xtc')
def to_mdtraj_XTCTrajectoryFile(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:xtc to mdtraj.XTCTrajectoryFile.

    Parameters
    ----------
    item : file:xtc
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.XTCTrajectoryFile
        Converted molecular system representation.
    """

    from mdtraj.formats import XTCTrajectoryFile
    from ..mdtraj_XTCTrajectoryFile.extract import extract as extract_mdtraj_XTCTrajectoryFile

    tmp_item = XTCTrajectoryFile(item)
    tmp_item = extract_mdtraj_XTCTrajectoryFile(tmp_item, atom_indices=atom_indices,
                                                structure_indices=structure_indices,
                                                copy_if_all=False, skip_digestion=True)

    return tmp_item

