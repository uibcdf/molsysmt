from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.Trajectory')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.Trajectory to molsysmt.Topology.

    Parameters
    ----------
    item : mdtraj.Trajectory
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.Topology
        Converted molecular system representation.
    """

    from .to_mdtraj_Topology import to_mdtraj_Topology as to_mdtraj_Topology_local
    from molsysmt.form.mdtraj_Topology.to_molsysmt_Topology import to_molsysmt_Topology as mdtraj_Topology_to_molsysmt_Topology_func

    tmp_item = to_mdtraj_Topology_local(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = mdtraj_Topology_to_molsysmt_Topology_func(tmp_item, atom_indices='all', skip_digestion=True)

    return tmp_item
