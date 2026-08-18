from molsysmt._private.argdigest import arg_digest

@arg_digest(form='parmed.GromacsTopologyFile')
def to_openmm_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from parmed.GromacsTopologyFile to openmm.Topology.

    Parameters
    ----------
    item : parmed.GromacsTopologyFile
        Source item in parmed.GromacsTopologyFile form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Topology
        Resulting object in openmm.Topology form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.parmed_Structure.to_openmm_Topology import to_openmm_Topology as parmed_Structure_to_openmm_Topology

    return parmed_Structure_to_openmm_Topology(item, atom_indices=atom_indices, skip_digestion=True)
