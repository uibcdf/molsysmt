from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolSys')
def to_pytraj_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.MolSys to pytraj.Topology.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    pytraj.Topology
        Converted molecular system representation.
    """

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology.to_pytraj_Topology import to_pytraj_Topology as molsysmt_Topology_to_pytraj_Topology

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    tmp_item = molsysmt_Topology_to_pytraj_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

