from molsysmt._private.argdigest import arg_digest

@arg_digest(form='pytraj.Trajectory')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from pytraj.Trajectory to molsysmt.Topology.

    Parameters
    ----------
    item : pytraj.Trajectory
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.Topology
        Converted molecular system representation.
    """

    from .to_pytraj_Topology import to_pytraj_Topology
    from molsysmt.form.pytraj_Topology.to_molsysmt_Topology import (
        to_molsysmt_Topology as pytraj_Topology_to_molsysmt_Topology,
    )

    tmp_item = to_pytraj_Topology(item, skip_digestion=True)
    tmp_item = pytraj_Topology_to_molsysmt_Topology(
        tmp_item,
        atom_indices=atom_indices,
        skip_digestion=True,
    )

    return tmp_item
