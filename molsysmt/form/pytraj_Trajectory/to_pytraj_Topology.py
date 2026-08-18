from molsysmt._private.argdigest import arg_digest

@arg_digest(form='pytraj.Trajectory')
def to_pytraj_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from pytraj.Trajectory to pytraj.Topology.

    Parameters
    ----------
    item : pytraj.Trajectory
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    pytraj.Topology
        Converted molecular system representation.
    """

    from ..pytraj_Topology.extract import extract as extract_pytraj_Topology

    tmp_item = item.topology
    tmp_item = extract_pytraj_Topology(
        tmp_item,
        atom_indices=atom_indices,
        copy_if_all=False,
        skip_digestion=True,
    )

    return tmp_item
