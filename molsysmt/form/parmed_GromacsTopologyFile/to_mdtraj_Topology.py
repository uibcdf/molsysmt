from molsysmt._private.argdigest import arg_digest

@arg_digest(form='parmed.GromacsTopologyFile')
def to_mdtraj_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from parmed.GromacsTopologyFile to mdtraj.Topology.

    Parameters
    ----------
    item : parmed.GromacsTopologyFile
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.Topology
        Converted molecular system representation.
    """

    from molsysmt.form.parmed_Structure.to_mdtraj_Topology import to_mdtraj_Topology as parmed_Structure_to_mdtraj_Topology

    return parmed_Structure_to_mdtraj_Topology(item, atom_indices=atom_indices, skip_digestion=True)
