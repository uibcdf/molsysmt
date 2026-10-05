from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:gro")
def to_mdtraj_Topology(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """
    Converting from file:gro to mdtraj.Topology.

    This uses the same inferred connectivity as the native GRO conversion and
    the GRO-to-MDTraj trajectory route. Bonds are inferred on the full atom axis
    of the first structure before atom selection; unsupported chemistry remains
    subject to the existing template and distance-based candidate limitations.


    Parameters
    ----------
    item : molecular system
        Path to a GRO file declaring atom/group labels, coordinates and box data.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Source atom indices to retain after full-system connectivity inference.
        Defaults to 'all'.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Source structure indices to retain. Defaults to 'all'. Connectivity is
        inferred using the first structure before this selection.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Topology
        Resulting object in mdtraj.Topology form.


    Examples
    --------
    >>> import molsysmt as msm
    >>> topology = msm.convert(msm.systems['nglview']['md_1u19.gro'],
    ...                        to_form='mdtraj.Topology', selection=[0, 1])
    >>> topology.n_atoms
    2

    .. admonition:: User guide

       See :ref:`user-foundations-native-world-file-handlers-molsysmt-grofilehandler`
       for connectivity and coordinate-reading limits.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import (
        to_mdtraj_Topology as mdtraj_Trajectory_to_mdtraj_Topology,
    )

    from .to_mdtraj_Trajectory import to_mdtraj_Trajectory

    tmp_item = to_mdtraj_Trajectory(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    tmp_item = mdtraj_Trajectory_to_mdtraj_Topology(tmp_item, skip_digestion=True)

    return tmp_item
