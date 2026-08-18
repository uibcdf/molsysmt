from molsysmt._private.argdigest import arg_digest

@arg_digest(form='parmed.GromacsTopologyFile')
def to_mdtraj_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from parmed.GromacsTopologyFile to mdtraj.Topology.


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
    mdtraj.Topology
        Resulting object in mdtraj.Topology form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.parmed_Structure.to_mdtraj_Topology import to_mdtraj_Topology as parmed_Structure_to_mdtraj_Topology

    return parmed_Structure_to_mdtraj_Topology(item, atom_indices=atom_indices, skip_digestion=True)
