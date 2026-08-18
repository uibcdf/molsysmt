from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:gro')
def to_mdtraj_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:gro to mdtraj.Topology.

    Parameters
    ----------
    item : file:gro
        Source item in file:gro form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Topology
        Resulting object in mdtraj.Topology form.

    .. versionadded:: 1.0.0
    """

    from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology as mdtraj_Trajectory_to_mdtraj_Topology

    tmp_item = to_mdtraj_Trajectory(item, atom_indices=atom_indices,
            structure_indices=structure_indices, skip_digestion=True)
    tmp_item = mdtraj_Trajectory_to_mdtraj_Topology(tmp_item, skip_digestion=True)

    return tmp_item

