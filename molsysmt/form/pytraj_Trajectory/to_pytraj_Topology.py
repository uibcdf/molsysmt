from molsysmt._private.argdigest import arg_digest

@arg_digest(form='pytraj.Trajectory')
def to_pytraj_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from pytraj.Trajectory to pytraj.Topology.


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
    pytraj.Topology
        Resulting object in pytraj.Topology form.


    .. versionadded:: 1.0.0
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
