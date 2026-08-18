from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.HDF5TrajectoryFile')
def to_mdtraj_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.HDF5TrajectoryFile to mdtraj.Topology.

    Parameters
    ----------
    item : mdtraj.HDF5TrajectoryFile
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.Topology
        Converted molecular system representation.
    """

    from ..mdtraj_Topology.extract import extract as extract_mdtraj_Topology

    tmp_item = item.topology
    tmp_item = extract_mdtraj_Topology(tmp_item, atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)

    return tmp_item

