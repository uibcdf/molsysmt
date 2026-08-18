from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:h5')
def to_openmm_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:h5 to openmm.Topology.

    Parameters
    ----------
    item : file:h5
        Source item in file:h5 form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Topology
        Resulting object in openmm.Topology form.

    .. versionadded:: 1.0.0
    """

    from .to_mdtraj_HDF5TrajectoryFile import to_mdtraj_HDF5TrajectoryFile
    from molsysmt.form.mdtraj_HDF5TrajectoryFile.to_openmm_Topology import to_openmm_Topology as mdtraj_HDF5TrajectoryFile_to_openmm_Topology

    tmp_item = to_mdtraj_HDF5TrajectoryFile(item, skip_digestion=True)
    tmp_item = mdtraj_HDF5TrajectoryFile_to_openmm_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

