from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.Trajectory')
def to_mdtraj_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.Trajectory to mdtraj.Topology.

    Parameters
    ----------
    item : mdtraj.Trajectory
        Source item in mdtraj.Trajectory form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Topology
        Resulting object in mdtraj.Topology form.

    .. versionadded:: 1.0.0
    """

    from ..mdtraj_Topology.extract import extract as extract_mdtraj_Topology
    from mdtraj.core.topology import Topology as mdtraj_Topology

    if isinstance(item, mdtraj_Topology):
        tmp_item = item
    elif hasattr(item, 'topology'):
        tmp_item = item.topology
    else:
        # Emergency path for file handlers or strings
        import mdtraj as mdt
        if isinstance(item, str):
            tmp_item = mdt.load_topology(item)
        else:
            # Maybe a handler?
            tmp_item = item.topology

    tmp_item = extract_mdtraj_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

