from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.GromacsTopFile')
def to_openmm_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from openmm.GromacsTopFile to openmm.Topology.

    Parameters
    ----------
    item : openmm.GromacsTopFile
        Source item in openmm.GromacsTopFile form.
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

    tmp_item = item.topology

    return tmp_item

