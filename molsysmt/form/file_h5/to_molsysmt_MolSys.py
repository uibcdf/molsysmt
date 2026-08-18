from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:h5')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:h5 to molsysmt.MolSys.


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
    molsysmt.MolSys
        Resulting object in molsysmt.MolSys form.


    .. versionadded:: 1.0.0
    """

    from .to_mdtraj_HDF5TrajectoryFile import to_mdtraj_HDF5TrajectoryFile
    from molsysmt.form.mdtraj_HDF5TrajectoryFile.to_molsysmt_MolSys import to_molsysmt_MolSys as mdtraj_HDF5TrajectoryFile_to_molsysmt_MolSys
    import molsysmt as msm

    tmp_item = to_mdtraj_HDF5TrajectoryFile(item, skip_digestion=True)
    try:
        res_item = mdtraj_HDF5TrajectoryFile_to_molsysmt_MolSys(
            tmp_item,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            skip_digestion=True,
        )
    finally:
        msm.form.close(tmp_item)

    return res_item
