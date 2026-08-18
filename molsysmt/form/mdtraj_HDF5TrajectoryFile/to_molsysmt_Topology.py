from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.HDF5TrajectoryFile')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.HDF5TrajectoryFile to molsysmt.Topology.


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

    from .to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.to_molsysmt_Topology import to_molsysmt_Topology as mdtraj_Topology_to_molsysmt_Topology_func

    tmp_item = to_mdtraj_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = mdtraj_Topology_to_molsysmt_Topology_func(tmp_item, atom_indices='all', skip_digestion=True)

    return tmp_item

