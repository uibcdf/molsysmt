from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.Topology')
def to_parmed_GromacsTopologyFile(item, atom_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.Topology to parmed.GromacsTopologyFile.

    Parameters
    ----------
    item : mdtraj.Topology
        Source item in mdtraj.Topology form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    parmed.GromacsTopologyFile
        Resulting object in parmed.GromacsTopologyFile form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.parmed_Structure.to_parmed_Structure import to_parmed_Structure
    from molsysmt.form.parmed_Structure.to_parmed_GromacsTopologyFile import to_parmed_GromacsTopologyFile as parmed_Structure_to_parmed_GromacsTopologyFile

    tmp_item = to_parmed_Structure(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = parmed_Structure_to_parmed_GromacsTopologyFile(tmp_item, skip_digestion=True)

    return tmp_item

