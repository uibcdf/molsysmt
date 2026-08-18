from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:h5')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:h5 to molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.


    .. versionadded:: 1.0.0
    """

    from .to_mdtraj_HDF5TrajectoryFile import to_mdtraj_HDF5TrajectoryFile
    from molsysmt.form.mdtraj_HDF5TrajectoryFile.to_molsysmt_Topology import to_molsysmt_Topology as mdtraj_HDF5TrajectoryFile_to_molsysmt_Topology
    import molsysmt as msm

    tmp_item = to_mdtraj_HDF5TrajectoryFile(item, skip_digestion=True)
    try:
        res_item = mdtraj_HDF5TrajectoryFile_to_molsysmt_Topology(
            tmp_item,
            atom_indices=atom_indices,
            skip_digestion=True,
        )
    finally:
        msm.form.close(tmp_item)

    return res_item
