from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:xtc')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:xtc to mdtraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Trajectory
        Resulting object in mdtraj.Trajectory form.


    .. versionadded:: 1.0.0
    """

    from .to_mdtraj_XTCTrajectoryFile import to_mdtraj_XTCTrajectoryFile
    from molsysmt.form.mdtraj_XTCTrajectoryFile.to_mdtraj_Trajectory import to_mdtraj_Trajectory as mdtraj_XTCTrajectoryFile_to_mdtraj_Trajectory
    import molsysmt as msm

    tmp_item = to_mdtraj_XTCTrajectoryFile(item, skip_digestion=True)
    res_item = mdtraj_XTCTrajectoryFile_to_mdtraj_Trajectory(tmp_item, atom_indices=atom_indices,
                structure_indices=structure_indices, skip_digestion=True)

    msm.form.close(tmp_item)

    return res_item

