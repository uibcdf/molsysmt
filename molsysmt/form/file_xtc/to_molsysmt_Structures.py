from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:xtc')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:xtc to molsysmt.Structures.

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
    molsysmt.Structures
        Resulting object in molsysmt.Structures form.

    .. versionadded:: 1.0.0
    """

    from .to_mdtraj_XTCTrajectoryFile import to_mdtraj_XTCTrajectoryFile
    from molsysmt.form.mdtraj_XTCTrajectoryFile.to_molsysmt_Structures import to_molsysmt_Structures as mdtraj_XTCTrajectoryFile_to_molsysmt_Structures
    import molsysmt as msm

    tmp_item = to_mdtraj_XTCTrajectoryFile(item, skip_digestion=True)
    res_item = mdtraj_XTCTrajectoryFile_to_molsysmt_Structures(tmp_item, atom_indices=atom_indices,
                                                               structure_indices=structure_indices,
                                                               skip_digestion=True)

    msm.form.close(tmp_item)

    return res_item

